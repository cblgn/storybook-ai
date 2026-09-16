#!/usr/bin/env bash
set -euo pipefail

if (( BASH_VERSINFO[0] < 4 || (BASH_VERSINFO[0] == 4 && BASH_VERSINFO[1] < 3) )); then
  echo "Ce script nécessite Bash 4.3 ou supérieur." >&2
  exit 1
fi

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v uv >/dev/null || ! command -v node >/dev/null; then
  echo "Installez uv et Node.js avant de lancer l’application (voir README.md)." >&2
  exit 1
fi

if command -v pnpm >/dev/null; then
  pnpm_command=(pnpm)
elif command -v npm >/dev/null; then
  pnpm_version="$(node -p "require(process.argv[1]).packageManager" "$project_dir/frontend/package.json")"
  pnpm_command=(npm exec --yes "--package=$pnpm_version" -- pnpm)
else
  echo "Installez pnpm (voir README.md)." >&2
  exit 1
fi

# Each command gets a process group, including reloaders and their children.
set -m
process_ids=()
cleanup() {
  trap '' INT TERM
  for pid in "${process_ids[@]}"; do
    kill -TERM -- "-$pid" 2>/dev/null || true
  done
  wait || true
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

cd "$project_dir/backend"
uv sync --locked --no-build &
process_ids+=("$!")
wait "$!"

cd "$project_dir/frontend"
"${pnpm_command[@]}" install --frozen-lockfile &
process_ids+=("$!")
wait "$!"
process_ids=()

backend_options=()
if [[ -f "$project_dir/backend/.env" ]]; then
  backend_options+=(--env-file "$project_dir/backend/.env")
fi

echo "Application : http://localhost:5173 — API : http://localhost:8000"
echo "Ctrl+C arrête les deux serveurs."

cd "$project_dir/backend"
uv run --locked --no-build uvicorn storybook.api.app:app --reload --host 127.0.0.1 --port 8000 \
  --timeout-graceful-shutdown 5 "${backend_options[@]}" &
process_ids+=("$!")

cd "$project_dir/frontend"
"${pnpm_command[@]}" dev &
process_ids+=("$!")

# If either server exits, stop the other and report the failure.
status=0
wait -n "${process_ids[@]}" || status=$?
echo "Un serveur s’est arrêté ; arrêt de l’application." >&2
if (( status == 0 )); then status=1; fi
exit "$status"

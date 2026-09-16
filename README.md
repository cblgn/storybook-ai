# Storybook AI

Des histoires du soir personnalisées, en français. Monorepo local : React → FastAPI
→ service de génération → Writer PydanticAI → histoire structurée.

La tâche 001 fournit le formulaire, la génération avec le Writer, l’affichage,
les erreurs et la connexion de santé. Le Planner, le Reviewer et la révision
unique restent la prochaine étape du MVP décrit dans `SPEC.md`.

## Prérequis

- Python **3.14+** et [uv](https://docs.astral.sh/uv/).
- Node.js 24.15+ sur la branche 24 (prévue pour la CI), ou 22.22.2+ sur la branche 22,
  ou 26+, et pnpm 10.34.5. Ces versions sont celles prises en charge par le projet.
- Un fournisseur LLM configuré pour générer de vraies histoires.

Si pnpm n’est pas installé : `npm install --global pnpm@10.34.5`.

## Démarrage local

Depuis la racine, une seule commande lance l’application complète en développement :

```bash
./scripts/dev.sh
```

Le script nécessite Bash 4.3+, synchronise les dépendances verrouillées, charge
`backend/.env` s’il existe et lance FastAPI et Vite avec rechargement automatique.
Si pnpm est absent, il utilise la version du projet via `npm exec` (téléchargée
au besoin). **Ctrl+C arrête les deux serveurs**, ainsi que leurs sous-processus.
Si un serveur échoue, l’autre est également arrêté. Les ports 8000 et 5173 doivent
être disponibles. Le script fonctionne aussi depuis un autre répertoire.

Pour lancer les serveurs séparément, terminal 1 depuis la racine :

```bash
cd backend
uv sync --locked
uv run uvicorn storybook.api.app:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2, depuis la racine :

```bash
cd frontend
pnpm install --frozen-lockfile
pnpm dev
```

Ouvrir **http://localhost:5173**. Vite transmet `/api` à FastAPI sur le port 8000.
La page affiche « Service connecté » lorsque `/api/health` répond. Ce contrôle
vérifie le serveur, pas l’authentification du fournisseur LLM.

## Fournisseur LLM

Par défaut, le Writer utilise `openai-codex:gpt-5.6-luna` via le fournisseur natif
[PydanticAI Codex](https://pydantic.dev/docs/ai/models/openai-codex/).
Il utilise l’authentification locale existante de Codex ; celle-ci reste hors du
projet. Aucune clé ni aucun fichier d’authentification ne doit être copié ici.

Le modèle est configurable via `STORYBOOK_MODEL`, au format `fournisseur:modèle`.
La distribution `pydantic-ai-slim[openai]` inclut les fournisseurs Codex et OpenAI.
Pour un autre fournisseur, installer l’extra PydanticAI correspondant.

Configuration facultative :

```bash
cd backend
cp .env.example .env
# Modifier les variables nécessaires dans .env.
uv run uvicorn storybook.api.app:app --reload --env-file .env --port 8000
```

Pour une clé API, choisir un modèle `openai:...` disponible sur votre compte et
renseigner `OPENAI_API_KEY` dans l’environnement ou le `.env` chargé par uvicorn.
`STORYBOOK_GENERATION_TIMEOUT_SECONDS` vaut 180 par défaut. Le Writer autorise une
nouvelle tentative en cas de sortie invalide et au plus trois appels au modèle.
Cette validation de structure ne remplace pas la future relecture narrative.

Sans authentification valide, le serveur et l’interface démarrent quand même ;
la génération affiche un message d’erreur permettant de réessayer.

## API

- `GET /api/health` → `{"status":"ok"}`
- `POST /api/stories` → un `StoryBook` validé (titre, synopsis, personnages, scènes,
  phrase de clôture).
- Documentation interactive : http://localhost:8000/docs

Exemple de requête :

```bash
curl http://localhost:8000/api/stories \
  -H 'Content-Type: application/json' \
  -d '{"child_name":"Léa","age":6,"hero":"un petit dragon timide","setting":"forêt enchantée","theme":"prendre confiance en soi","duration_minutes":3}'
```

Âge : 3–12 ans, durée : 3, 5 ou 10 minutes approximatives. Le prénom est facultatif.
Les erreurs de validation retournent 422 ; les échecs de génération retournent
503 avec un message générique. Aucune histoire n’est conservée après rechargement.

## Vérifications

```bash
cd backend
uv run pytest
uv run ruff check .
uv run mypy src
```

```bash
cd frontend
pnpm lint
pnpm build
pnpm exec playwright install chromium
pnpm test:e2e
```

Les tests Python interdisent les appels à un vrai LLM. Les tests navigateur
démarrent FastAPI et Vite avec un `TestModel` PydanticAI déterministe. Ils couvrent
le proxy, les champs, l’envoi, les résultats, l’attente et la reprise après erreur,
sur ordinateur et mobile. Libérer les ports 8000 et 5173 avant `pnpm test:e2e`.
Les tests de fournisseur réel sont marqués `integration` et exclus par défaut.

`pnpm build` produit `frontend/dist`. FastAPI ne sert pas encore ce build ;
utiliser `./scripts/dev.sh` pour le parcours complet en développement.

## Organisation

```text
backend/src/storybook/
  api/         # Routes HTTP et injection du service
  domain/      # Contrats Pydantic
  agents/      # Writer, sans concepts HTTP
  services/    # Génération, délai maximal et traduction des erreurs
  settings.py  # Configuration par environnement
frontend/src/
  components/ui/   # Primitives shadcn/ui adaptées au thème
  features/story/  # Formulaire, API typée et lecture
  lib/             # Fetch et utilitaires
```

Les lockfiles uv et pnpm sont intentionnellement versionnables. Les secrets,
environnements, dépendances, caches et builds sont ignorés par Git.

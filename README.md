# Storybook AI

[![CI](https://github.com/cblgn/storybook-ai/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/cblgn/storybook-ai/actions/workflows/ci.yml)
[![Security](https://github.com/cblgn/storybook-ai/actions/workflows/security.yml/badge.svg?branch=main)](https://github.com/cblgn/storybook-ai/actions/workflows/security.yml)
[![CodeQL](https://github.com/cblgn/storybook-ai/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/cblgn/storybook-ai/actions/workflows/codeql.yml)

[![Sonar Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=cblgn_storybook-ai&metric=alert_status)](https://sonarcloud.io/dashboard?id=cblgn_storybook-ai)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=cblgn_storybook-ai&metric=coverage)](https://sonarcloud.io/component_measures?id=cblgn_storybook-ai&metric=coverage)

Des histoires du soir personnalisées, en français. Monorepo local : React → FastAPI
→ service de génération → Writer PydanticAI → histoire structurée.

Le socle actuel fournit le formulaire, la génération avec le Writer, l’affichage,
les erreurs et la connexion de santé. Le Planner, le Reviewer et la révision
unique restent la prochaine étape du MVP décrit dans [SPEC.md](SPEC.md).

Pour contribuer, suivre [CONTRIBUTING.md](CONTRIBUTING.md) : une issue GitHub
décrit le travail, une PR en porte l’implémentation. Les instructions des agents
sont dans [AGENTS.md](AGENTS.md) ; les décisions d’architecture significatives
se documentent dans [docs/adr/](docs/adr/README.md).

## Qualité et sécurité

`main` est protégé : PR obligatoire, checks réussis, branche à jour et squash merge.
La CI reste déterministe, sans appel LLM : lint, typage, tests, build et couverture
backend minimale de 80 %. Les audits de dépendances, CodeQL, Dependabot, le scan de
secrets et la protection au push complètent ces contrôles. Les Actions sont
épinglées à des SHA complets, avec des permissions minimales.

Le [projet SonarQube Cloud](https://sonarcloud.io/dashboard?id=cblgn_storybook-ai)
utilise un workflow CI dédié à `main`, avec les rapports de couverture Python et
TypeScript et une vérification bloquante de la Quality Gate. L’activation et son
statut effectif sont décrits dans la documentation de sécurité.
Voir la [politique de sécurité](SECURITY.md) pour un signalement privé
et la [vérification des protections](docs/repository-security.md).

## Prérequis

- Python **3.14+** et [uv](https://docs.astral.sh/uv/).
- Node.js 24.15+ sur la branche 24 (utilisée en CI), ou 22.22.2+ sur la branche 22,
  ou 26+, et pnpm 10.34.5. Ces minimums incluent les exigences de jsdom.
- [Ollama](https://ollama.com/download) récent et le modèle `qwen3.5:0.8b`
  pour générer localement, sans clé API (voir ci-dessous).

Si pnpm n’est pas installé : `npm install --global pnpm@10.34.5`.

## Démarrage local

Après avoir démarré Ollama et téléchargé le modèle (section suivante), lancer
FastAPI et React depuis la racine :

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
vérifie FastAPI, pas la disponibilité d’Ollama ou du modèle.

## Fournisseur LLM

Par défaut, le Writer utilise **Qwen3.5 0.8B dans Ollama**, via l’API compatible
OpenAI sur `http://127.0.0.1:11434/v1`. PydanticAI transmet le schéma JSON et valide
le `StoryBook` retourné. Le raisonnement est désactivé pour limiter la latence.
La génération tourne sur CPU, sans clé API, abonnement ou repli cloud.

Installer Ollama depuis sa [documentation officielle](https://docs.ollama.com/linux),
puis lancer le serveur dans un terminal dédié (Linux/WSL) :

```bash
OLLAMA_HOST=127.0.0.1:11434 OLLAMA_NO_CLOUD=1 \
  OLLAMA_CONTEXT_LENGTH=8192 OLLAMA_NUM_PARALLEL=1 ollama serve
```

Si Ollama tourne déjà comme service, lui appliquer ces variables et le redémarrer
plutôt que lancer un second serveur. Garder l’API sur l’interface locale.
Dans un autre terminal, télécharger le modèle une fois, puis lancer l’application :

```bash
ollama pull qwen3.5:0.8b
./scripts/dev.sh
```

Le modèle occupe environ 1 Go sur disque, en plus du runtime et de la mémoire
nécessaire à l’inférence. Les téléchargements nécessitent Internet ; la génération
n’en a plus besoin ensuite. Ne pas ajouter le runtime ou les modèles au dépôt.
Le modèle 0,8B est un premier essai : la qualité du français, la cohérence et la
durée demandée doivent être évaluées sur de vraies histoires. Le schéma valide
la structure, pas la qualité narrative. La synthèse vocale reste une étape séparée.

Le modèle est configurable via `STORYBOOK_MODEL`, au format `fournisseur:modèle`.
`STORYBOOK_OLLAMA_BASE_URL` permet de changer l’adresse d’un serveur Ollama
de confiance ; conserver le suffixe `/v1`. La distribution
`pydantic-ai-slim[openai]` inclut les fournisseurs Ollama, Codex et OpenAI.
Pour un autre fournisseur, installer l’extra PydanticAI correspondant.

Configuration facultative :

```bash
cd backend
cp .env.example .env
# Modifier les variables nécessaires dans .env.
uv run uvicorn storybook.api.app:app --reload --env-file .env --port 8000
```

Pour utiliser explicitement un fournisseur distant, choisir un modèle `openai:...` et
renseigner `OPENAI_API_KEY` dans l’environnement ou le `.env` chargé par uvicorn.
`STORYBOOK_GENERATION_TIMEOUT_SECONDS` vaut 180 par défaut. Le Writer autorise une
nouvelle tentative en cas de sortie invalide et au plus trois appels au modèle.
Cette validation de structure ne remplace pas la future relecture narrative.

Si Ollama est arrêté, si le modèle manque, ou si la génération dépasse le délai,
le serveur et l’interface démarrent quand même ; la génération affiche le message
d’erreur permettant de réessayer. Pour diagnostiquer, vérifier `ollama list` et
les journaux du serveur. Le délai est configurable pour les machines plus lentes.

Test réel facultatif, après téléchargement du modèle et démarrage d’Ollama :

```bash
cd backend
uv run pytest -m integration tests/test_ollama.py -v
```

Ce test appelle uniquement le modèle local par défaut et vérifie sa sortie typée ;
il est exclu des tests ordinaires et de la CI. Il ne mesure pas la qualité littéraire.

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

Les commandes de tests, lint, typage, couverture et audits sont regroupées dans
[CONTRIBUTING.md](CONTRIBUTING.md#vérifications-locales). Les tests ordinaires
utilisent des modèles déterministes et ne nécessitent aucun identifiant LLM.

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

Les règles de contribution, les contrôles GitHub et leur activation sont décrits
dans [CONTRIBUTING.md](CONTRIBUTING.md).

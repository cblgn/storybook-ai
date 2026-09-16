# Contribuer à Storybook AI

[README.md](README.md) présente le projet et son installation locale.
[SPEC.md](SPEC.md) définit les exigences produit ; [AGENTS.md](AGENTS.md) contient
les instructions permanentes des agents. Une **issue GitHub** décrit une unité de
travail et fait autorité pour son périmètre. Une **pull request** en porte
l’implémentation : normalement, une issue d’implémentation correspond à une PR.

Rédiger les titres, descriptions et mises à jour des issues **en anglais**, y
compris les exigences, critères d’acceptation et notes techniques, même si les
échanges ou l’interface sont en français. Conserver les identifiants de code et
les citations de l’interface dans leur langue d’origine.

## Parcours standard

1. Partir d’un `main` à jour : vérifier `git status`, préserver le travail local,
   puis utiliser `git switch main` et `git pull --ff-only`.
2. Sélectionner ou créer une issue GitHub. Décrire le contexte, l’objectif et les
   critères d’acceptation ; lier les sections pertinentes de `SPEC.md` sans les
   recopier. Expliciter tout conflit avec la spécification avant d’implémenter.
3. Créer une branche dédiée avec `git switch -c <branche>`, en incluant le numéro
   de l’issue dans son nom. Aucun développement directement sur `main`.
4. Implémenter le plus petit changement cohérent et ses tests utiles. Mettre à
   jour `SPEC.md` si les exigences produit changent explicitement ; réserver les
   [ADRs](docs/adr/README.md) aux décisions d’architecture significatives.
5. Exécuter les vérifications locales pertinentes ci-dessous et examiner les
   résultats. Les tests ordinaires restent déterministes, sans vrai LLM.
6. Relire `git status` et le diff complet, y compris les nouveaux fichiers.
   Ajouter uniquement les fichiers concernés puis commiter avec Conventional
   Commits.
7. Pousser la branche avec `git push -u origin <branche>`.
8. Créer une PR vers `main` avec le modèle fourni et `Closes #<issue>`.
   Expliquer le pourquoi, le résultat, les validations et les limites ; ajouter
   des captures pour les changements visuels. Lier aussi la PR depuis l’issue.
9. Attendre la réussite des checks GitHub requis : qualité, sécurité et CodeQL
   lorsque disponible. Corriger les défauts ; ne jamais contourner ni affaiblir
   CI, audits, typage, lint, couverture ou protection de branche pour faire passer
   une modification.
10. Relire le diff final et traiter les retours de revue. Tout changement après
    revue doit repasser les contrôles concernés.
11. Effectuer un **squash merge** vers `main`, avec un message Conventional Commit.
    Codex ne fusionne jamais une PR sans autorisation explicite de l’utilisateur.
    L’issue reste ouverte jusqu’à la fusion ; `Closes #<issue>` permet sa fermeture.
12. Laisser GitHub supprimer automatiquement la branche fusionnée via le réglage
    **Automatically delete head branches**. Repartir ensuite du `main` actualisé.

Exemples de branches :

```text
feat/12-story-writer
fix/18-story-duration
ci/23-codeql
docs/27-architecture
```

Exemples de commits et de titres de squash :

```text
feat: add story writer agent
fix: prevent duplicate generation
ci: add dependency audit
test: cover reviewer workflow
docs: document architecture
```

Préférer des PR indépendantes. Si une PR doit temporairement cibler une autre
branche de fonctionnalité, préciser la dépendance dans les deux issues/PRs.
Après squash merge de la précédente, réconcilier la branche dépendante avec
`main` sans réécrire l’historique publié, la recibler vers `main`, vérifier son diff
et relancer les checks. Les mots de fermeture d’issue ne sont interprétés que
pour une PR ciblant la branche par défaut. Ne pas fusionner dans la branche
intermédiaire pour contourner ce parcours.

## Vérifications locales

Backend, depuis `backend/` :

```bash
uv run pytest
uv run pytest --cov=src/storybook --cov-report=term-missing --cov-report=xml
uv run ruff check .
uv run mypy src
uv export --locked --all-groups --no-emit-project --format requirements-txt --output-file /tmp/storybook-audit.txt --quiet
uv run pip-audit --require-hashes --disable-pip -r /tmp/storybook-audit.txt
```

Frontend, depuis `frontend/` :

```bash
pnpm lint
pnpm typecheck
pnpm test
pnpm test:coverage
pnpm build
pnpm exec playwright install chromium
pnpm test:e2e
pnpm audit --audit-level=high
```

Installer Chromium une fois avant les tests navigateur ; libérer les ports 8000
et 5173. Playwright démarre Vite et FastAPI avec un `TestModel` PydanticAI et couvre
validation, génération, attente et reprise après erreur sur ordinateur et mobile.
Les tests de composants simulent la frontière HTTP. Les futurs tests de vrai
fournisseur portent le marqueur `integration`, exclu par défaut, et s’exécutent
explicitement avec `pytest -m integration` ; ils ne font pas partie de la CI normale.

La couverture backend doit rester à **80 % minimum**. Les rapports
`backend/coverage.xml` et `frontend/coverage/lcov.info` restent hors de Git.
Les audits incluent les dépendances verrouillées de production et de développement :
`pip-audit` échoue sur toute vulnérabilité connue ; `pnpm audit` sur les niveaux
élevé/critique. Aucun secret, `.env`, build, cache ou dépendance installée ne doit
être ajouté aux commits. Pour une modification uniquement documentaire, vérifier
les liens, les modèles et le diff ; expliquer les contrôles applicatifs non pertinents.

## Revue et contrôles GitHub

Les workflows de qualité, audits et CodeQL doivent réussir avant fusion. Le
ruleset `Protect main` impose une branche à jour, les conversations résolues et un
historique linéaire ; force pushes et suppression de `main` sont interdits.
Aucune approbation d’un second mainteneur n’est requise pour ce projet solo.

GitHub autorise uniquement le squash merge et supprime les branches fusionnées.
La politique Dependabot autorise l’auto-merge des versions mineures et patch, y
compris les groupes dont la mise à jour la plus importante reste mineure ou patch.
Les versions majeures, brouillons et métadonnées inconnues restent manuels. Tous
les contrôles et protections s’appliquent aussi aux fusions automatiques.
Cette politique ne donne pas à Codex l’autorisation de fusionner une autre PR.

Sonar analyse `main` après fusion et consomme les rapports de couverture. Son
résultat ne doit pas être présenté comme un check exécuté sur la PR lorsque le
workflow ne l’a pas analysée. Consulter les résultats GitHub/Sonar disponibles
et préciser toute limite dans la PR.

La [politique de sécurité du dépôt](docs/repository-security.md) décrit les checks
requis, les permissions et les paramètres maintenus. Pour une vérification en
lecture seule depuis une session `gh` de mainteneur authentifiée :

```bash
python3 scripts/verify_github_security.py
```

Un signalement de vulnérabilité suit [SECURITY.md](SECURITY.md), jamais une issue
publique. Pour les agents, [AGENTS.md](AGENTS.md#skills) oriente vers les procédures
d’implémentation et de durcissement ; ce guide reste le parcours des contributeurs.

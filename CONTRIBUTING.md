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
   Commits. Un agent ne crée de commit que sur demande explicite.
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

Les agents respectent les limites de publication données par l’utilisateur.
Si les opérations distantes sont interdites ou indisponibles, préparer localement
les descriptions nécessaires et signaler ce qui reste à publier.

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

## Contrôles et réglages GitHub

Les workflows existants utilisent Python 3.14, Node.js 24, pnpm et les lockfiles :

- `ci.yml` : qualité backend/frontend, couverture et tests navigateur.
- `security.yml` : audits sur les PR, les pushes vers `main`, chaque semaine et
  sur déclenchement manuel.
- `codeql.yml` : Python et JavaScript/TypeScript sur dépôt public ; pour un dépôt
  privé disposant de Code Security, activer `CODEQL_ENABLED=true`.
- `sonar.yml` : sources et couverture des deux projets, recalculées sur le commit
  analysé, uniquement sur `main`. Aucun artefact d’une PR n’est exécuté avec le secret.
- Dependabot : uv, npm/pnpm et Actions chaque semaine ; groupes mineurs/correctifs,
  mises à jour majeures séparées.

Les réglages suivants sont une procédure d’administration, pas une déclaration
qu’ils sont déjà activés. Les fichiers du dépôt ne configurent pas GitHub à eux seuls.

1. Dans **Settings → General → Pull Requests**, autoriser **squash merging**,
   désactiver les autres méthodes de fusion et activer **Automatically delete head
   branches**. Cela supprime la branche après fusion, sans autoriser d’auto-merge.
2. Protéger `main` : PR obligatoire, branche à jour, force pushes et suppression
   interdits ; exiger `Backend quality`, `Frontend quality`, `Browser integration`,
   `Backend dependency audit` et `Frontend dependency audit`. Ajouter
   `CodeQL (python)` et `CodeQL (javascript-typescript)` lorsque disponibles.
   Les noms deviennent visibles après une première exécution des workflows.
   Lors de l’initialisation, planifier l’activation des checks avec l’arrivée des
   workflows ; ne jamais désactiver une protection existante pour fusionner.
3. Activer les alertes et mises à jour de sécurité Dependabot. Conserver CodeQL
   en configuration avancée, sans activer en parallèle la configuration par défaut.
4. Importer le dépôt dans SonarQube Cloud et désactiver l’analyse automatique au
   profit de la CI. Remplacer les identifiants publics dans `sonar-project.properties`,
   ajouter le secret Actions `SONAR_TOKEN`, puis la variable `SONAR_ENABLED=true`.
   Garder l’analyse gratuite sur `main` après fusion, sans check Sonar obligatoire
   pour les PR. Ne jamais inscrire un jeton dans une issue ou dans Git.

Pour les artefacts historiques à conserver pendant la transition, suivre la
[note de migration temporaire](AGENTS.md#temporary-bootstrap-migration).

Références : [liaison issue–PR](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue),
[uv dans Actions](https://docs.astral.sh/uv/guides/integration/github/),
[Code Security](https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository),
[SonarQube Cloud dans Actions](https://docs.sonarsource.com/sonarcloud/advanced-setup/ci-based-analysis/github-actions-for-sonarcloud).

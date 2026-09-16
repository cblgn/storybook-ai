# Décisions d’architecture

Créer un ADR uniquement pour une décision architecturale significative : par
exemple un changement de stockage, de frontière entre composants ou d’orchestration
des agents. Les corrections ordinaires, choix de détail et comptes rendus de tâche
restent dans les issues et PR. Aucun ADR n’est nécessaire par défaut.

Utiliser `NNNN-titre-court.md` et documenter brièvement :

- statut et date : proposé, accepté ou remplacé ;
- contexte et contraintes, avec liens vers l’issue et `SPEC.md` ;
- options considérées et compromis ;
- décision et justification ;
- conséquences et lien vers la PR d’implémentation.

Faire relire l’ADR avec la PR concernée. Si une décision acceptée change, ajouter
un nouvel ADR qui référence et remplace l’ancien ; conserver la justification
historique. La spécification produit reste dans [SPEC.md](../../SPEC.md), le
parcours de contribution dans [CONTRIBUTING.md](../../CONTRIBUTING.md).

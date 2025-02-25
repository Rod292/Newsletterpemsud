# Newsletter PEM SUD - Arthur Loyd Bretagne

Ce projet contient tous les fichiers nécessaires pour la newsletter promotionnelle du projet immobilier PEM SUD à Saint-Brieuc.

## Contenu du projet

- `newsletter_pem_sud.html` - Le fichier HTML de la newsletter
- `newsletter_style.css` - Les styles CSS pour la newsletter
- `send_newsletter.py` - Script Python pour l'envoi automatique de la newsletter
- `clients_exemple.csv` - Exemple de fichier CSV contenant des données clients fictives
- `README.md` - Ce fichier d'instructions

## Structure de la newsletter

La newsletter a été conçue pour mettre en valeur le projet immobilier PEM SUD avec :

- Un design professionnel aux couleurs d'Arthur Loyd (rouge #e50019)
- Une mise en page claire et structurée
- Des sections informatives sur le projet (localisation, caractéristiques, disponibilité)
- Des éléments interactifs (questions, appels à l'action)
- Une carte Google Maps intégrée
- Des informations de contact

## Personnalisation de la newsletter

### Modifications du contenu

Pour modifier le contenu de la newsletter, ouvrez le fichier `newsletter_pem_sud.html` dans un éditeur de texte ou HTML et modifiez les textes selon vos besoins.

### Modifications du style

Pour modifier l'apparence de la newsletter, vous pouvez éditer le fichier `newsletter_style.css`.

### Ajout de variables de personnalisation

Le script d'envoi peut remplacer certaines variables dans le HTML par des informations spécifiques à chaque client. Pour ajouter des variables personnalisées :

1. Dans le fichier HTML, ajoutez des balises de type `{{NOM_VARIABLE}}` où vous souhaitez insérer des données personnalisées
2. Dans le script Python, ajoutez la logique pour remplacer ces variables dans la fonction `personalize_newsletter()`

## Images

Pour utiliser vos propres images :

1. Remplacez `project_image.jpg` par l'image du projet PEM SUD
2. Assurez-vous que le logo Arthur Loyd est disponible (actuellement chargé depuis une URL)
3. Si vous ajoutez d'autres images, mettez également à jour le script d'envoi

## Envoi de la newsletter

### Prérequis

- Python 3.6 ou supérieur
- Les modules Python suivants : `smtplib`, `email`, `argparse`, `csv`, `logging`

### Format du fichier CSV

Le fichier CSV des clients doit contenir au minimum une colonne `email`. Pour plus de personnalisation, ajoutez aussi les colonnes `nom`, `prenom` et `entreprise`.

### Test d'envoi

Pour tester l'envoi de la newsletter à une seule adresse email :

```bash
python send_newsletter.py --csv clients_exemple.csv --template newsletter_pem_sud.html --email votre_email@example.com --password votre_mot_de_passe --test --test-email destinataire@example.com
```

### Envoi à tous les clients

Pour envoyer la newsletter à tous les clients listés dans le fichier CSV :

```bash
python send_newsletter.py --csv clients_exemple.csv --template newsletter_pem_sud.html --email votre_email@example.com --password votre_mot_de_passe
```

### Options du script

- `--csv` : Chemin vers le fichier CSV contenant les clients (obligatoire)
- `--template` : Chemin vers le template HTML de la newsletter (obligatoire)
- `--email` : Email de l'expéditeur (obligatoire)
- `--password` : Mot de passe de l'email de l'expéditeur (obligatoire)
- `--smtp` : Serveur SMTP (par défaut: smtp.gmail.com)
- `--port` : Port SMTP (par défaut: 587)
- `--test` : Mode test (envoi à une seule adresse)
- `--test-email` : Email pour le test

## Journalisation

Le script génère un fichier de log avec la date du jour (`newsletter_sending_AAAAMMJJ.log`) qui contient des informations sur le déroulement de l'envoi.

## Sécurité

Ne partagez jamais vos identifiants email dans des fichiers ou des dépôts publics. Pour une utilisation en production, considérez l'utilisation de variables d'environnement ou d'un fichier de configuration sécurisé.

## Compatibilité avec les clients de messagerie

La newsletter a été conçue pour être compatible avec la plupart des clients de messagerie modernes, mais certaines fonctionnalités CSS avancées peuvent ne pas être supportées par tous les clients. Un test d'envoi est recommandé avant l'envoi en masse.

---

© 2025 Arthur Loyd Bretagne. Tous droits réservés. 
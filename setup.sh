#!/bin/bash
# Script d'installation pour la newsletter PEM SUD
# Arthur Loyd Bretagne

echo "===== Configuration de l'environnement pour la newsletter PEM SUD ====="

# Vérification de Python
echo "Vérification de l'installation Python..."
if command -v python3 &>/dev/null; then
    PYTHON="python3"
    echo "Python 3 trouvé."
elif command -v python &>/dev/null; then
    PYTHON="python"
    echo "Python trouvé."
else
    echo "Python n'est pas installé. Veuillez installer Python 3.6 ou supérieur."
    exit 1
fi

# Vérification de la version de Python
VERSION=$($PYTHON -c 'import sys; print(sys.version_info.major, sys.version_info.minor)')
read -r MAJOR MINOR <<< "$VERSION"

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 6 ]); then
    echo "Python 3.6 ou supérieur est recommandé. Version actuelle: $MAJOR.$MINOR"
    read -p "Continuer quand même? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Création d'un environnement virtuel (optionnel)
echo "Souhaitez-vous créer un environnement virtuel pour ce projet?"
read -p "(Recommandé pour isoler les dépendances) (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Création de l'environnement virtuel..."
    $PYTHON -m venv newsletter_env
    
    if [ -d "newsletter_env" ]; then
        echo "Environnement virtuel créé avec succès."
        
        # Activation de l'environnement virtuel
        if [ -f "newsletter_env/bin/activate" ]; then
            source newsletter_env/bin/activate
            echo "Environnement virtuel activé."
        else
            echo "Impossible d'activer l'environnement virtuel. Veuillez l'activer manuellement."
        fi
    else
        echo "Erreur lors de la création de l'environnement virtuel. Installation dans l'environnement global."
    fi
fi

# Installation des dépendances
echo "Installation des dépendances..."
$PYTHON -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "Installation des dépendances réussie."
else
    echo "Erreur lors de l'installation des dépendances."
    exit 1
fi

# Création du dossier pour les images si nécessaire
if [ ! -d "images" ]; then
    mkdir -p images
    echo "Dossier 'images' créé."
    echo "Veuillez placer l'image du projet (project_image.jpg) dans ce dossier."
fi

# Instructions pour l'utilisation
echo
echo "===== Installation terminée ====="
echo
echo "Pour utiliser la newsletter, suivez ces étapes:"
echo "1. Placez votre image du projet dans le dossier 'images'"
echo "2. Modifiez le fichier CSV des clients selon vos besoins"
echo "3. Pour tester l'envoi, exécutez:"
echo "   $PYTHON send_newsletter.py --csv clients_exemple.csv --template newsletter_pem_sud.html --email votre_email@example.com --password votre_mot_de_passe --test --test-email test@example.com"
echo
echo "Pour plus d'informations, consultez le fichier README.md"
echo

# Fin du script
echo "Configuration terminée avec succès!" 
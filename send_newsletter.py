#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script d'envoi de newsletter pour Arthur Loyd Bretagne
Ce script permet d'envoyer la newsletter PEM SUD aux clients
"""

import os
import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
import csv
import logging
from datetime import datetime
import io

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=f'newsletter_sending_{datetime.now().strftime("%Y%m%d")}.log'
)

def read_html_template(file_path):
    """Lit le template HTML de la newsletter"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        logging.error(f"Erreur lors de la lecture du template HTML: {e}")
        return None

def read_clients_from_csv(csv_path):
    """Lit les clients depuis un fichier CSV"""
    clients = []
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as file:  # utf-8-sig gère le BOM
            csv_reader = csv.DictReader(file, delimiter=';')
            for row in csv_reader:
                # Nettoyer les clés et les valeurs
                cleaned_row = {k.strip(): v.strip() for k, v in row.items() if k and v}
                if cleaned_row:  # Ajouter seulement si la ligne n'est pas vide
                    clients.append(cleaned_row)
        return clients
    except Exception as e:
        logging.error(f"Erreur lors de la lecture du fichier CSV: {e}")
        return []

def personalize_newsletter(html_template, client_data):
    """Personnalise la newsletter pour chaque client"""
    personalized_html = html_template
    
    # Personnalisation du contenu pour chaque client
    if 'Nom' in client_data and client_data['Nom']:
        personalized_html = personalized_html.replace('{{NOM_CLIENT}}', client_data['Nom'])
    else:
        personalized_html = personalized_html.replace('{{NOM_CLIENT}}', 'Cher client')
    
    # Autres personnalisations selon les données du client
    if 'Entreprise' in client_data and client_data['Entreprise']:
        personalized_html = personalized_html.replace('{{ENTREPRISE}}', client_data['Entreprise'])
    else:
        personalized_html = personalized_html.replace('{{ENTREPRISE}}', '')
    
    return personalized_html

def send_email(sender_email, sender_password, recipient_email, html_content, smtp_server, smtp_port, images=None):
    """Envoie l'email avec la newsletter HTML"""
    try:
        # Création du message
        msg = MIMEMultipart('related')
        msg['Subject'] = Header("🏢 Saint-Brieuc : Bureaux neufs à partir de 182m² - PEM SUD", 'utf-8')
        msg['From'] = f"Arthur Loyd Bretagne <{sender_email}>"
        msg['To'] = recipient_email
        
        # Partie HTML avec preview text
        html_part = MIMEMultipart('alternative')
        preview_text = "<div style='display:none;max-height:0px;overflow:hidden'>Découvrez des espaces de travail modernes et écologiques au coeur du nouveau projet PEM SUD à Saint Brieuc</div>"
        html_content_with_preview = preview_text + html_content
        html_part.attach(MIMEText(html_content_with_preview, 'html', 'utf-8'))
        msg.attach(html_part)
        
        # Ajout des images intégrées avec meilleure compatibilité pour Apple Mail
        if images:
            for img_id, img_path in images.items():
                try:
                    with open(img_path, 'rb') as img_file:
                        img = MIMEImage(img_file.read())
                        img.add_header('Content-ID', f'<{img_id}>')
                        # Ajouter l'en-tête Content-Disposition pour s'assurer que les images s'affichent correctement
                        img.add_header('Content-Disposition', 'inline', filename=os.path.basename(img_path))
                        # Ajouter l'en-tête Content-Location pour améliorer la compatibilité
                        img.add_header('Content-Location', img_id)
                        # Ajouter X-Attachment-Id pour améliorer la compatibilité avec Apple Mail
                        img.add_header('X-Attachment-Id', img_id)
                        msg.attach(img)
                except Exception as e:
                    logging.warning(f"Impossible d'attacher l'image {img_path}: {e}")
        
        # Connexion au serveur SMTP et envoi
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        logging.info(f"Email envoyé avec succès à {recipient_email}")
        return True
    
    except Exception as e:
        logging.error(f"Erreur lors de l'envoi de l'email à {recipient_email}: {e}")
        return False

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Envoi de la newsletter PEM SUD d'Arthur Loyd Bretagne")
    parser.add_argument('--csv', required=True, help='Chemin vers le fichier CSV contenant les clients')
    parser.add_argument('--template', required=True, help='Chemin vers le template HTML de la newsletter')
    parser.add_argument('--email', required=True, help='Email de l\'expéditeur')
    parser.add_argument('--password', required=True, help='Mot de passe de l\'email de l\'expéditeur')
    parser.add_argument('--smtp', default='smtp.gmail.com', help='Serveur SMTP')
    parser.add_argument('--port', type=int, default=587, help='Port SMTP')
    parser.add_argument('--test', action='store_true', help='Mode test (envoi à une seule adresse)')
    parser.add_argument('--test-email', help='Email pour le test')
    
    args = parser.parse_args()
    
    # Lecture du template HTML
    html_template = read_html_template(args.template)
    if not html_template:
        logging.error("Impossible de lire le template HTML. Arrêt du programme.")
        return
    
    # Lecture des clients
    clients = read_clients_from_csv(args.csv)
    if not clients:
        logging.error("Aucun client trouvé dans le fichier CSV. Arrêt du programme.")
        return
    
    # Images à inclure dans l'email
    images = {
        'logo': 'Logo Arthur Loyd.png',
        'project_photo_1': 'Project photo 1.png',
        'project_photo_2': 'Project Photo 2.png',
        'project_photo_3': 'Project photo 3.png'
    }
    
    # Mode test
    if args.test:
        if not args.test_email:
            logging.error("Email de test non spécifié. Utilisez --test-email pour spécifier l'adresse de test.")
            return
        
        # Chercher les informations du client test dans le CSV
        test_client = None
        for client in clients:
            if client['Email'].lower() == args.test_email.lower():
                test_client = client
                break
        
        if not test_client:
            logging.warning(f"Email de test non trouvé dans le CSV, utilisation des données de test par défaut")
            test_client = {'Email': args.test_email, 'Nom': 'Client Test', 'Entreprise': 'Entreprise Test'}
        
        personalized_html = personalize_newsletter(html_template, test_client)
        success = send_email(args.email, args.password, args.test_email, personalized_html, args.smtp, args.port, images)
        
        if success:
            print(f"Email de test envoyé avec succès à {args.test_email}")
        else:
            print(f"Échec de l'envoi de l'email de test à {args.test_email}")
        
        return
    
    # Envoi à tous les clients
    successful = 0
    failed = 0
    
    for client in clients:
        if 'Email' not in client or not client['Email']:
            logging.warning(f"Client sans email: {client}")
            continue
        
        personalized_html = personalize_newsletter(html_template, client)
        success = send_email(args.email, args.password, client['Email'], personalized_html, args.smtp, args.port, images)
        
        if success:
            successful += 1
        else:
            failed += 1
    
    logging.info(f"Envoi terminé. {successful} emails envoyés avec succès, {failed} échecs.")
    print(f"Envoi terminé. {successful} emails envoyés avec succès, {failed} échecs.")

if __name__ == "__main__":
    main() 
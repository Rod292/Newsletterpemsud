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
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                clients.append(row)
        return clients
    except Exception as e:
        logging.error(f"Erreur lors de la lecture du fichier CSV: {e}")
        return []

def personalize_newsletter(html_template, client_data):
    """Personnalise la newsletter pour chaque client"""
    personalized_html = html_template
    
    # Personnalisation du contenu pour chaque client
    if 'nom' in client_data and client_data['nom']:
        personalized_html = personalized_html.replace('{{NOM_CLIENT}}', client_data['nom'])
    else:
        personalized_html = personalized_html.replace('{{NOM_CLIENT}}', 'Cher client')
    
    # Autres personnalisations selon les données du client
    if 'entreprise' in client_data and client_data['entreprise']:
        personalized_html = personalized_html.replace('{{ENTREPRISE}}', client_data['entreprise'])
    else:
        personalized_html = personalized_html.replace('{{ENTREPRISE}}', '')
    
    return personalized_html

def send_email(sender_email, sender_password, recipient_email, subject, html_content, smtp_server, smtp_port, images=None):
    """Envoie l'email avec la newsletter HTML"""
    try:
        # Création du message
        msg = MIMEMultipart('related')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = sender_email
        msg['To'] = recipient_email
        
        # Partie HTML
        html_part = MIMEMultipart('alternative')
        html_part.attach(MIMEText(html_content, 'html', 'utf-8'))
        msg.attach(html_part)
        
        # Ajout des images intégrées
        if images:
            for img_id, img_path in images.items():
                try:
                    with open(img_path, 'rb') as img_file:
                        img = MIMEImage(img_file.read())
                        img.add_header('Content-ID', f'<{img_id}>')
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
        'logo': 'logo.png',
        'project_image': 'project_image.jpg'
    }
    
    # Sujet de l'email
    subject = "Imaginez votre entreprise au cœur d'un quartier dynamique et écologique à Saint-Brieuc !"
    
    # Mode test
    if args.test:
        if not args.test_email:
            logging.error("Email de test non spécifié. Utilisez --test-email pour spécifier l'adresse de test.")
            return
        
        test_client = {'email': args.test_email, 'nom': 'Client Test', 'entreprise': 'Entreprise Test'}
        personalized_html = personalize_newsletter(html_template, test_client)
        success = send_email(args.email, args.password, args.test_email, subject, personalized_html, args.smtp, args.port, images)
        
        if success:
            print(f"Email de test envoyé avec succès à {args.test_email}")
        else:
            print(f"Échec de l'envoi de l'email de test à {args.test_email}")
        
        return
    
    # Envoi à tous les clients
    successful = 0
    failed = 0
    
    for client in clients:
        if 'email' not in client or not client['email']:
            logging.warning(f"Client sans email: {client}")
            continue
        
        personalized_html = personalize_newsletter(html_template, client)
        success = send_email(args.email, args.password, client['email'], subject, personalized_html, args.smtp, args.port, images)
        
        if success:
            successful += 1
        else:
            failed += 1
    
    logging.info(f"Envoi terminé. {successful} emails envoyés avec succès, {failed} échecs.")
    print(f"Envoi terminé. {successful} emails envoyés avec succès, {failed} échecs.")

if __name__ == "__main__":
    main() 
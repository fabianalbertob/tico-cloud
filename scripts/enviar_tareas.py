import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

def enviar_tareas():
    archivo = 'tareas/pendientes.txt'
    hora = datetime.now().strftime("%H:%M")
    
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            tareas = f.read().strip()
        cuerpo = "Tus tareas pendientes:\n\n" + tareas if tareas else "No hay tareas"
    else:
        cuerpo = "No se encontraron tareas"
    
    cuerpo += "\n\n--- TICO - " + hora + "hs"
    
    msg = MIMEText(cuerpo)
    msg['Subject'] = "Tareas Diarias - " + hora + "hs"
    msg['From'] = os.environ['GMAIL_USER']
    msg['To'] = os.environ['DEST_EMAIL']
    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(os.environ['GMAIL_USER'], os.environ['GMAIL_PASSWORD'])
    server.send_message(msg)
    server.quit()
    print("Tareas enviadas - " + hora + "hs")

if __name__ == '__main__':
    enviar_tareas()

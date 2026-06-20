import imaplib
import email
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

def revisar_mail():
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(os.environ['GMAIL_USER'], os.environ['GMAIL_PASSWORD'])
        mail.select('inbox')
        status, messages = mail.search(None, 'UNSEEN')
        mail_ids = messages[0].split()
        
        if not mail_ids:
            print("No hay mails nuevos")
            return
        
        resumen = "RESUMEN DE CORREOS - " + datetime.now().strftime('%d/%m/%Y %H:%M') + "\n\n"
        resumen += "Tienes " + str(len(mail_ids)) + " mail(s) nuevo(s).\n\n"
        
        for mail_id in mail_ids[-10:]:
            status, msg_data = mail.fetch(mail_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            resumen += "De: " + str(msg['from']) + "\n"
            resumen += "Asunto: " + str(msg['subject']) + "\n\n"
        
        mail.close()
        mail.logout()
        enviar_email("Resumen de Mails - TICO", resumen)
        
    except Exception as e:
        print("Error: " + str(e))

def enviar_email(asunto, cuerpo):
    msg = MIMEText(cuerpo)
    msg['Subject'] = asunto
    msg['From'] = os.environ['GMAIL_USER']
    msg['To'] = os.environ['DEST_EMAIL']
    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(os.environ['GMAIL_USER'], os.environ['GMAIL_PASSWORD'])
    server.send_message(msg)
    server.quit()
    print("Email enviado")

if __name__ == '__main__':
    revisar_mail()

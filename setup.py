from pathlib import Path

print("🚀 Configurando TICO Cloud...")

base = Path(".")

# Crear carpetas
carpetas = [".github/workflows", "scripts", "tareas"]
for carpeta in carpetas:
    (base / carpeta).mkdir(parents=True, exist_ok=True)
    print(f"✅ Carpeta: {carpeta}")

# Archivo 1: revisar-mail.yml
revisar_mail = """name: Revisar Mail

on:
  schedule:
    - cron: '0 11 * * *'
    - cron: '0 21 * * *'

jobs:
  revisar-mail:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Instalar dependencias
      run: pip install imaplib2 email
    
    - name: Revisar mail
      env:
        GMAIL_USER: ${{ secrets.GMAIL_USER }}
        GMAIL_PASSWORD: ${{ secrets.GMAIL_PASSWORD }}
        DEST_EMAIL: ${{ secrets.DEST_EMAIL }}
      run: python scripts/revisar_mail.py
"""

(base / ".github/workflows/revisar-mail.yml").write_text(revisar_mail, encoding="utf-8")
print("✅ .github/workflows/revisar-mail.yml")

# Archivo 2: tareas-diarias.yml
tareas_diarias = """name: Tareas Diarias

on:
  schedule:
    - cron: '0 12 * * *'
    - cron: '0 15 * * *'
    - cron: '0 20 * * *'

jobs:
  enviar-tareas:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Enviar tareas
      env:
        GMAIL_USER: ${{ secrets.GMAIL_USER }}
        GMAIL_PASSWORD: ${{ secrets.GMAIL_PASSWORD }}
        DEST_EMAIL: ${{ secrets.DEST_EMAIL }}
      run: python scripts/enviar_tareas.py
"""

(base / ".github/workflows/tareas-diarias.yml").write_text(tareas_diarias, encoding="utf-8")
print("✅ .github/workflows/tareas-diarias.yml")

# Archivo 3: revisar_mail.py
revisar_py = '''import imaplib
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
        
        resumen = "RESUMEN DE CORREOS - " + datetime.now().strftime('%d/%m/%Y %H:%M') + "\\n\\n"
        resumen += "Tienes " + str(len(mail_ids)) + " mail(s) nuevo(s).\\n\\n"
        
        for mail_id in mail_ids[-10:]:
            status, msg_data = mail.fetch(mail_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            resumen += "De: " + str(msg['from']) + "\\n"
            resumen += "Asunto: " + str(msg['subject']) + "\\n\\n"
        
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
'''

(base / "scripts/revisar_mail.py").write_text(revisar_py, encoding="utf-8")
print("✅ scripts/revisar_mail.py")

# Archivo 4: enviar_tareas.py
enviar_py = '''import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

def enviar_tareas():
    archivo = 'tareas/pendientes.txt'
    hora = datetime.now().strftime("%H:%M")
    
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            tareas = f.read().strip()
        cuerpo = "Tus tareas pendientes:\\n\\n" + tareas if tareas else "No hay tareas"
    else:
        cuerpo = "No se encontraron tareas"
    
    cuerpo += "\\n\\n--- TICO - " + hora + "hs"
    
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
'''

(base / "scripts/enviar_tareas.py").write_text(enviar_py, encoding="utf-8")
print("✅ scripts/enviar_tareas.py")

# Archivo 5: pendientes.txt
pendientes = """📌 TAREAS DEL DÍA
==================

☐ Revisar estudios de pacientes
☐ Actualizar historias clínicas
☐ Llamar a pacientes pendientes

---
💡 Editá este archivo o usá TICO para agregar tareas
"""

(base / "tareas/pendientes.txt").write_text(pendientes, encoding="utf-8")
print("✅ tareas/pendientes.txt")

# Archivo 6: README.md
readme = """# TICO Cloud

Sistema de tareas programadas y revisión de mail.

## Horarios (Argentina UTC-3)
- Revisar mail: 8:00 y 18:00 hs
- Enviar tareas: 9:00, 12:00 y 17:00 hs

## Secrets configurados en GitHub
- GMAIL_USER
- GMAIL_PASSWORD
- DEST_EMAIL
"""

(base / "README.md").write_text(readme, encoding="utf-8")
print("✅ README.md")

print("\\n🎉 ¡TICO Cloud configurado!")
print("\\n📋 Próximos pasos:")
print("1. git init")
print("2. git add .")
print("3. git commit -m 'Configuración inicial'")
print("4. git branch -M main")
print("5. git remote add origin https://github.com/fabianalbertob/tico-cloud.git")
print("6. git push -u origin main")
import re
from email.message import EmailMessage
import smtplib
from openpyxl import Workbook
from bs4 import BeautifulSoup

enviar_email = True

book = Workbook()
sheet = book.active


def start_scrape(subject:str, content:str, login:str, password='', emailsManual=[], page=''):
    emails = []
    try:
      scrape = BeautifulSoup(page, 'html.parser')
      scrape = scrape.get_text()
      emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}", scrape))
    except:
      print("Não foi possível obter os e-mails do link fornecido.")

    contentSignature = content + """\n
Este é um e-mail automático, favor não responder.    
Bot para envio de e-mails criado por Matheus e Arthur.
github.com/matheusAparicio
github.com/ArthurErn"""

    email_list = list(emails)
    for item in emailsManual:
        email_list.insert(0, item)
       
    if enviar_email:
      for row in zip(email_list):
            
            sheet.append(row)
            msg = EmailMessage()
            msg['Subject'] = subject
            msg.set_content(contentSignature)
            msg['From'] = login
            msg['To'] = row[0]
            print(row[0])
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
              smtp.login(login, password)
              smtp.auth_login()
              smtp.send_message(msg)
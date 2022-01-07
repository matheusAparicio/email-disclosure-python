import re
from email.message import EmailMessage
import smtplib
from openpyxl import Workbook
from bs4 import BeautifulSoup
from segredo import EMAIL_ADRESS, EMAIL_PASSWORD


enviar_email = True

book = Workbook()
sheet = book.active


def start_scrape(subject:str, content:str, sender:str, page=''):
    
    scrape = BeautifulSoup(page, 'html.parser')
    scrape = scrape.get_text()
  
    emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}", scrape))
    email_list = list(emails)
       
    if enviar_email:
      for row in zip(email_list):
            
            sheet.append(row)
            msg = EmailMessage()
            msg['Subject'] = subject
            msg.set_content(content)
            msg['From'] = EMAIL_ADRESS
            msg['To'] = row[0]
            print(row[0])
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
              smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)
              smtp.auth_login()
              smtp.send_message(msg)
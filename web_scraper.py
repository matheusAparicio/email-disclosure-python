

import re
from urllib.request import urlopen, Request
import os
from datetime import datetime
from email.message import EmailMessage
import smtplib
from openpyxl import Workbook
from bs4 import BeautifulSoup
from segredo import EMAIL_ADRESS, EMAIL_PASSWORD


enviar_email = True

book = Workbook()
sheet = book.active


def start_scrape(page):
       
    scrape = BeautifulSoup(page, 'html.parser')
    scrape = scrape.get_text()
  
    emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}", scrape))
    email_list = list(emails)
       
    if enviar_email:
      for row in zip(email_list):
            
            sheet.append(row)
            msg = EmailMessage()
            msg['Subject'] = 'Olá'
            msg.set_content('testando um bot de python com webscraping')
            msg['From'] = EMAIL_ADRESS
            msg['To'] = row[0]
            print(row[0])
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
              smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)
              smtp.auth_login()
              smtp.send_message(msg)
      
        
def main():

    webpage = input("Cole o link para fazer webscraping de emails: ")

    try:
        page = urlopen(webpage) 
        start_scrape(page)
    except:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(webpage, headers=hdr)
        page = urlopen(req)
        start_scrape(page)

if __name__ == "__main__":
    main()

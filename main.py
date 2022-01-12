from web_scraper import start_scrape
from urllib.request import urlopen, Request
from cryptography.fernet import Fernet
from getBoolByString import getBoolByString
from getStringByBool import getStringByBool

def main():

    commandManual = False
    commandWebScraping = False
    commandFileScraping = False
    certain = 'N'
    login = ""
    password = ""
    saveLogin = 'N'
    subject = ""
    content = ""
    emailCurrent = ""
    emails = []
    webpage = ""
    try:
        with open('key.txt', 'rb') as f:
            key = f.readline()
    except FileNotFoundError:
        with open('key.txt', 'wb') as f:
            key = Fernet.generate_key()
            f.write(key)
    fernet = Fernet(key)

    print("Bem vinda(o) ao nosso sistema! Digite o número da opção desejada e tecle enter.\n\n")

    while(certain != 'S' and certain != 's'):
        
        print("Digite 's' para sim e 'n' para não nas seguintes perguntas. (Uma não anula a outra.)")
    
        commandManual = getBoolByString(input("Você digitará manualmente os e-mails para o qual enviará mensagens?: "))
        commandWebScraping = getBoolByString(input("Você irá adquirir e-mails de algum site através de webscraping?: "))
        commandFileScraping = getBoolByString(input("Você irá adquirir e-mails de algum arquivo através de webscraping?: "))

        print(f"""
Digitar e-mails manualmente: {getStringByBool(commandManual)}
Digitar site para webscraping de e-mails: {getStringByBool(commandWebScraping)}
Digitar caminho de arquivo para scraping de e-mails: {getStringByBool(commandFileScraping)}""")

        certain = input("Você tem certeza de suas escolhas?: ")
    
    try:
        with open('segredo.txt', 'rb') as f:
            lines = f.readlines()
            login = fernet.decrypt(lines[0]).decode()
            password = fernet.decrypt(lines[1]).decode()
    except FileNotFoundError:
        login = input("Digite o e-mail remetente: ")
        password = input("Digite a senha do e-mail remetente: ")
        saveLogin = input("Deseja salvar as informações de login? (S/N): ")
        if (saveLogin == 's' or saveLogin == 'S'):
            with open('segredo.txt', 'wb') as f:
                f.write(fernet.encrypt(login.encode()))
                line = "\n"
                f.write(line.encode('utf-8'))
                f.write(fernet.encrypt(password.encode()))

    subject = input("Digite o assunto dos e-mails: ")
    content = input("Digite o conteúdo dos e-mails:\n")

    if (commandManual):
        while (emailCurrent != "" or len(emails) == 0):
            emailCurrent = input(f"Digite o e-mail {len(emails)+1}: ")
            if emailCurrent != "":
                emails.append(emailCurrent)

    if (commandWebScraping):
        webpage = input("Cole o link para fazer webscraping de emails: ")

    try:
        if (webpage != ""):
            page = urlopen(webpage)
        start_scrape(subject, content, login, password, emailsManual=emails, page=page)
    except:
        if commandWebScraping:
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = Request(webpage, headers=hdr)
            page = urlopen(req)
            start_scrape(subject, content, login, password, emailsManual=emails, page=page)
        print("caiu no except")

if __name__ == "__main__":
    main()
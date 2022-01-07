from web_scraper import start_scrape
from urllib.request import urlopen, Request
from cryptography.fernet import Fernet

def main():

    command = 0
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

    print("Bem vinda(o) ao nosso sistema! Digite o número da opção desejada e tecle enter.")

    while(command != 1 and command != 2 and command != 3 or (certain != 'S' and certain != 's')):
        command = int(input("""
    1: Você digita manualmente os e-mails para o qual quer enviar mensagens.
    2: Você digita um site onde será feito webscrapping para obter os e-mails do qual serão enviadas as mensagens.
    3: Você adiciona e-mails manualmente e indica um site para mais e-mails a serem obtidos.
    Comando: """))

        if (command == 1):
            certain = input("Você escolheu a opção 1: Adicionar e-mails manualmente.\nTem certeza? (S/N): ")
        elif (command == 2):
            certain = input("Você escolheu a opção 2: Adicionar e-mails automaticamente.\nTem certeza? (S/N): ")
        elif (command == 3):
            certain = input("Você escolheu a opção 3: Adicionar e-mails manualmente e automaticamente.\nTem certeza? (S/N): ")
        else:
            print("Comando não reconhecido.")
    
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

    if (command == 1 or command == 3):
        emailCurrent = input("Digite o e-mail 1: ")
        emails.append(emailCurrent)
        while (emailCurrent != ""):
            emailCurrent = input(f"Digite o e-mail {len(emails)+1}: ")
            if emailCurrent != "":
                emails.append(emailCurrent)

    if (command == 2 or command == 3):
        webpage = input("Cole o link para fazer webscraping de emails: ")

    try:
        if command == 1:
            start_scrape(subject, content, login, password, emailsManual=emails)
        elif command == 2:
            page = urlopen(webpage)
            start_scrape(subject, content, login, password, page=page)
        else:
            page = urlopen(webpage)
            start_scrape(subject, content, login, password, emailsManual=emails, page=page)
    except:
        if command != 1:
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = Request(webpage, headers=hdr)
            page = urlopen(req)
            start_scrape(subject, content, login, password, emailsManual=emails, page=page)
        print("caiu no except")

if __name__ == "__main__":
    main()
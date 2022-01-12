def getBoolByString(value: str):
    if (value == 'S' or value == 's'):
        return True
    elif (value == 'N' or value == 'n'):
        return False
    else:
        print("Comando não reconhecido.")
        getBoolByString(input("Digite o comando novamente. (S/N): "))
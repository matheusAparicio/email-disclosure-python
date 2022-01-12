def getStringByBool(value: bool):
    if (value == True):
        return "Sim"
    elif (value == False):
        return "Não"
    else:
        return "Erro: não foi possível obter o valor booleano."
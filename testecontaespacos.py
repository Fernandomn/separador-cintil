
entrada = input ("Digite a frase de entrada")

numSpaces = 0
for i in range(len(entrada)):
    if entrada[i] != ' ':
        numSpaces +=1
    else:
        print(numSpaces)
        numSpaces = 0
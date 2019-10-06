import settings



def reconstroiArvore(frase, indice, lista):
    i = 0
    while i < len(frase):
        caracter = frase[i]
        if caracter == '(':
            novoIndice, listaProv = reconstroiArvore(frase[i + 1:], i + 1, [])
            i = novoIndice + 1
            lista.append(listaProv)
        elif caracter == ')':
            if (frase[:i].find(' ') >= 0):
                # recupera a classe, verificando char a char se é uma palavra
                classe = ''.join(c for c in frase.split(' ')[0] if c.isalpha() or c == '_')
                palavra = frase[:i].split(' ')[1]
            else:
                # refazer. simbolos nem sempre precisam de uma classe distinta. e essa não é a melhor forma de achar um simbolo
                palavra = frase[:i]
                classe = palavra
            if len(lista) > 0:
                return i + indice, [classe, lista]
            else:
                return i + indice, [classe, palavra]
        elif caracter in settings.pointList:  # or caracter + frase[i + 1] in settings.pointList:
            lista.append([caracter]) if not (caracter == '"' or caracter == "'") else lista.append(
                [caracter + caracter])
            return i + indice + 1, lista
        else:
            i += 1
    return i, lista[0]


def verificaCasosCONJ(arvore):
    if arvore[0] in settings.pointList:
        return
    if arvore[0] == settings.conjBarTag:  # or arvore[0] == settings.conjPTag:

        for filho in arvore[1]:

            if filho[0] == settings.conjTag:
                indice = arvore[1].index(filho)
                palavra = filho[1]
                arvore[1].remove(filho)
                arvore[1].insert(indice, palavra)

        arvore = arvore[1]

    numFilhos = len(arvore[1]) if type(arvore) is list and len(arvore) > 1 and type(arvore[1]) is list else 0

    if numFilhos > 0:
        for i in range(numFilhos):
            verificaCasosCONJ(arvore[1][i])
            if settings.removeTag in arvore[1][i][0]:
                arvore[1] = arvore[1] + arvore[1][i][1]
                arvore[1].remove(arvore[1][i])
        if settings.conjPTag in arvore[0] and type(arvore[0]) == str:  # se um dos filhos é uma conjunção
            children = arvore[1]
            for child in children:
                if child[0] == settings.conjBarTag:
                    child[0] = settings.conjPTag
            arvore[0] = settings.removeTag
    else:
        return


def imprimeArvore(arvore, nivel, wordLevelTag):
    classe = arvore[0]
    espacoEsquerda = ''.join('  ' for n in range(nivel))

    if len(arvore) > 1:
        # caso não seja um nó folha
        if type(arvore[1]) is list:
            if wordLevelTag in classe:
                # stringRetorno = '{0}{1}'.format(espacoEsquerda, arvore[1])
                lPalavras = ' '.join(filho for filho in arvore[1])

                if classe == settings.conjPTag :
                    # palavra = treeText[inicio: inicio + treeText[inicio:].index(')')].split()[1].lower()
                    if not lPalavras in settings.conjList2:
                        settings.conjList2.append(lPalavras)

                stringRetorno = '{0}({1} {2})\n'.format(
                    espacoEsquerda, classe, lPalavras)
            else:
                stringRetorno = '{0}({1} \n'.format(espacoEsquerda, classe)

                filhos = ''.join(imprimeArvore(filho, nivel + 1, wordLevelTag) for filho in arvore[1])
                stringRetorno += filhos

                stringRetorno += '{0})\n'.format(espacoEsquerda)
        else: #nós folha
            if classe.isalpha():

                if classe == settings.conjTag:
                    # palavra = treeText[inicio: inicio + treeText[inicio:].index(')')].split()[1].lower()
                    if not arvore[1] in settings.conjList2:
                        settings.conjList2.append(arvore[1])
                # else:
                stringRetorno = '{0}({1} {2})\n'.format(
                    espacoEsquerda, classe, arvore[1])
            else:
                stringRetorno = '{0}({1})\n'.format(espacoEsquerda, classe)
    else:
        if type(arvore) is str:
            stringRetorno = '{0}{1}'.format(espacoEsquerda, arvore)
        elif type(arvore) is list:
            stringRetorno = '{0}{1}'.format(espacoEsquerda, arvore[0])

    return stringRetorno

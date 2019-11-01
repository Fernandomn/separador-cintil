import settings


def reconstroiArvore(frase, indice, lista):
    i = 0
    while i < len(frase):
        caracter = frase[i]
        if caracter == '(':
            novoIndice, listaProv = reconstroiArvore(frase[i + 1:], i + 1, [])

            i = novoIndice + 1

            # if type(listaProv[0]) is list:
            #     for item in listaProv:
            #         lista.append(item)
            # else:
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
            # método antigo. inseria o pnt ao final da lista. faz sentido para o cintil, mas não para o ptb
            lista.append(caracter) if not (caracter == '"' or caracter == "'") else lista.append(
                caracter + caracter)
            return i + indice + 1, lista
        else:
            i += 1
    return i, lista[0]


def consertaConj(arvore):
    for filho in arvore[1]:
        # if filho[0] == settings.conjTag:
        indice = arvore[1].index(filho)
        palavra = filho[1]
        arvore[1].remove(filho)
        arvore[1].insert(indice, palavra)
    return arvore[1]


def consertaC(arvore):
    for filho in arvore[1]:
        # if filho[0] == settings.CTag:
        indice = arvore[1].index(filho)
        palavra = filho[1]
        arvore[1].remove(filho)
        arvore[1].insert(indice, palavra)
    return arvore[1]


def setRemoveTags(arvore):
    if settings.conjPTag in arvore[0] and type(arvore[0]) == str:  # se um dos filhos é uma conjunção
        children = arvore[1]
        for child in children:
            if child[0] == settings.conjBarTag:
                child[0] = settings.conjPTag
        arvore[0] = settings.removeTag
    if settings.CPTag in arvore[0] and type(arvore[0]) == str:  # se um dos filhos é uma conjunção
        children = arvore[1]
        for child in children:
            if child[0] == settings.CPBarTag:
                child[0] = settings.CPTag
        arvore[0] = settings.removeTag


def revisaTags(arvore):
    classe = arvore[0]
    if classe in settings.pointList:
        return
    if classe == settings.conjBarTag:  # or arvore[0] == settings.conjPTag:
        arvore = consertaConj(arvore)
    if classe == settings.CPBarTag:
        arvore = consertaC(arvore)

    numFilhos = len(arvore[1]) if type(arvore) is list and len(arvore) > 1 and type(arvore[1]) is list else 0

    if numFilhos > 0:
        for i in range(numFilhos):
            revisaTags(arvore[1][i])
            if settings.removeTag in arvore[1][i][0]:
                # print('if settings.removeTag in arvore[1][i][0]:')
                arvore[1] = arvore[1] + arvore[1][i][1]
                arvore[1].remove(arvore[1][i])
        setRemoveTags(arvore)
        # arvore = setRemoveTags(arvore)

    else:
        return


def imprimeArvore(arvore, nivel):
    classe = arvore[0]
    espacoEsquerda = ''.join('  ' for n in range(nivel))

    if len(arvore) > 1:
        # caso não seja um nó folha
        if type(arvore[1]) is list:
            if classe in settings.wordLevelTags:
                # stringRetorno = '{0}{1}'.format(espacoEsquerda, arvore[1])
                lPalavras = ' '.join(filho for filho in arvore[1])

                if classe == settings.conjPTag:
                    # palavra = treeText[inicio: inicio + treeText[inicio:].index(')')].split()[1].lower()
                    if not lPalavras in settings.conjList2:
                        settings.conjList2.append(lPalavras)

                stringRetorno = '{0}({1} {2})\n'.format(
                    espacoEsquerda, classe, lPalavras)
            else:
                stringRetorno = '{0}({1} \n'.format(espacoEsquerda, classe)

                filhos = ''.join(imprimeArvore(filho, nivel + 1) for filho in arvore[1])
                stringRetorno += filhos

                stringRetorno += '{0})\n'.format(espacoEsquerda)
        else:  # nós folha
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

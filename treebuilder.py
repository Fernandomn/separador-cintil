import settings


# conjTag = '_CONJP_'


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
        elif caracter in settings.pointList or caracter + frase[i + 1] in settings.pointList:
            lista.append([caracter])
            return i + indice, lista
        else:
            i += 1
    return i, lista[0]


def verificaCasosCONJ(arvore):
    if arvore[0] in settings.pointList:
        return
    if arvore[0] == settings.conjTag:
        listaClasses = []

        wordLevel = True
        for filho in arvore[1]:
            if type(filho[1]) is list:
                wordLevel = False
            # TODO verificar AQUI se os filhos da coordenação são todos folha (ou seja, coordenação word level)
            if filho[0] != '.' and filho[0] != ',' and filho[0] != settings.conjTag:
                listaClasses.append(filho[0])
            if filho[0] == 'CONJ':
                indice = arvore[1].index(filho)
                palavra = filho[1]
                arvore[1].remove(filho)
                arvore[1].insert(indice, palavra)

        arvore = arvore[1]
        # # TODO: Verificar se as classes são puramente POS. Se forem, a classe tem que ter o sintagma apropriado
        # if not wordLevel:
        #     classeCoord = listaClasses[0] if classesIguais(listaClasses) else "UCP"
        # else:
        #     # TODO Verificar se são sempre iguais
        #     if classesIguais(listaClasses):
        #         classeCoord = 'WL_'+dicSintagma[listaClasses[0]]
        #     else:
        #         print('classes diferentes em wordlevel')
        #     #     classeCoord = descobreSintagma(listaClasses)
        # arvore[0] = classeCoord

    numFilhos = len(arvore[1]) if type(arvore) is list and type(arvore[1]) is list else 0

    if numFilhos > 0:
        for i in range(numFilhos):
            verificaCasosCONJ(arvore[1][i])
        if arvore[0] == settings.conjTag:
            arvore = arvore[1]
        if 'CONJP' in arvore[1]:  # se um dos filhos é uma conjunção
            children = arvore[1]
            # arvore[1] =
    else:
        return

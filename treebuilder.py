import settings
import sintagma as s


def reconstroiArvoreObj(frase, indice, arvore):
    i = 0
    while i < (len(frase)):
        caracter = frase[i]
        if caracter == '(':
            classe = ''.join(c for c in frase.split(' ')[0] if c.isalpha() or c == '_')
            nova_arvore = s.Sintagma(classe, [], arvore.classe, '')
            novo_indice, subarvore = reconstroiArvoreObj(frase[i + 1:], i + 1, nova_arvore)
            i = novo_indice + 1
            arvore.filhos.append(subarvore)
        elif caracter == ')':
            if frase[:i].find(' ') >= 0:
                # recupera a classe, verificando char a char se é uma palavra
                classe = ''.join(c for c in frase.split(' ')[0] if c.isalpha() or c == '_')
                palavra = frase[:i].split(' ')[1]
            else:
                palavra = frase[:i]
                classe = palavra

            if len(arvore.filhos) > 0:
                subarvore = s.Sintagma(classe, arvore.filhos, arvore.classe, '')
                # return i + indice, subarvore
            else:
                subarvore = s.Sintagma(classe, [], arvore.classe, palavra)
            return i + indice, subarvore

        elif caracter in settings.pointList:
            point = caracter if not (caracter == '"' or caracter == "'") else caracter + caracter
            subarvore = s.Sintagma(settings.pointTag, [], arvore.classe, point)
            arvore.filhos.append(subarvore)
            i += 1
        else:
            i += 1
    return i, arvore


def consertaTagProbObj(arvore):
    # if arvore.classe == settings.conjBarTag and settings.conjPTag not in arvore.classe_pai:
    #     arvore.classe = settings.conjPTag
    for filho in arvore.filhos:
        arvore.valor += filho.valor + ' '
    arvore.valor = arvore.valor.strip()
    return arvore


def setRemoveTagsObj(arvore):
    to_remove = False
    if arvore.classe == settings.conjPTag:
        for filho in arvore.filhos:
            if filho.classe == settings.conjBarTag:
                to_remove = True
                filho.classe = settings.conjPTag
        # if to_remove:
        arvore.classe = settings.removeTag
    if arvore.classe == settings.CPTag:
        for filho in arvore.filhos:
            if filho.classe == settings.CPBarTag:
                to_remove = True
                filho.classe = settings.CPTag
        # if to_remove:
        arvore.classe = settings.removeTag
        # arvore.classe = settings.removeTag


# def consertaCObj(arvore):

def revisaTagsObj(arvore):
    classe = arvore.classe

    if classe == settings.pointTag:
        return
    if classe in settings.tagsProblematicas:
        arvore = consertaTagProbObj(arvore)

    if len(arvore.filhos) > 0:
        for filho in arvore.filhos:
            revisaTagsObj(filho)
            if settings.removeTag == filho.classe:
                arvore.removeFilho(filho)
        setRemoveTagsObj(arvore)
    else:
        return


def imprimeArvoreObj(arvore, nivel):
    espaco_esquerda = ''.join(' ' for n in range(nivel))

    # raiz
    if arvore.classe == '':
        return imprimeArvoreObj(arvore.filhos[0], nivel)
    # nao-terminal
    if len(arvore.filhos) > 0:

        string_filhos = ''
        # if arvore.valor != '':
        if arvore.classe in settings.wordLevelTags:
            for filho in arvore.filhos:
                string_filhos += filho.valor + ' '
            # string_filhos = string_filhos
            string_retorno = '{0}({1} {2})\n'.format(espaco_esquerda, arvore.classe, string_filhos.strip())
        else:
            for filho in arvore.filhos:
                string_filhos += imprimeArvoreObj(filho, nivel + 1)

            string_retorno = '{0}({1} \n{2}{0})\n'.format(espaco_esquerda, arvore.classe, string_filhos)
    # terminal
    else:
        if arvore.classe == settings.pointTag:
            string_retorno = '{0}{1}\n'.format(espaco_esquerda, arvore.valor)
        else:
            string_retorno = '{0}({1} {2})\n'.format(espaco_esquerda, arvore.classe, arvore.valor)

    return string_retorno

# def reconstroiArvore(frase, indice, lista):
#     i = 0
#     while i < len(frase):
#         caracter = frase[i]
#
#         if caracter == '(':
#             novoIndice, listaProv = reconstroiArvore(frase[i + 1:], i + 1, [])
#
#             i = novoIndice + 1
#             lista.append(listaProv)
#
#         elif caracter == ')':
#             if frase[:i].find(' ') >= 0:
#                 # recupera a classe, verificando char a char se é uma palavra
#                 classe = ''.join(c for c in frase.split(' ')[0] if c.isalpha() or c == '_')
#                 palavra = frase[:i].split(' ')[1]
#             else:
#                 # refazer. simbolos nem sempre precisam de uma classe distinta. e essa não é a melhor forma de achar um simbolo
#                 palavra = frase[:i]
#                 classe = palavra
#
#             if len(lista) > 0:  # é uma folha ou não?
#                 return i + indice, [classe, lista]
#             else:
#                 return i + indice, [classe, palavra]
#
#         elif caracter in settings.pointList:  # or caracter + frase[i + 1] in settings.pointList:
#             charSimb = caracter if not (caracter == '"' or caracter == "'") else caracter + caracter
#             # lista.append([caracter]) if not (caracter == '"' or caracter == "'") else lista.append(
#             #     [caracter + caracter])
#             # return i + indice + 1, [settings.pointTag, charSimb]
#             # return i + indice + 1, [lista, [settings.pointTag, charSimb]]
#             # return i + indice + 1, [charSimb, lista]
#             lista.append([charSimb])
#             i += 1
#         else:
#             i += 1
#     return i, lista[0]
#
#
# def consertaConj(arvore):
#     for filho in arvore[1]:
#         # if filho[0] == settings.conjTag:
#         indice = arvore[1].index(filho)
#         palavra = filho[1]
#         arvore[1].remove(filho)
#         arvore[1].insert(indice, palavra)
#     return arvore[1]
#
#
# def consertaC(arvore):
#     for filho in arvore[1]:
#         # if filho[0] == settings.CTag:
#         indice = arvore[1].index(filho)
#         palavra = filho[1]
#         arvore[1].remove(filho)
#         arvore[1].insert(indice, palavra)
#     return arvore[1]
#
#
# def setRemoveTags(arvore):
#     if settings.conjPTag in arvore[0] and type(arvore[0]) == str:  # se um dos filhos é uma conjunção
#         children = arvore[1]
#         for child in children:
#             if child[0] == settings.conjBarTag:
#                 child[0] = settings.conjPTag
#         arvore[0] = settings.removeTag
#     if settings.CPTag in arvore[0] and type(arvore[0]) == str:  # se um dos filhos é uma conjunção
#         children = arvore[1]
#         for child in children:
#             if child[0] == settings.CPBarTag:
#                 child[0] = settings.CPTag
#         arvore[0] = settings.removeTag

#
# def revisaTags(arvore):
#     classe = arvore[0]
#     if classe in settings.pointList:
#         return
#     if classe == settings.conjBarTag:  # or arvore[0] == settings.conjPTag:
#         arvore = consertaConj(arvore)
#     if classe == settings.CPBarTag:
#         arvore = consertaC(arvore)
#
#     numFilhos = len(arvore[1]) if type(arvore) is list and len(arvore) > 1 and type(arvore[1]) is list else 0
#
#     if numFilhos > 0:
#         for i in range(numFilhos):
#             revisaTags(arvore[1][i])
#             if settings.removeTag in arvore[1][i][0]:
#                 # print('if settings.removeTag in arvore[1][i][0]:')
#                 arvore[1] = arvore[1] + arvore[1][i][1]
#                 arvore[1].remove(arvore[1][i])
#         setRemoveTags(arvore)
#         # arvore = setRemoveTags(arvore)
#
#     else:
#         return
#
#
# def imprimeArvore(arvore, nivel):
#     classe = arvore[0]
#     espacoEsquerda = ''.join('  ' for n in range(nivel))
#
#     # é subarvore
#     if len(arvore) > 1:
#         # caso não seja um nó folha
#         if type(arvore[1]) is list:
#             if classe in settings.wordLevelTags:
#                 # lPalavras = ' '.join(filho for filho in arvore[1])
#                 lPalavras = ''
#                 for filho in arvore[1]:
#                     lPalavras += filho + ' '
#                 lPalavras = lPalavras.strip()
#
#                 if classe == settings.conjPTag:
#                     # palavra = treeText[inicio: inicio + treeText[inicio:].index(')')].split()[1].lower()
#                     if not lPalavras in settings.conjList2:
#                         settings.conjList2.append(lPalavras)
#
#                 stringRetorno = '{0}({1} {2})\n'.format(espacoEsquerda, classe, lPalavras)
#             else:
#                 stringRetorno = '{0}({1} \n'.format(espacoEsquerda, classe)
#
#                 # filhos = ''.join(imprimeArvore(filho, nivel + 1) for filho in arvore[1])
#                 filhos = ''
#                 for filho in arvore[1]:
#                     filhos += imprimeArvore(filho, nivel + 1)
#
#                 stringRetorno += filhos
#
#                 stringRetorno += '{0})\n'.format(espacoEsquerda)
#         else:  # nós folha
#             if classe.isalpha():
#
#                 if classe == settings.conjTag:
#                     # palavra = treeText[inicio: inicio + treeText[inicio:].index(')')].split()[1].lower()
#                     if not arvore[1] in settings.conjList2:
#                         settings.conjList2.append(arvore[1])
#                 # else:
#                 stringRetorno = '{0}({1} {2})\n'.format(
#                     espacoEsquerda, classe, arvore[1])
#             else:
#                 stringRetorno = '{0}({1})\n'.format(espacoEsquerda, classe)
#     else:
#         # é folha
#         if type(arvore) is str:
#             stringRetorno = '{0}{1}'.format(espacoEsquerda, arvore)
#         elif type(arvore) is list:
#             # stringRetorno = '{0}{1}'.format(espacoEsquerda, imprimeArvore(arvore[0], nivel + 1))
#             if type(arvore[0]) is str:
#                 stringRetorno = '{0}{1}'.format(espacoEsquerda, arvore[0])
#             else:
#                 stringTemp = ''
#                 for filho in arvore[0]:
#                     stringTemp += imprimeArvore(filho, nivel + 1)
#                 stringRetorno = '{0}{1}'.format(espacoEsquerda, stringTemp)
#
#     return stringRetorno

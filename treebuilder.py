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
    if arvore.classe == settings.conjBarTag and settings.conjPTag not in arvore.classe_pai:
        arvore.classe = settings.conjPTag
    for filho in arvore.filhos:
        arvore.valor += filho.valor + ' '
    arvore.valor = arvore.valor.strip()
    return arvore


def setRemoveTagsObj(arvore):
    to_remove = False
    if arvore.classe == settings.conjPTag:
        for filho in arvore.filhos:
            if filho.classe == settings.conjBarTag:
                # to_remove = True
                filho.classe = settings.conjPTag
                arvore.classe = settings.removeTag
        # if to_remove:
    if arvore.classe == settings.CPTag:
        for filho in arvore.filhos:
            if filho.classe == settings.CPBarTag:
                # to_remove = True
                filho.classe = settings.CPTag
        arvore.classe = settings.removeTag
        # if to_remove:
        # arvore.classe = settings.removeTag


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
        if arvore.classe in settings.wordLevelTags and arvore.valor != '':
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

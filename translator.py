import settings
import treebuilder as tb


def tradutor(tag):
    if not settings.posDict:
        settings.posDict = {
            "A": "JJ",  # Adjetivo
            "A'": "ADJP",  # Sintagma Adjectival
            # "ADJ": "JJ",  # Adjectivos
            "ADV": "RB",  # Advérbios
            "ADV'": "ADVP",  # Sintagma Adverbial
            "ADVP": "ADVP",  # Sintagma Adverbial
            "AP": "ADJP",  # Sintagma Adjectival
            "ART'": "NP",  # sintagma de artigo - não ocorre no handbook
            # # o artigo 'Primeiros passos na aquisição da sintaxe:' chama NP de DT. talvez ajude. mas acho que é melhor corrigir essa árvore.
            "ART": "DT",  # Artigo # Artigo [REVISAR] (TODO) nota: unico caso em que essa tag aparece está errado.
            "C'": settings.CPBarTag,  # "SBAR" Sintagma Objetal  - nao ocorre no handbook
            "C": settings.CTag,  # Complemento (TODO) objeto
            "CARD": "CD",  # Cardinais
            "CARD'": "NP",  # Sintagmas Cardinais
            # "CJ": "CC",  # Conjunções - Essa tag aparece apenas em manuais. não ocorre no CINTIL em momento algum.
            "CL": "PRP",  # Clíticos [explicar] https://ciberduvidas.iscte-iul.pt/consultorio/perguntas/clitico/15150
            # "CN": "NNS",  # Nomes comuns
            "CONJ'": settings.conjBarTag,  # sintagma Conjuntivo
            "CONJ": settings.conjTag,  # Conjunções
            "CONJP": settings.conjPTag,  # sintagma Conjuntivo
            "CP": settings.CPTag,  # "SBAR"  Sintagma Objetal (TODO) v
            "D": "DT",  # Artigo
            "D1": "DT",  # Quantificadores - nao ocorre no handbook, só no site
            "D2": "JJ",  # Quantificadores - nao ocorre no handbook, só no site
            # "DA": "DT",  # Artigos Definidos
            "DEM": "DT",
            # # Demonstrativos -> Para o PTB, this, that, these, those são, também, artigos. logo, DEM -> DT.
            # "DFR": "QP",  # Denominadores de Fracções
            # "DGT": "CD",  # Numerais Árabes
            # "DGTR": "CD",  # Numerais Romanos
            # "DM": "UH",  # Marcadores Discursivos nota: não aparece em nenhum caso
            # "EADR": "NN",  # Endereços Electrónicos
            # "EOE": settings.eofTag,  # Fim de Enumeração
            # "EXC": "UH",  # Exclamação
            # "GER": "VBG",  # Gerúndios
            # "GERAUX": "VBG",  # Gerúndio "ter"/"haver" em tempos compostos
            # "IA    ": "DT",  # Artigos Indefinidos
            # "IND": "PRP",  # Indefinidos
            # "INF": "VB",  # Infinitivo
            # "INFAUX": "VB",  # Infinitivo "ter"/"haver" em tempos compostos
            # "INT": "WP",  # Interrogativos
            "ITJ": "UH",  # Interjecções
            "ITJ'": "INTJ",  # Interjecções (TODO)
            # "LTR": "NN",  # Letras
            # "MGT": "NN",  # Unidade de Medida
            # "MTH": "NNP",  # Meses (TODO) v
            "N": "NNS",  # Substantivo
            "N'": "NP",  # Sintagmas Nominais
            "NP": "NP",  # Sintagmas Nominais
            "ORD": "CD",  # Ordinais
            "P": "IN",  # Preposição
            "P'": "PP",  # Sintagmas Preposicionais - não ocorre no handbook
            # "PADR": "NN",  # Parte de Endereço
            "PERCENT": "NN",
            "PERCENT'": "NP",  # Sintagma percentual (TODO) nota: pode ser substituido por um termo so 'por cento'
            # # simbolo percentual nota: pode ser pronome + substantivo tbm ('por cento') # nota2: PTB considera o % como NN (single noum)
            "PERCENTP": "NP",  # Sintagma percentual (TODO) nota: ptb considera como NP
            # "PNM": "NP",  # Parte de Nome (TODO) v
            "PNT": settings.pointTag,  # Pontuação
            "POSS'": "NP",  # Possessivos (TODO) nota: não existe um sintagma pronominal. o jeito é manter o NP msm
            "POSS": "PP$",  # Possessivos v
            # "POSSP": "NP",  # Possessivos (TODO) nota: não ocorre
            "PP": "PP",  # Sintagmas Preposicionais
            # "PPA": "VBN",  # Particípios passados que não formam tempos compostos
            # "PPT": "VBN",  # Particípios passados em tempos compostos
            # "PREP": "IN",  # Preposições
            "PRS": "PRP",  # Pronomes Pessoais
            "QNT": "PRP",  # Quantificadores
            "QNT'": "NP",  # Quantificadores
            "REL": "PRP",  # Pronomes Relativos
            "S": "S",  # Sentença
            # "STT": "NN",  # Títulos Sociais
            # "SYB": "SYM",  # Símbolos
            # "TERMN": "SYM",  # Terminações Opcionais
            # "UM    ": "CD",  # "um" ou "uma"
            # "UNIT": "NN",  # Unidade de Medida Abreviada
            "V'": "VP",  # Sintagma Verbal
            "V": "VB",  # Verbos (sem ser PPA, PPT, INF ou GER)
            # "VAUX": "VB",  # Formas Finitas de "ter" ou "haver" em tempos compostos
            "VP": "VP",  # Sintagma Verbal
            # "WD": "NNP"  # Dias da Semana
        }
    return settings.posDict[tag]


def classeProblematica(classe):
    return classe[0] == '_' and classe[-1] == '_'
    # pass


def extraiPnt(index, inicio, treeText):
    final = inicio + treeText[inicio:].index(')')
    pntWord = treeText[final - 1]
    if pntWord == '"' or pntWord == "'":
        # se é a primeira ocorrência
        if settings.isFirstQuoteMark:
            pntWord = "``"
        else:  # se é a última
            pntWord = "''"
        settings.isFirstQuoteMark = not settings.isFirstQuoteMark

    if not pntWord in settings.pointList:  # verificar necessidade de adicionar simbolos singulares, além dos pares
        settings.pointList.append(pntWord)

    return treeText[:index] + pntWord + treeText[final + 1:]


def extraiEoe(index, inicio, treeText):
    final = inicio + treeText[inicio:].index(')')
    eoeWord = treeText[final - 1]
    return treeText[:index] + eoeWord + treeText[final + 1:]
    pass


def traduzirTags(treeText):
    settings.isFirstQuoteMark = True
    reverArvore = False

    for index in reversed(range(len(treeText))):
        caractere = treeText[index]

        if caractere == '(':
            inicio = index + 1
            final = inicio + treeText[inicio:].index(' ')
            classe = treeText[inicio:final]

            # ------------------------
            if classe in settings.tagOcc:
                settings.tagOcc[classe] += 1
            else:
                settings.tagOcc[classe] = 1
            # if classe == settings.CTag:
            #     word = treeText[final:].split(')')[0].strip().lower()
            #     if word in settings.CWordDict:
            #         settings.CWordDict[word] += 1
            #     else:
            #         settings.CWordDict[word] = 1
            # ------------------------

            if classe == settings.pointTag:
                treeText = extraiPnt(index, inicio, treeText)
            # elif classe == settings.eofTag:
            #     treeText = extraiEoe(index, inicio, treeText)
            else:
                classeTraduzida = tradutor(classe)
                treeText = treeText[:inicio] + classeTraduzida + treeText[final:]
                if not reverArvore and classeProblematica(classeTraduzida):
                    reverArvore = True

            # palavra = treeText[inicio: inicio + treeText[inicio:].index(')')].split()[1].lower()
            # if classe == settings.conjTag or classe == 'CONJ':
            #     palavra = treeText[inicio: inicio + treeText[inicio:].index(')')].split()[1].lower()
            #     if not palavra in settings.conjList:
            #         settings.conjList.append(palavra)
            # if classe == 'CL':
            #     palavra = treeText[inicio: inicio + treeText[inicio:].index(')')].split()[1].lower()
            #     if not palavra in settings.clitList:
            #         settings.clitList.append(palavra)

    # if settings.conjBarTag in treeText:

    if reverArvore:
        # print('precisa rever. Frase: {0}'.format(treeText))

        i, listTree = tb.reconstroiArvore(treeText, 0, [])
        listTree = ['S', listTree]
        tb.revisaTags(listTree)  # ???
        treeText = tb.imprimeArvore(listTree, 0)

        # print(treeText)

    return treeText

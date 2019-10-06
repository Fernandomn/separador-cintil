import settings
import treebuilder as tb


def tradutor(tag):
    if not settings.posDict:
        settings.posDict = {
            "A": "JJ",  # Adjetivo
            "A'": "ADJP",  # Sintagma Adjectival
            "AP": "ADJP",  # Sintagma Adjectival
            "ADJ": "JJ",  # Adjectivos
            "ADV": "RB",  # Advérbios
            "ADVP": "ADVP",  # Sintagma Adverbial
            "ADV'": "ADVP",  # Sintagma Adverbial
            "CARD": "CD",  # Cardinais
            "CARD'": "NP",  # Sintagmas Cardinais
            "C": "IN",  # Complemento (TODO) objeto
            "CP": "SBAR",  # Sintagma Objetal (TODO) v
            "C'": "SBAR",  # Sintagma Objetal (TODO) v
            "CJ": "CC",  # Conjunções - Essa tag aparece apenas em manuais. não ocorre no CINTIL em momento algum.
            "CONJ": settings.conjTag,  # Conjunções
            "CONJ'": settings.conjBarTag,  # sintagma Conjuntivo
            "CONJP": "CONJP",  # sintagma Conjuntivo
            "CL": "PRP",  # Clíticos [explicar]
            "CN": "NNS",  # Nomes comuns
            "N": "NNS",  # Substantivo
            "D": "DT",  # Artigo
            "DA": "DT",  # Artigos Definidos
            "ART": "DT",  # Artigo
            # Artigo [REVISAR] (TODO) nota: unico caso em que essa tag aparece está errado.
            "ART'": "NP",
            # o artigo 'Primeiros passos na aquisição da sintaxe:' chama NP de DT. talvez ajude.
            # mas acho que é melhor corrigir essa árvore.
            # Demonstrativos -> Para o PTB, this, that, these, those são, também, artigos. logo, DEM -> DT.
            "DEM": "DT",
            "DFR": "CD",  # Denominadores de Fracções
            "DGTR": "CD",  # Numerais Romanos
            "DGT": "CD",  # Numerais Árabes
            "DM": "UH",  # Marcadores Discursivos nota: não aparece em nenhum caso
            "EADR": "NN",  # Endereços Electrónicos
            "EOE": "IN",  # Fim de Enumeração
            "EXC": "UH",  # Exclamação
            "GER": "VBG",  # Gerúndios
            "GERAUX": "VBG",  # Gerúndio "ter"/"haver" em tempos compostos
            "IA	": "DT",  # Artigos Indefinidos
            "IND": "PRP",  # Indefinidos
            "INF": "VB",  # Infinitivo
            "INFAUX": "VB",  # Infinitivo "ter"/"haver" em tempos compostos
            "INT": "WP",  # Interrogativos
            "ITJ": "UH",  # Interjecções
            "ITJ'": "INTJ",  # Interjecções (TODO)
            "LTR": "NN",  # Letras
            "MGT": "NN",  # Unidade de Medida
            "MTH": "NNP",  # Meses (TODO) v
            "NP": "NP",  # Sintagmas Nominais
            "N'": "NP",  # Sintagmas Nominais
            "ORD": "CD",  # Ordinais
            "PADR": "NN",  # Parte de Endereço
            "PNM": "NP",  # Parte de Nome (TODO) v
            "PNT": settings.pointTag,  # Pontuação
            "POSS": "PP$",  # Possessivos v
            # Possessivos (TODO) nota: não existe um sintagma pronominal. o jeito é manter o NP msm
            "POSS'": "NP",
            "POSSP": "NP",  # Possessivos (TODO) nota: não ocorre
            "PPA": "VBN",  # Particípios passados que não formam tempos compostos
            "P": "IN",  # Preposição
            "PP": "PP",  # Sintagmas Preposicionais
            "P'": "PP",  # Sintagmas Preposicionais
            "PPT": "VBN",  # Particípios passados em tempos compostos
            # simbolo percentual nota: pode ser pronome + substantivo tbm ('por cento')
            "PERCENT": "NN",
            # guia oficial diz 'LDFR1…LDFRn'.
            # nota2: PTB considera o % como NN (single noum)
            # Sintagma percentual (TODO) nota: pode ser substituido por um termo so 'por cento'
            "PERCENT'": "NP",
            # Sintagma percentual (TODO) nota: ptb considera como NP
            "PERCENTP": "NP",
            "PREP": "IN",  # Preposições
            "PRS": "PRP",  # Pronomes Pessoais
            "QNT": "PRP",  # Quantificadores
            "D1": "DT",  # Quantificadores
            "D2": "JJ",  # Quantificadores
            "QNT'": "ADJP",  # Quantificadores
            "REL": "PRP",  # Relativos
            "S": "S",  # Sentença
            "STT": "NN",  # Títulos Sociais
            "SYB": "SYM",  # Símbolos
            "TERMN": "SYM",  # Terminações Opcionais
            "UM	": "CD",  # "um" ou "uma"
            "UNIT": "NN",  # Unidade de Medida Abreviada
            "VAUX": "VB",  # Formas Finitas de "ter" ou "haver" em tempos compostos
            "V": "VB",  # Verbos (sem ser PPA, PPT, INF ou GER)
            "V'": "VP",  # Sintagma Verbal
            "VP": "VP",  # Sintagma Verbal
            "WD": "NNP"  # Dias da Semana
        }
    return settings.posDict[tag]


def traduzirTags(treeText):
    isFirstQuoteMark = True
    for index in reversed(range(len(treeText))):
        caractere = treeText[index]
        if (caractere == '('):
            inicio = index + 1
            final = inicio + treeText[inicio:].index(' ')
            classe = treeText[inicio:final]

            if classe == settings.pointTag:
                final = inicio + treeText[inicio:].index(')')
                pntWord = treeText[final - 1]
                if pntWord == '"' or pntWord == "'":
                    # se é a primeira ocorrência
                    if isFirstQuoteMark:
                        pntWord = "``"
                    else:  # se é a última
                        pntWord = "''"
                    isFirstQuoteMark = not isFirstQuoteMark
                treeText = treeText[:index] + pntWord + treeText[final + 1:]
                if not pntWord in settings.pointList:  # verificar necessidade de adicionar simbolos singulares, além dos pares
                    settings.pointList.append(pntWord)
            else:
                treeText = treeText[:inicio] + \
                           tradutor(classe) + treeText[final:]
            if classe == settings.conjTag or classe == 'CONJ':
                palavra = treeText[inicio: inicio+treeText[inicio:].index(')')].split()[1].lower()
                if not palavra in settings.conjList:
                    settings.conjList.append(palavra)

    # fazer com todas, ou só com as que tem CONJ?
    if settings.conjBarTag in treeText:
        i, listTree = tb.reconstroiArvore(treeText, 0, [])
        listTree = ['S', listTree]
        tb.verificaCasosCONJ(listTree)
        treeText = tb.imprimeArvore(listTree, 0, settings.conjPTag)
        print(treeText)

    return treeText

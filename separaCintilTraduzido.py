import xml.etree.ElementTree as ET

# Referencia:
# http://cintil.ul.pt/pt/cintilwhatsin.html#breakdown
# https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# https://www.sketchengine.eu/penn-treebank-tagset/
# https://www.sketchengine.eu/modified-penn-treebank-tagset/
# https://www.eecis.udel.edu/~vijay/cis889/ie/pos-set.pdf
# https://www.clips.uantwerpen.be/pages/mbsp-tags
# https://ciberduvidas.iscte-iul.pt/consultorio/perguntas/determinantes-quantificadores-e-pronomes/29575
# https://pt.pons.com

arvore = ET.parse('CINTIL-Treebank.xml')
raiz = arvore.getroot()

posDict = {}


def tradutor(tag):
    global posDict
    if not posDict:
        posDict = {
            "A": "JJ",  # Adjetivo
            "A'": "ADJP",  # Sintagma Adjectival [explicar]
            "AP": "ADJP",  # Sintagma Adjectival
            "ADJ": "JJ",  # Adjectivos
            "ADV": "RB",  # Advérbios
            "ADVP": "ADVP",  # Sintagma Adverbial
            "ADV'": "ADVP",  # Sintagma Adverbial
            "CARD": "CD",  # Cardinais
            "CARD'": "NP",  # Sintagmas Cardinais
            "C": "IN",  # Complemento (TODO) v
            "CP": "SBAR",  # Sintagma Complemental (TODO) v
            "C'": "SBAR",  # Sintagma Complemental (TODO) v
            "CJ": "CC",  # Conjunções [explicar]
            # referencia: http://amyrey.web.unc.edu/classes/ling-101-online/tutorials/how-to-draw-syntax-trees/
            "CONJ": "CC",  # Conjunções
            "CONJ'": "NP",  # sintagma Conjuntivo (TODO)
            "CONJP": "NP",  # sintagma Conjuntivo (TODO)
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
            "DEM": "PRP",  # Demonstrativos
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
            "PNT": ".",  # Pontuação
            "POSS": "PRP$",  # Possessivos v
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
            "QNT": "JJ",  # Quantificadores
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
    return posDict[tag]


ns = {'base': "http://nlx.di.fc.ul.pt",
      'clarin': "http://nlx.di.fc.ul.pt",
      'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

for corpus in raiz.findall('base:corpus', ns):
    for sentenca in corpus.findall('base:sentence', ns):
        id = sentenca.find('base:id', ns).text.replace('/', '-')
        raw = sentenca.find('base:raw', ns)
        tree = sentenca.find('base:tree', ns)
        treeText = tree.text
        # for index in range(len(treeText)-1, 0, -1):
        for index in reversed(range(len(treeText))):
            caractere = treeText[index]
            if(caractere == '('):
                inicio = index+1
                final = inicio + treeText[inicio:].index(' ')
                classe = treeText[inicio:final]
                # print(raw.text)
                # print(treeText)
                # print(classe)
                treeText = treeText[:inicio] + \
                    tradutor(classe)+treeText[final:]

        rawFile = open('raw-trad/%s' % id, 'w')
        treeFile = open('tree-trad/%s' % id, 'w')
        rawFile.write(raw.text)
        treeFile.write(treeText)
        rawFile.close()
        treeFile.close()

        # print(id.text)
        # print(raw.text)
        # print(tree.text)

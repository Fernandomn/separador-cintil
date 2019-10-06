import xml.etree.ElementTree as ET
import treebuilder as tb
import settings
import translator
import os

# TODO: Pegar correções da tabela no drive, e criar scripts necessários

# Referencia:
# http://amyrey.web.unc.edu/classes/ling-101-online/tutorials/how-to-draw-syntax-trees/
# http://cintil.ul.pt/pt/cintilwhatsin.html#breakdown
# https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# https://www.sketchengine.eu/penn-treebank-tagset/
# https://www.sketchengine.eu/modified-penn-treebank-tagset/
# https://www.eecis.udel.edu/~vijay/cis889/ie/pos-set.pdf
# https://www.clips.uantwerpen.be/pages/mbsp-tags
# https://ciberduvidas.iscte-iul.pt/consultorio/perguntas/determinantes-quantificadores-e-pronomes/29575
# https://pt.pons.com

# https://nlp.stanford.edu/software/parser-faq.html#headfinder
# Why do I get the exception "null head found for tree" after training my own parser model?
# The default HeadFinder is written specifically for the PTB. If you train a parser on trees that use a different set of productions, the default HeadFinder will not know how to handle this and will throw this exception. The easiest way to get around this problem is to use LeftHeadFinder instead. You can also get a slight performance increase by writing a custom HeadFinder for your treebank and using that instead.

arvore = ET.parse('CINTIL-Treebank.xml')
raiz = arvore.getroot()

ns = {'base': "http://nlx.di.fc.ul.pt",
      'clarin': "http://nlx.di.fc.ul.pt",
      'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

occList = ['CONJ', 'CP', 'C']


# metodo criado unicamente para facilitar escrita do projeto final. servepara criar um arquivo com uma lista de conjunções.
def createListFiles():
    createListFile('separated_conjunction_list.txt', settings.conjList)
    createListFile('combined_conjunction_list.txt', settings.conjList2)
    createListFile('points_list.txt', settings.pointList)


def createListFile(fileName, list):
    conjFile = open(fileName, 'w')
    # conjFile.write(settings.conjList)]
    settings.conjList.sort()
    conjFile.write("\n".join(str(item) for item in list))
    conjFile.close()


def verificaOcorrencias(occList, treeText):
    for tag in occList:
        fileName = 'occurrence_list_{0}.txt'.format(tag)
        # if not os.path.exists(fileName):
        #     occFile = open(fileName, 'w')
        # else:
        #     occFile = open(fileName, 'a')
        occFile = open(fileName, 'a' if os.path.exists(fileName) else 'w')
        if '({0}'.format(tag) in treeText.split():
            occFile.write(treeText + '\n')
        occFile.close()


def main():
    settings.init()

    for corpus in raiz.findall('base:corpus', ns):
        for sentenca in corpus.findall('base:sentence', ns):
            id = sentenca.find('base:id', ns).text.replace('/', '-')
            raw = sentenca.find('base:raw', ns)
            tree = sentenca.find('base:tree', ns)
            treeText = tree.text

            verificaOcorrencias(occList, treeText)
            # for index in range(len(treeText)-1, 0, -1):

            treeText = translator.traduzirTags(treeText)

            rawFile = open('raw-trad/%s' % id, 'w')
            treeFile = open('tree-trad/%s' % id, 'w')
            rawFile.write(raw.text)
            treeFile.write(treeText)
            rawFile.close()
            treeFile.close()

            # print(id.text)
            # print(raw.text)
            # print(tree.text)
    createListFiles()


if __name__ == '__main__':
    main()

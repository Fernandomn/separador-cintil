import xml.etree.ElementTree as ET
import treebuilder as tb
import settings
import translator
import os
import csv

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

occList = ["CL", "CONJ'"]
dir_relatorios = 'relatorios'
dir_raw_trad = 'raw-trad'
dir_tree_trad = 'tree-trad'
dir_list = [dir_relatorios, dir_raw_trad, dir_tree_trad]


# metodo criado unicamente para facilitar escrita do projeto final. servepara criar um arquivo com uma lista de conjunções.
def printOccList(dict):
    file_name = '{0}/{1}'.format(dir_relatorios, 'occurrence_count.csv')
    occ_file = open(file_name, 'w', encoding='utf-8')
    listKeys = settings.posDict.keys()
    for key in sorted(listKeys):
        occ_file.write("{0}, {1}\n".format(key, dict[key] if key in dict else 0))

    occ_file.close()


def createListFiles():
    createListFile('separated_conjunction_list.txt', settings.conjList)
    # createListFile('combined_conjunction_list.txt', settings.conjList2)
    createListFile('points_list.txt', settings.pointList)
    createListFile('clitics_list.txt', settings.clitList)
    printOccList(settings.tagOcc)


def createListFile(fileName, list):
    file_name = '{0}/{1}'.format(dir_relatorios, fileName)
    conjFile = open(file_name, 'w', encoding='utf-8')
    list.sort()
    conjFile.write("\n".join(str(item) for item in list))
    conjFile.close()


def verificaOcorrencias(occList, treeText):
    for tag in occList:
        fileName = '{0}/{1}'.format(dir_relatorios, 'occurrence_list_{0}.txt'.format(tag))
        occFile = open(fileName, 'a' if os.path.exists(fileName) else 'w', encoding='utf-8')
        if '({0}'.format(tag) in treeText.split():
            occFile.write(treeText + '\n')
        occFile.close()


def iniciaOcorrencias():
    for dir in dir_list:
        if not os.path.exists(dir):
            os.mkdir(dir)
        # os.chdir(dir)

    for tag in occList:
        fileName = '{0}/{1}'.format(dir_relatorios, 'occurrence_list_{0}.txt'.format(tag))
        occFile = open(fileName, 'w', encoding='utf-8')
        occFile.close()


def createTreeFile(base_dir, parse_id, text):
    tree_file = open('{0}-trad/{1}'.format(base_dir, parse_id), 'w', encoding='utf-8')
    tree_file.write(text)
    tree_file.close()


def main():
    settings.init()
    iniciaOcorrencias()
    for corpus in raiz.findall('base:corpus', ns):
        for sentenca in corpus.findall('base:sentence', ns):
            parse_id = sentenca.find('base:id', ns).text.replace('/', '-')
            raw = sentenca.find('base:raw', ns)
            tree = sentenca.find('base:tree', ns)
            tree_text = tree.text

            verificaOcorrencias(occList, tree_text)

            tree_text = translator.traduzirTags(tree_text)
            createTreeFile('raw', parse_id, raw.text)
            createTreeFile('tree', parse_id, tree_text)

    createListFiles()


if __name__ == '__main__':
    main()

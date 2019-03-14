import xml.etree.ElementTree as ET

arvore = ET.parse('CINTIL-Treebank.xml')
raiz = arvore.getroot()

ns = {'base': "http://nlx.di.fc.ul.pt",
      'clarin': "http://nlx.di.fc.ul.pt",
      'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

for corpus in raiz.findall('base:corpus', ns):
    for sentenca in corpus.findall('base:sentence', ns):
        id = sentenca.find('base:id', ns).text.replace('/', '-')
        raw = sentenca.find('base:raw', ns)
        tree = sentenca.find('base:tree', ns)

        rawFile = open('raw/%s' % id, 'w')
        treeFile = open('tree/%s' % id, 'w')
        rawFile.write(raw.text)
        treeFile.write(tree.text)
        rawFile.close()
        treeFile.close()

        # print(id.text)
        # print(raw.text)
        # print(tree.text)

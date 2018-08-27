from bs4 import BeautifulSoup

#DESIGN CHOICE: don't include the seed directly coz too much string comes into picture
#from text
def addArtificialSeeds(html, seed):
    soup = BeautifulSoup(html.decode('utf-8'), 'html.parser')
    output = []
    for s in soup.strings:
        s = str(s.encode('utf-8')).strip()
        s = " ".join(s.split())
        if s.startswith(seed) and len(s)<=len(seed)*3:
            output.append(s)
    return list(set(output))


def addArtificialKeyValueSeeds(html, seed):
    (k, v) = seed
    output = []
    soup = BeautifulSoup(html.decode('utf-8'), 'html.parser')
    keys   = []
    values = []
    # print((k,v))
    for s in soup.strings:
        s = str(s.encode('utf-8')).strip()
        s = " ".join(s.split())
        # s = str(s.encode('utf-8')).strip()
        if s.startswith(k) and len(s) <= len(k) * 3:
            keys.append(s)
        elif s.startswith(v) and len(s)<=len(v)*3:
            values.append(s)
            # print("Value accepted")
    for key in keys:
        for value in values:
            output.append((key, value))
    return list(set(output))

import itertools

def addArtificialClusterSeeds(html, seedList):
    soup = BeautifulSoup(html.decode('utf-8'), 'html.parser')
    seedStore = []
    for seed in seedList:
        seedContentList = []
        for s in soup.strings:
            s = str(s.encode('utf-8')).strip()
            s = " ".join(s.split())
            if s.startswith(seed) and len(s) <= len(seed) * 3:
                seedContentList.append(s)
        if len(seedContentList)>0:
            seedStore.append(list(set(seedContentList)))
    #do the cross product of lists
    return [list(element) for element in itertools.product(*seedStore)]

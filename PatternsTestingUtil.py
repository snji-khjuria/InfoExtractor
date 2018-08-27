import csv
def readEntityExtractionPatterns(patternsLocation):
    print("Reading the entity extraction patterns")
    output = []
    with open(patternsLocation, "r") as f:
        lines = csv.reader(f, delimiter='\t')
        # lines = f.readlines()
        # lines = lines[1:]
        for line in lines:
            # print(line)
            # print(line[0])
            # line = line.strip()
            # line = line.split("\t")
            output.append((line[0], line[1]))
    return output[1:]


def readTripletPatterns(patternsLocation):
    print("Reading the patterns...")
    output = []
    with open(patternsLocation, "r") as f:
        lines = csv.reader(f, delimiter="\t")
        for line in lines:
            output.append((line[0], line[1], line[2]))
    print("Patterns read")
    return output[1:]

#find entity set in left and right pattern.
def doEntityExtractions(leftPattern, rightPattern, pageContent):
    searchIndex = 0
    output = []
    while True:
        try:
            startL = pageContent.index(leftPattern, searchIndex)
            endL   = startL+len(leftPattern)
            end    = pageContent.index(rightPattern, endL)
            if end-endL<=1000:
                output.append(pageContent[endL:end].strip())
            searchIndex = startL+1
        except ValueError:
            return list(set(output))
    return list(set(output))


def getClusterStrings(middlePattern, clusters):
    output = []
    for cluster in clusters:
        outputPerCluster = []
        searchIndex      = 0
        while True:
            try:
                startL         = cluster.index(middlePattern, searchIndex)
                clusterElement = cluster[searchIndex:startL].strip()
                # print("Cluster element is ")
                # print(clusterElement)
                outputPerCluster.append(clusterElement)
                searchIndex = startL+len(middlePattern)
            except ValueError:
                break
        # print("Output per cluster is ")
        # print(outputPerCluster)
        # print("Cluster was ")
        # print(cluster)
        outputPerCluster = "\n".join(outputPerCluster)
        output.append(outputPerCluster)
    # print("Output is ")
    # print(output)
    return output

def doClusterExtraction(leftPattern, middlePattern, rightPattern, pageContent):
    searchIndex = 0
    output = []
    while True:
        try:
            startL = pageContent.index(leftPattern, searchIndex)
            endL   = startL + len(leftPattern)
            end    = pageContent.index(rightPattern, endL)
            if end - endL<=50000:
                output.append(pageContent[endL:end].strip())
            searchIndex = startL+1
        except ValueError:
            break
    # print("Number of clusters are:- " + str(len(output)))
    # print(output)
    output = getClusterStrings(middlePattern, output)
    return list(set(output))


def doRelationExtractions(leftPattern, middlePattern, rightPattern, pageContent):
    searchIndex = 0
    output = []
    while True:
        try:
            startL = pageContent.index(leftPattern, searchIndex)
            endL   = startL + len(leftPattern)
            end    = pageContent.index(middlePattern, endL)
            keyLength = end - endL
            if keyLength<=1000:
                searchIndex = end + len(middlePattern)
                startR      = pageContent.index(rightPattern, searchIndex)
                valueLength = startR - searchIndex
                if valueLength<=1000:
                    key = pageContent[endL:end].strip()
                    value = pageContent[searchIndex:startR].strip()
                    output.append(key+"\t"+value)
            searchIndex = startL+1
        except:
            return list(set(output))
    return list(set(output))

from FileUtil import readPlainHtmlPageContent

def entityPatternsTesting(patternsLocation, corpus):
    output         = []
    entityPatterns = readEntityExtractionPatterns(patternsLocation)
    print("Entity patterns are:- ")
    print(entityPatterns)
    for pattern in entityPatterns:
        (lp, rp) = pattern
        for page in corpus:
            pageLocation = page + "/page.html"
            plainHtmlContent = readPlainHtmlPageContent(pageLocation)
            entities = doEntityExtractions(lp, rp, plainHtmlContent)
            output.extend(entities)
    return output

def isHtml(r):
    if "</" in r or ">" in r:
        return True
    else:
        return False

def filteredRelations(relations):
    output = []
    for r in relations:
        if not isHtml(r):
            output.append(r)
    return output
def relationPatternsTesting(patternsLocation, corpus):
    output = []
    relationPatterns = readTripletPatterns(patternsLocation)
    for pattern in relationPatterns:
        (lp, mp, rp) = pattern
        for page in corpus:
            pageLocation     = page + "/page.html"
            plainHtmlContent = readPlainHtmlPageContent(pageLocation)
            relations = doRelationExtractions(lp, mp, rp, plainHtmlContent)
            relations = filteredRelations(relations)
            # for r in relations:
            #     print(r)
            # break
            output.extend(relations)
    return output


def clusterPatternsTesting(patternsLocation, corpus):
    output = []
    clusterPatterns = readTripletPatterns(patternsLocation)
    for pattern in clusterPatterns:
        (lp, mp, rp) = pattern
        for page in corpus:
            pageLocation = page + "/page.html"
            plainHtmlContent = readPlainHtmlPageContent(pageLocation)
            clusters = doClusterExtraction(lp, mp, rp, plainHtmlContent)
            output.extend(clusters)
    return output

from FileUtil import getAllPagesInsideWebsite

websiteLocation = "./supervisedData/amazon"
def doEntityExtractionTesting():
    global websiteLocation
    patternsLocation     = "./supervisedData/amazon/titlePatterns.tsv"
    outputLocation       = "./entityTestingAmazon"
    pages                = getAllPagesInsideWebsite(websiteLocation)
    entities             = entityPatternsTesting(patternsLocation, pages)
    entities = "\n".join(entities)
    with open(outputLocation, "w") as f:
        f.write(entities)
        f.close()
    print("Output written at location:- " + str(outputLocation))

def doRelationExtractionTesting():
    global websiteLocation
    patternsLocation = "./supervisedData/amazon/tablePatterns.tsv"
    outputLocation   = "./relationTestingAmazon"
    pages = getAllPagesInsideWebsite(websiteLocation)
    relations = relationPatternsTesting(patternsLocation, pages)
    relations = "\n".join(relations)
    with open(outputLocation, "w") as f:
        f.write(relations)
        f.close()
    print("Output written at location:- " + str(outputLocation))
# doRelationExtractionTesting()

def doClusterExtractionTesting():
    global websiteLocation
    patternsLocation = "./supervisedData/amazon/specsPatterns.tsv"
    outputLocation   = "./specsTestingAmazon"
    pages = getAllPagesInsideWebsite(websiteLocation)
    clusters = clusterPatternsTesting(patternsLocation, pages)
    clusters = "\n\n".join(clusters)
    with open(outputLocation, "w") as f:
        f.write(clusters)
        f.close()
    print("Output written at location:- " + str(outputLocation))

print("Boom")
doClusterExtractionTesting()
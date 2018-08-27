CONTEXT_LIMIT                 = 100

#just check if everything is inside the cluster context positions
def checkIfAllElementInClusterPresent(pageCluster, clusterElements):
    for c in clusterElements:
        if not c in pageCluster:
            return False
    return True

#it gives me all the possible htmls present inside the html
def getInsideHtmlWithinPageClusterElements(elementList, pageCluster):
    htmlSet = set([])
    if len(elementList)<=0:
        return list(htmlSet)
    startIndex  = len(elementList[0])
    pageCluster = pageCluster[startIndex:]
    for index in range(1, len(elementList)):
        loc = pageCluster.find(elementList[index])
        htmlSet.add(pageCluster[:loc].strip())
        loc+=len(elementList[index])
        pageCluster = pageCluster[loc:]
    return list(htmlSet)

from utils import getLeftIndex, getRightIndex
def getClusterContexts(pageContent, clusterElements):
    #get the first and last element of cluster
    firstEl                 = clusterElements[0]
    lastEl                  = clusterElements[len(clusterElements)-1]
    contexts                = []
    searchLocation          = 0
    rightContextRangeLimit  = len(pageContent)-1
    leftKeyLength           = len(firstEl)
    rightKeyLength          = len(lastEl)
    while(True):
        leftLoc = pageContent.find(firstEl, searchLocation)
        if leftLoc==-1:
            break
        leftContext     = pageContent[getLeftIndex(leftLoc-CONTEXT_LIMIT):leftLoc].strip()
        searchLocation  = leftLoc+1
        rightLocStart   = leftLoc + leftKeyLength
        rightLoc        = pageContent.find(lastEl, rightLocStart)
        if rightLoc==-1:
            break
        rightLocEnd     = rightLoc + rightKeyLength
        rightContext    = pageContent[rightLocEnd:getRightIndex(rightLocEnd + CONTEXT_LIMIT, rightContextRangeLimit)].strip()
        pageCluster     = pageContent[leftLoc:rightLocEnd]
        # print("pagecluster is " + str(pageCluster))
        #once we have the context range and check if we found all entities in this cluster
        statusFoundAll  = checkIfAllElementInClusterPresent(pageCluster, clusterElements)
        # print("status found all:- " + str(statusFoundAll))
        #once we know that all elements are there inside the cluster so there must be 1 element only inside
        insideHtmlList  = getInsideHtmlWithinPageClusterElements(clusterElements, pageCluster)
        print("length of inside html:- " + str(len(insideHtmlList)))
        print(insideHtmlList)
        if statusFoundAll==True and len(insideHtmlList)==1:
            # print("Length of inside html is " + str(len(insideHtmlList)))
            contexts.append((leftContext, insideHtmlList[0], rightContext))
    return contexts
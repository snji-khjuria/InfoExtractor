import os.path
CONTEXT_LIMIT                 = 100

def getLeftIndex(l):
    return max(0, l)

def getRightIndex(r, limit):
    return min(r, limit)

#reverse strings present in list of list elements
def revLeftContexts(lc):
    output = []
    for l in lc:
        output.append(revStrInList(l))
    return output
#reverse all strings present in list
def revStrInList(l):
    output = []
    for item in l:
        output.append(item[::-1])
    return output

def getCommonPrefix(s1, s2):
    l = [s1, s2]
    return os.path.commonprefix(l)

from StringUtil import replaceNumWordsInStr
def processNumInContext(corpusLevelContext):
    output = []
    for seedLevelContext in corpusLevelContext:
        seedLevelOutput = []
        for eachPattern in seedLevelContext:
            patternAsList = list(eachPattern)
            pOutputAsList = []
            for item in patternAsList:
                item = replaceNumWordsInStr(item)
                pOutputAsList.append(item)
            seedLevelOutput.append(tuple(pOutputAsList))
        output.append(seedLevelOutput)
    return output


import csv
def writeTripletPatternsAsCsv(outputLocation, patterns):
    l = []
    l.append(["LeftPattern", "MiddlePattern", "RightPattern", "TextProcessing"])
    for pattern in patterns:
        (lp, mp, rp, textProcessing) = pattern
        l.append([lp, mp, rp, textProcessing])
    with open(outputLocation, "w") as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(l)



def writePairPatternsAsCsv(outputLocation, patterns):
    l = []
    l.append(["LeftPattern", "RightPattern", "TextProcessing"])
    for pattern in patterns:
        (lp, rp, textProcesssing) = pattern
        l.append([lp, rp, textProcesssing])
    with open(outputLocation, "w") as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(l)

import csv
def writePatternsAsCsv(outputLocation, patterns):
    l = []
    l.append(["LeftPattern", "RightPattern", "TextProcessing"])
    for pattern in patterns:
        (lp, rp, textProcessing) = pattern
        l.append([lp, rp, textProcessing])
    with open(outputLocation, "w") as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(l)

def separateLeftMiddleRightContexts(multipleRelationContexts):
    lcs = []
    mcs = []
    rcs = []
    for context in multipleRelationContexts:
        lc = []
        mc = []
        rc = []
        for (a, b, c) in context:
            lc.append(a)
            mc.append(b)
            rc.append(c)
        lcs.append(lc)
        mcs.append(mc)
        rcs.append(rc)
    return (lcs, mcs, rcs)


#get all contexts for key value pair
def getAllContextsForKV(pageContent, key, value, KEY_VALUE_AWAY_LIMIT=100):
    contexts = []
    rightContextRangeLimit = len(pageContent)-1
    leftKeyLength          = len(key)
    rightKeyLength         = len(value)
    searchLocation         = 0
    while(True):
        leftLoc = pageContent.find(key, searchLocation)
        if leftLoc == -1:
            break
        leftContext     = pageContent[getLeftIndex(leftLoc-CONTEXT_LIMIT):leftLoc].strip()
        searchLocation  = leftLoc+1
        rightLocStart   = leftLoc + leftKeyLength
        rightLoc        = pageContent.find(value, rightLocStart)
        if rightLoc==-1:
            break
        rightLocEnd = rightLoc + rightKeyLength
        rightContext = pageContent[rightLocEnd:getRightIndex(rightLocEnd + CONTEXT_LIMIT, rightContextRangeLimit)].strip()
        middleContext = pageContent[rightLocStart:rightLoc].strip()
        if len(middleContext)<=KEY_VALUE_AWAY_LIMIT:
            contexts.append((leftContext, middleContext, rightContext))
    return contexts

def appendPreprocessType(patterns, pType):
    output = []
    for p in patterns:
        p = list(p)
        p.append(pType)
        output.append(tuple(p))
    return output


CONTEXT_LIMIT                 = 100
#get contexts for single object
def getSingleObjectContexts(pageContent, singleObject):
    contexts                 = []
    searchLocation           = 0
    rightContextRangeLimit   = len(pageContent)-1
    keyLength                = len(singleObject)
    while(True):
        loc = pageContent.find(singleObject, searchLocation)
        if loc==-1:
            break
        rightLocStart = loc + keyLength
        leftContext = pageContent[getLeftIndex(loc-CONTEXT_LIMIT):loc].strip()
        rightContext = pageContent[rightLocStart:getRightIndex(rightLocStart+CONTEXT_LIMIT, rightContextRangeLimit)].strip()
        contexts.append((leftContext, rightContext))
        searchLocation = loc+1
    return contexts


def segmentPairContexts(contexts):
    lcs = []
    rcs = []
    for c in contexts:
        lc = []
        rc = []
        for (a, b) in c:
            lc.append(a)
            rc.append(b)
        lcs.append(lc)
        rcs.append(rc)
    return (lcs, rcs)

def initTable(e1, e2):
    table = []
    for i in range(len(e1)):
        row = []
        for j in range(len(e2)):
            row.append("EMPTY")
        table.append(row)
    return table


def findStringPattern(expr1, expr2):
    table = initTable(expr1, expr2)
    return findCommonRegExp(expr1, expr2, 0, 0, table)

import re
def countLength1Substr(s):
    [m.start() for m in re.finditer('\*', s)]

def filterStarPattern(s):
    startResults  = [m.start() for m in re.finditer('\*', s)]
    substrs = [startResults[i] - startResults[i-1]-1 for i in range(1, len(startResults))]
    components = []
    prevIndex=0
    while prevIndex<len(substrs) and substrs[prevIndex]>3:
        prevIndex+=1
    nextIndex=prevIndex+1
    componentLength=1
    while nextIndex<len(substrs):
        if substrs[nextIndex]<=3:
            componentLength+=1
            nextIndex+=1
        else:
            components.append(componentLength)
            componentLength=0
            nextIndex+=1
    if componentLength!=0:
        components.append(componentLength)
    results = [True if item>4 else False for item in components]
    # return False
    return results.count(True)>=1

def starPatternMerging(pattern):
    position = pattern.find('*')
    if position==-1:
        return pattern
    output = pattern[:position]
    while True:
        nextPosition = pattern.find('*', position+1)
        if nextPosition==-1:
            break
        if nextPosition-position>3:
            output+=pattern[position:nextPosition]
        position=nextPosition
    output+=pattern[position:]
    return output

#if the leftmost pattern has atleast 3 characters(>2) on its left
def leftPatternPreprocessing(pattern):
    position = pattern.find('*')
    if position==-1 or position>2:
        return pattern
    else:
        return pattern[position+1:]


def filterLeftPattern(s):
    if s[len(s)-1]=='*':
        return True
    else:
        return False

def filterRightPattern(s):
    if s[0]=='*':
        return True
    else:
        return False

def pickBestLeftPatterns(patterns):
    output = []
    for p in patterns:
            if filterLeftPattern(p)==False:
                output.append(leftPatternPreprocessing(starPatternMerging(p)))
    return output

#if the rightmost star  is having atleast 3(>2) characters on its right go for it
def rightPatternPreprocessing(pattern):
    position = pattern.rfind('*')
    if position==-1 or len(pattern)-1-position>2:
        return pattern
    else:
        return pattern[:position]

def pickBestRightPatterns(patterns):
    output = []
    for p in patterns:
        if filterRightPattern(p)==False:
            # output.append(p)
            output.append(rightPatternPreprocessing(starPatternMerging(p)))
    return output

def filterMiddlePattern(s):
    if s[0]=='*' or s[len(s)-1]=='*':
        return True
    else:
        return False


def pickBestMiddlePatterns(patterns):
    # return patterns
    output = []
    for p in patterns:
        if filterMiddlePattern(p)==False:
            output.append(starPatternMerging(p))
    return output

def findStringPatternWithList(e1, l1):
    output = ""
    for item in l1:
        r = findStringPattern(e1, item)
        if len(r)-r.count("*")>len(output)-output.count("*"):
            output = r
    return output

def findListToListPattern(l1, l2):
    output = []
    for item in l1:
        output.append(findStringPatternWithList(item, l2))
    return output


def findCommonRegExp(expr1, expr2, i, j, table):
    if i==len(expr1) or j==len(expr2):
        return ""
    entry = table[i][j]
    if entry!="EMPTY":
        return entry
    if expr1[i]==expr2[j]:
        s = findCommonRegExp(expr1, expr2, i+1, j+1, table)
        table[i][j] = expr1[i]+s
        return table[i][j]
    else:
        s1 = findCommonRegExp(expr1, expr2, i+1, j, table)
        s2 = findCommonRegExp(expr1, expr2, i, j+1, table)
        if len(s1)>0 and s1[0]!='*':
            s1 = "*"+s1
        if len(s2)>0 and s2[0]!='*':
            s2 = "*"+s2
        l1 = len(s1) - s1.count("*")
        l2 = len(s2) - s2.count("*")
        if l1>l2:
            table[i][j] = s1
        elif l2>l1:
            table[i][j] = s2
        else:
            if s1.count("*")>s2.count("*"):
                table[i][j] = s2
            else:
                table[i][j] = s1

        return table[i][j]

from utils import revLeftContexts, revStrInList

def patternTypeSeparator(contexts):
    hashTable = {}
    totalSeeds = len(contexts)
    for c in contexts:
        for item in c:
            if not item in hashTable:
                hashTable[item] = 1
            else:
                hashTable[item] += 1
    patterns = []
    seedSpecificContexts = []
    for (k, v) in hashTable.items():
        if v == totalSeeds:
            patterns.append(k)
        else:
            seedSpecificContexts.append(k)
    seedSpecificContexts = set(seedSpecificContexts)
    resultingContexts = []
    for c in contexts:
        intersected = list(set(c) & seedSpecificContexts)
        if len(intersected)>0:
            resultingContexts.append(intersected)
    return patterns, resultingContexts

def compareLLs(lc, resultingContexts):
    for index in range(0, len(lc)):
        l1 = set(lc[index])
        l2 = set(resultingContexts[index])
        if l1!=l2:
            print("NOtOkay")
            print(index)
            return False

    return True

def compressLeftContexts(lc):
    patterns, resultingContexts = patternTypeSeparator(lc)
    if len(resultingContexts)==0:
        return patterns
    revLC = revLeftContexts(resultingContexts)
    l1    = revLC[0]
    for index in range(1, len(revLC)):
        l1 = findListToListPattern(l1, revLC[index])
    l1    = revStrInList(l1)
    patterns.extend(l1)
    return pickBestLeftPatterns(patterns)

def compressRightContexts(rc):
    patterns, resultingContexts = patternTypeSeparator(rc)
    if len(resultingContexts)==0:
        return patterns
    l1 = resultingContexts[0]
    for index in range(1, len(resultingContexts)):
        l1 = findListToListPattern(l1, resultingContexts[index])
    patterns.extend(l1)
    return pickBestRightPatterns(patterns)

def compressMiddleContexts(mc):
    patterns, resultingContexts = patternTypeSeparator(mc)
    if len(resultingContexts)==0:
        return patterns
    l1 = resultingContexts[0]
    for index in range(1, len(resultingContexts)):
        l1 = findListToListPattern(l1, resultingContexts[index])
    patterns.extend(l1)
    return pickBestMiddlePatterns(patterns)
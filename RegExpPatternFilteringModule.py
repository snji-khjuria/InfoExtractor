import re
def removeRegExpStar(s):
    old = re.compile("\*")
    new = "STAR"
    return re.sub(old, new, s)
def getRegExpStarBack(s):
    old = re.compile("STAR")
    #? is for non-greedy regex nature
    new = ".*?"
    return re.sub(old, new, s)

def getAllPatternLocations(pattern, s):
    regexp = re.compile("(?=" + pattern + ")")
    output = []
    for m in regexp.finditer(s):
        startPos = m.start()
        sObj = re.search(pattern, s[startPos:])
        endPos   = startPos + sObj.end()
        output.append((startPos, endPos))
    return output

#find entity set in left and right pattern.
def makeSingleObjectExtractions(pageContent, leftPattern, rightPattern, threshold=1000):
    output = []
    leftPattern  = getRegExpStarBack(re.escape(removeRegExpStar(leftPattern)))
    rightPattern = getRegExpStarBack(re.escape(removeRegExpStar(rightPattern)))
    leftPatternsLocation = getAllPatternLocations(leftPattern, pageContent)
    for (startL, endL) in leftPatternsLocation:
        rpLoc = re.search(rightPattern, pageContent[endL:])
        if not rpLoc is None:
            element = pageContent[endL:endL+rpLoc.start()]
            if len(element)<=threshold:
                output.append(element.strip())
    return list(set(output))

from FileUtil import getAllPagesInsideWebsite, readFileContentInList
from FileUtil import readPlainHtmlPageContent



def patternsWithEveryMatch(stats):
    output = []
    for patternId, patternResults in stats.items():
        flagPattern=True
        (pattern, patternResults) = patternResults
        for patternResult in patternResults:
            (computed, expected, expectedArtificial) = patternResult
            computed           = set(computed)
            expected           = set(expected)
            expectedArtificial = set(expectedArtificial)
            if computed!=expected or computed!=expectedArtificial:
                flagPattern=False
        if flagPattern==True:
            output.append(pattern)
    return output
from bs4 import BeautifulSoup

def isHtmlString(item):
    return bool(BeautifulSoup(item, "html.parser").find())

def setContainsHtml(s):
    for item in s:
        if isHtmlString(item):
            return True
    return False

def patternsWithNonHtmlMatches(stats):
    output = []
    for patternId, patternResults in stats.items():
        flagPattern=True
        (pattern, patternResults) = patternResults
        for patternResult in patternResults:
            (computed, expected, expectedArtificial) = patternResult
            computed = set(computed)
            expected = set(expected)
            expectedArtificial = set(expectedArtificial)
            intersected = expectedArtificial & computed
            if len(intersected)==0 or setContainsHtml(computed) :
                flagPattern=False
                break
            # else:
            #     print("Expected was")
            #     print(expectedArtificial)
            #     print("Computed was")
            #     print(computed)
            #     print()
        if flagPattern==True:
            output.append(pattern)
    return output

def patternsWithMatchingSomething(stats):
    output = []
    for patternId, patternResults in stats.items():
        flagPattern = False
        (pattern, patternResults) = patternResults
        for patternResult in patternResults:
            (computed, expected, expectedArtificial) = patternResult
            computed           = set(computed)
            expected           = set(expected)
            expectedArtificial = set(expectedArtificial)
            intersected = computed & expectedArtificial
            if len(intersected)>0:
                flagPattern = True
                break
        if flagPattern == True:
            output.append(pattern)
    return output


def getPatternsFromStats(stats):
    fullMatchPatterns = patternsWithEveryMatch(stats)
    print("Full match patterns")
    print(fullMatchPatterns)
    if len(fullMatchPatterns)!=0:
        return fullMatchPatterns
    nonHtmlMatches    = patternsWithNonHtmlMatches(stats)
    print("Non html patterns")
    print(nonHtmlMatches)
    if len(nonHtmlMatches)!=0:
        return nonHtmlMatches
    nonEmptyMatches   = patternsWithMatchingSomething(stats)
    print("Non empty matches")
    print(nonEmptyMatches)
    return nonEmptyMatches

def singleObjectPatternFiltering(patterns, websiteLocation, supervisedFileLocation, artificialSeedSet, threshold=1000, preprocessType="None"):
    stats = {}
    output = []
    patternIndex  = 0
    for pattern in patterns:
        pages = getAllPagesInsideWebsite(websiteLocation)
        resultsPerPattern = []
        patternIndex+=1
        for page in pages:
            (lp, rp) = pattern
            exactPageLocation = page + "/page.html"
            contentList = readFileContentInList(page + "/" + supervisedFileLocation)
            singleObj = ""
            if len(contentList) == 1:
                singleObj = contentList[0]
            goldContent   = " ".join(singleObj.split())
            expected     = [goldContent]
            pageContent   = readPlainHtmlPageContent(exactPageLocation)
            computed      = makeSingleObjectExtractions(pageContent, lp, rp, threshold)
            resultsPerPattern.append((computed, expected, artificialSeedSet[page]))
        stats[patternIndex] = (pattern, resultsPerPattern)
    patterns = getPatternsFromStats(stats)
    return patterns

# def singleObjectPatternFiltering(patterns, websiteLocation, supervisedFileLocation, preprocessType="None"):
#     output = []
#     for pattern in patterns:
#         (lp, rp) = pattern
#         pages = getAllPagesInsideWebsite(websiteLocation)
#         patternScore = 0
#         for page in pages:
#             exactPageLocation = page + "/page.html"
#             contentList = readFileContentInList(page + "/" + supervisedFileLocation)
#             singleObj = ""
#             if len(contentList) == 1:
#                 singleObj = contentList[0]
#             goldContent = " ".join(singleObj.split())
#             pageContent = readPlainHtmlPageContent(exactPageLocation)
#             results     = makeSingleObjectExtractions(pageContent, lp, rp)
#             if len(results)>0:
#                 if goldContent in results:
#                     patternScore+=1
#         if patternScore >= 0:
#             output.append((lp, rp))
#     return output



#################Entity filtering ends#################################
#######################################################################
from FileUtil import readFileRelationContentInList
def multipleRelationFiltering(patterns, websiteLocation, supervisedFileLocation, artificialSeeds, preprocessType="None"):
    stats = {}
    patternIndex  = 0
    for pattern in patterns:
        pages = getAllPagesInsideWebsite(websiteLocation)
        resultsPerPattern = []
        patternIndex+=1
        for page in pages:
            artificialSeedsPerPage = artificialSeeds[page]
            (lp, mp, rp) = pattern
            exactPageLocation = page + "/page.html"
            contentList       = readFileRelationContentInList(page + "/" + supervisedFileLocation)
            expected          = [k.strip() + " " + v.strip() for (k, v) in contentList]
            expected          = [" ".join(item.split()) for item in expected]
            pageContent       = readPlainHtmlPageContent(exactPageLocation)
            computed          = getAllRelations(lp, mp, rp, pageContent)
            computed          = [k.strip() + " " + v.strip() for (k, v) in computed]
            computed          = [" ".join(item.split()) for item in computed]
            artificialPerPage = [k.strip() + " " + v.strip() for (k, v) in artificialSeeds[page]]
            artificialPerPage = [" ".join(item.split()) for item in artificialPerPage]
            resultsPerPattern.append((computed, expected, artificialPerPage))
            stats[patternIndex] = (pattern, resultsPerPattern)
        patterns = getPatternsFromStats(stats)
    return patterns



def getAllRelations(leftPattern, middlePattern, rightPattern, pageContent):
    searchIndex = 0
    output = []
    mp = middlePattern
    rp = rightPattern
    leftPattern   =  getRegExpStarBack(re.escape(removeRegExpStar(leftPattern)))
    middlePattern =  getRegExpStarBack(re.escape(removeRegExpStar(middlePattern)))
    rightPattern  =  getRegExpStarBack(re.escape(removeRegExpStar(rightPattern)))
    leftPatternsLocation = getAllPatternLocations(leftPattern, pageContent)
    for (startL, endL) in leftPatternsLocation:
        mLoc = re.search(middlePattern, pageContent[endL:])
        if not mLoc is None:
            startM = endL + mLoc.start()
            endM   = endL + mLoc.end()
            key    = pageContent[endL:startM].strip()
            rLoc = re.search(rightPattern, pageContent[endM:])
            if not rLoc is None:
                startR = endM + rLoc.start()
                # endR   = endM + rLoc.end()
                value  = pageContent[endM:startR].strip()
                if len(key) <= 1000 and len(value) <= 1000:
                    output.append((key, value))
    return list(set(output))
###############################################################
###############Cluster extraction code#########################

def clusterPatternFiltering(patterns, websiteLocation, supervisedFileLocation, artificialClusters, preprocessType="None"):
    stats = {}
    output = []
    patternIndex  = 0
    for pattern in patterns:
        pages = getAllPagesInsideWebsite(websiteLocation)
        resultsPerPattern = []
        patternIndex+=1
        for page in pages:
            (lp, mp, rp) = pattern
            exactPageLocation = page + "/page.html"
            # contentList = getClusterInsideLeftRightPattern(pageContent)
            contentList = readFileContentInList(page + "/" + supervisedFileLocation)
            contentList = [" ".join(item.split()) for item in contentList]
            expected    = contentList
            expectedArtificial = artificialClusters[page]
            expectedArtificial = [" ".join(item.split()) for sublist in expectedArtificial for item in sublist]
            pageContent   = readPlainHtmlPageContent(exactPageLocation)
            clusters      = getClusterInsideLeftRightPattern(pageContent, lp, mp, rp)
            computed      = []
            for cluster in clusters:
                computed.extend(getElementsOfCluster(cluster, mp))
            # print("Expected is ")
            # print(expected)
            # print("expected Artificial is ")
            # print(expectedArtificial)
            # print("Computed is ")
            # print(computed)
            resultsPerPattern.append((computed, expected, expectedArtificial))
        stats[patternIndex] = (pattern, resultsPerPattern)
    patterns = getPatternsFromStats(stats)
    return patterns


def getClusterInsideLeftRightPattern(pageContent, leftPattern, insidePattern, rightPattern):
    output = []
    leftPattern   = getRegExpStarBack(re.escape(removeRegExpStar(leftPattern)))
    insidePattern = getRegExpStarBack(re.escape(removeRegExpStar(insidePattern)))
    rightPattern = getRegExpStarBack(re.escape(removeRegExpStar(rightPattern)))
    leftPatternsLocation = getAllPatternLocations(leftPattern, pageContent)
    for (startL, endL) in leftPatternsLocation:
        rpLoc = re.search(rightPattern, pageContent[endL:])
        if not rpLoc is None:
            cluster = pageContent[endL:endL+rpLoc.start()]
            if len(cluster)<=30000 and not re.search(insidePattern, cluster) is None:
                output.append(cluster)
    return list(set(output))

def getElementsOfCluster(cluster, insidePattern):
    insidePattern = getRegExpStarBack(re.escape(removeRegExpStar(insidePattern)))
    output = []
    patternsLocation = getAllPatternLocations(insidePattern, cluster)
    ePrev = 0
    for (s, e) in patternsLocation:
        output.append(cluster[ePrev:s].strip())
        ePrev = e
    if len(cluster) - ePrev>0:
        output.append(cluster[ePrev:].strip())
    return output


########################Cluster filtering module##############################
#############################################################################
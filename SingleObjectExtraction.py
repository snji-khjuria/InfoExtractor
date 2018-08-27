supervisedDataLocation        = "./supervisedData"
supervisedFileName            = "productTitle"
patternsOutputLocation        = "titlePatterns.tsv"
from utils import getLeftIndex, getRightIndex, revStrInList
from utils import segmentPairContexts

def getPatternScore(output, gold):
    # scoreAssigned = 100
    oSet = set(output)
    gSet = set(gold)
    cSet = oSet & gSet
    cSetSize = len(cSet)
    if cSetSize==0:
        return -100
    scoreAssigned = cSetSize*10
    return scoreAssigned





# from PatternsFilteringModule import singleObjectPatternFiltering
from RegExpPatternFilteringModule import singleObjectPatternFiltering

from FileUtil import getWebsiteLocations
from FileUtil import getAllPagesInsideWebsite, readPlainHtmlPageContent
from FileUtil import readFileContentInList
from utils import getSingleObjectContexts, writePairPatternsAsCsv
from SingleObjectPatternsLearningUtil import  learnPatterns
from utils import appendPreprocessType
from utils import  processNumInContext
from SeedExpansionModule import addArtificialSeeds

websiteLocations = getWebsiteLocations(supervisedDataLocation)
print(websiteLocations)
for websiteLocation in websiteLocations:
    pages                = getAllPagesInsideWebsite(websiteLocation)
    singleObjectContexts = []
    singleObjList        = []
    artificialSeedSet    = {}
    for page in pages:
        exactPageLocation = page + "/page.html"
        contentList       = readFileContentInList(page + "/" + supervisedFileName)
        singleObj         = ""
        if len(contentList)==1:
            singleObj = contentList[0]
        #so that multiple spaces in product title are being removed
        singleObj                = " ".join(singleObj.split())
        pageContent              = readPlainHtmlPageContent(exactPageLocation)
        # print("Real seed was:- ")
        # print(singleObj)
        artificialSeedSetPerPage = addArtificialSeeds(pageContent, singleObj)
        # print("Artificial seeds are:- ")
        # print(artificialSeedSetPerPage)
        contextsPerPage          = []
        for seed in artificialSeedSetPerPage:
            cPerPagePerSeed      = getSingleObjectContexts(pageContent, seed)
            if len(cPerPagePerSeed)>0:
                contextsPerPage.extend(cPerPagePerSeed)
        if len(contextsPerPage)>0:
            singleObjectContexts.append(contextsPerPage)
        singleObjList.append(singleObj)
        artificialSeedSet[page] = artificialSeedSetPerPage
    print("You know what...")
    print("Single object contexts are:- ")
    print(singleObjectContexts)
    patterns         = learnPatterns(singleObjectContexts)

    filteredPatterns = patterns
    # print("Finally we have learnt the patterns...")
    filteredPatterns = singleObjectPatternFiltering(patterns, websiteLocation, supervisedFileName, artificialSeedSet)
    filteredPatterns = appendPreprocessType(filteredPatterns, "None")
    print("Patterns are:- ")
    print(patterns)
    print("FilteredPatterns are:- ")
    print(filteredPatterns)
    # filteredPatterns = patterns
    # filteredPatterns.extend(numProcessedPatterns)
    writePairPatternsAsCsv(websiteLocation+"/" + patternsOutputLocation, filteredPatterns)
    print("Patterns written at:- " + websiteLocation + "/" + patternsOutputLocation)


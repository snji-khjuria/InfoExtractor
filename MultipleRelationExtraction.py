#global variables section
supervisedDataLocation        = "./supervisedData"
supervisedFileName            = "productTables"
patternsOutputLocation        = "tablePatterns.tsv"
KEY_VALUE_AWAY_LIMIT          = 100


#essential imports
from SeedExpansionModule import addArtificialKeyValueSeeds
from utils    import writeTripletPatternsAsCsv, getAllContextsForKV
from FileUtil import getWebsiteLocations, getAllPagesInsideWebsite, readPlainHtmlPageContent
from FileUtil import readFileRelationContentInList
from RelationPatternsLearningUtil import learnPatterns
from RegExpPatternFilteringModule import multipleRelationFiltering
from utils import processNumInContext
#get all the locations for website so that we can start extracting the patterns for them.
websiteLocations = getWebsiteLocations(supervisedDataLocation)
print(websiteLocations)
from utils import appendPreprocessType
#work for each website independently
for websiteLocation in websiteLocations:
    pages                    = getAllPagesInsideWebsite(websiteLocation)
    corpusLevelRelationContext = []
    artificialSeeds = {}
    for page in pages:
        exactPageLocation = page + "/page.html"
        print("Exact page location:- ")
        print(exactPageLocation)
        #also can be called as supervision of relations
        supervisedRelationList        = readFileRelationContentInList(page+"/"+supervisedFileName)
        allRelationContextsPerPage    = []
        pageContent = readPlainHtmlPageContent(exactPageLocation)
        artificialSeedPerPage = []
        for supervisedRelation in supervisedRelationList:
            (key, value)               = supervisedRelation
            potentialArtificialSeedsPerKV       = addArtificialKeyValueSeeds(pageContent, (key, value))
            contextsPerRelation  = []
            artificialSeedsPerKV = []
            for (k, v) in potentialArtificialSeedsPerKV:
                contextPerArtificialRelation = getAllContextsForKV(pageContent, k, v, KEY_VALUE_AWAY_LIMIT)
                if len(contextPerArtificialRelation)>0:
                    artificialSeedsPerKV.append((k, v))
                    contextsPerRelation.extend(contextPerArtificialRelation)
            artificialSeedPerPage.extend(artificialSeedsPerKV)
            # print("True kv is ")
            # print("Key value is " + str(key + " " + value))
            # av = "\n".join([k + "\t" + v for (k, v) in artificialSeedsPerKV])
            # print("Artificial is ")
            # print(av)
            # contextsPerRelation = getAllContextsForKV(pageContent, key, value, KEY_VALUE_AWAY_LIMIT)
            #if condition to ignore the number of contexts.
            if len(contextsPerRelation)<=0:
                continue
            # print("Contexts per relation are:- ")
            # print(contextsPerRelation)
            allRelationContextsPerPage.append(contextsPerRelation)
        artificialSeeds[page] = artificialSeedPerPage
        corpusLevelRelationContext.extend(allRelationContextsPerPage)
    print("Multiple relation contexts are:- ")
    print("This is design choice to keep tables from all the pages belong to big table set")
    print("At this stage we have all the relation contexts present...")
    print("Relation contexts are list of lists per tuple....")
    #[[(left, middle, right)], [(l, m, r), (l, m, r)]]
    print(corpusLevelRelationContext)
    print("We are gonna learn patterns for this set of contexts...")
    patterns                               = learnPatterns(corpusLevelRelationContext)
    filteredPatterns = multipleRelationFiltering(patterns, websiteLocation, supervisedFileName, artificialSeeds)

    patterns = appendPreprocessType(patterns, "None")
    writeTripletPatternsAsCsv(websiteLocation + "/" + patternsOutputLocation, patterns)
    # writeTripletPatternsAsCsv(websiteLocation + "/" + patternsOutputLocation, patterns)
    print("Patterns written at location:- " + websiteLocation + "/" + patternsOutputLocation)

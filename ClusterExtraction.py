supervisedDataLocation        = "./supervisedData"
supervisedFileName            = "productSpecs"
patternsOutputLocation        = "specsPatterns.tsv"

from FileUtil import getWebsiteLocations
from FileUtil import getAllPagesInsideWebsite, readPlainHtmlPageContent
from FileUtil import readFileContentInList
from ClusterExtractionUtil import learnPatterns
from utils import writeTripletPatternsAsCsv
from ClusterContextExtraction import getClusterContexts
from RegExpPatternFilteringModule import clusterPatternFiltering
from utils import appendPreprocessType, processNumInContext
from SeedExpansionModule import addArtificialClusterSeeds
websiteLocations = getWebsiteLocations(supervisedDataLocation)
print(websiteLocations)
for websiteLocation in websiteLocations:
    pages                = getAllPagesInsideWebsite(websiteLocation)
    contexts             = []
    artificialClusters = {}
    for page in pages:
        print(page)
        print(websiteLocation)
        exactPageLocation = page + "/page.html"
        clusterElements   = readFileContentInList(page + "/" + supervisedFileName)
        pageContent = readPlainHtmlPageContent(exactPageLocation)
        contextsPerPage = getClusterContexts(pageContent, clusterElements)
        contexts.append(contextsPerPage)
        artificialClusterPerPage = addArtificialClusterSeeds(pageContent, clusterElements)
        artificialClusters[page]  = artificialClusterPerPage
        realCluster = "\n".join(clusterElements)
        # print("Real Cluster is ")
        # print(realCluster)
        # artificialCluster = ["\n".join(cluster) for cluster in artificialClusterPerPage]
        # artificialCluster = "\n\n\n".join(artificialCluster)
        # print("Artificial Cluster is ")
        # print(artificialCluster)
        # print("Real cluster")
        # realCluster = "\n".join(clusterElements)
        # print(realCluster)
        # print("Artificial cluster")
        # print(artificialSeedSetPerPage)
    patterns = learnPatterns(contexts)
    patterns = clusterPatternFiltering(patterns, websiteLocation, supervisedFileName, artificialClusters)
    patterns = appendPreprocessType(patterns, "None")
    writeTripletPatternsAsCsv(websiteLocation + "/" + patternsOutputLocation, patterns)
    print("Patterns written at location:- " + websiteLocation + "/" + patternsOutputLocation)
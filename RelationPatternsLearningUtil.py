FULL_PATTERN_LENGTH_THRESHOLD = 10
from utils import separateLeftMiddleRightContexts
# from GeneralPatternExtractionUtil import compressLeftContexts, compressMiddleContexts
# frsom GeneralPatternExtractionUtil import compressRightContexts
from RegExpPatternExtractionUtil import compressLeftContexts, compressRightContexts
from RegExpPatternExtractionUtil import compressMiddleContexts

def printll(ll):
    for l in ll:
        print(l)

def learnPatterns(multipleRelationContexts):
    (lcs, mcs, rcs) = separateLeftMiddleRightContexts(multipleRelationContexts)
    summarizedLeftContexts    = compressLeftContexts(lcs)
    summarizedMiddleContexts  = compressMiddleContexts(mcs)
    summarizedRightContexts   = compressRightContexts(rcs)
    output = []
    for left in summarizedLeftContexts:
        for middle in summarizedMiddleContexts:
            for right in summarizedRightContexts:
                if len(left) + len(middle) + len(right) > FULL_PATTERN_LENGTH_THRESHOLD:
                    output.append((left, middle, right))
    return list(set(output))
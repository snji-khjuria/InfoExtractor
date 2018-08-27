# from GeneralPatternExtractionUtil import compressLeftContexts, compressMiddleContexts
# from GeneralPatternExtractionUtil import  compressRightContexts
from RegExpPatternExtractionUtil import compressLeftContexts, compressMiddleContexts
from RegExpPatternExtractionUtil import  compressRightContexts

from utils import separateLeftMiddleRightContexts
FULL_PATTERN_LENGTH_THRESHOLD = 10

def learnPatterns(contexts):
    (lcs, mcs, rcs)        = separateLeftMiddleRightContexts(contexts)
    summarizedLeftContexts = compressLeftContexts(lcs)
    summarizedMiddleContexts = compressMiddleContexts(mcs)
    summarizedRightContexts = compressRightContexts(rcs)
    output = []
    for left in summarizedLeftContexts:
        for middle in summarizedMiddleContexts:
            for right in summarizedRightContexts:
                if len(left) + len(middle) + len(right) > FULL_PATTERN_LENGTH_THRESHOLD:
                    output.append((left, middle, right))
    return list(set(output))


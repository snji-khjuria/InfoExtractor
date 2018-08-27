from utils import getCommonPrefix


#########################################
# complex algorithm section starts

# how to insert common prefix into results list
def insertCommonPrefix(results, commonPrefix):
    # if common prefix is in results don't do anything
    if commonPrefix in results or len(commonPrefix) <= 0:
        return results
    r = list(results)
    # if any item has lesser length and starts with my new pattern remove it
    # and will later insert new commonprefix
    # here we go
    for item in r:
        if len(item) < len(commonPrefix) and commonPrefix.startswith(item):
            results.remove(item)
    # now we have list where no element smaller than current is present
    r = list(results)

    # if any item has length more than me and starts with me return previous results
    # and finally add my new commonprefix
    for item in r:
        if len(item) > len(commonPrefix) and item.startswith(commonPrefix):
            return results
    # if that element was not present in list so insert it otherwise we have already left
    # this function in above line
    results.add(commonPrefix)
    return results


# FAILURE REASON:- could be because no intersection between 2 components's prefix
# TODO: figure out way to deal with it...not done so far and code is working OKish even without it

# do prefix summarization of 2 lists
# for each element of l1 get max intersection with l2
# whatever is the max intersection now insert it in your final answers
# we have to insert common prefix for all of the elements of list1
def doPrefixSummarization(list1, list2):
    results = set()
    for item1 in list1:
        commonPrefix = ""
        for item2 in list2:
            c = getCommonPrefix(item1, item2)
            # print("Common prefix is ")
            # print(c)
            if len(c) > len(commonPrefix):
                commonPrefix = c
        results = insertCommonPrefix(results, commonPrefix)
    return results


def summarizeContexts(contexts):
    if len(contexts) <= 0:
        return contexts
    # whatever is present in context of first tuple is my summarization
    result = contexts[0]
    # for list of contexts related to each other triple do the summarization of
    # that triple with me and get the result
    # basically the prefix summarization is connected to 2 lists
    for index in range(1, len(contexts)):
        result = doPrefixSummarization(result, contexts[index])
    return list(result)


# complex algorithm section ends
#################################################################


from utils import revLeftContexts, revStrInList

#compressing the left patterns is all about reversing the patterns initially apply the above algorithm
#and now reverse the patterns again
#we have set of indepdendent contexts available to us
def compressLeftContexts(lc):
    revLC = revLeftContexts(lc)
    reversedSummarizedContexts = summarizeContexts(revLC)
    summarizedLeftContexts = revStrInList(reversedSummarizedContexts)
    return summarizedLeftContexts



#compressing the middle patterns only means to get single context set in the middle contexts
#now we just have set of potential middle contexts available to us
def compressMiddleContexts(contexts):
    output = []
    for context in contexts:
        output.extend(context)
    return list(set(output))

#compressing the right contextt is simply get summarization for each of the context independently
def compressRightContexts(rc):
    return summarizeContexts(rc)


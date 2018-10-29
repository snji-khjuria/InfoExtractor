import re
def replaceMultiWhitespaceWithSingle(str):
    # return str
    return re.sub('\s+', ' ', str).strip()


def replaceHtmlTags(str):
    notspace =  re.sub('&nbsp;', ' ', str).strip()
    notAmp   = re.sub('&amp;', '&', notspace).strip()
    notQuot  = re.sub('&quot;', '\"', notAmp).strip()
    notEscape = re.sub('\\\\"', '"', notQuot).strip()
    return notEscape

def replaceNumWordsInStr(s):
    return re.sub("(<[\s\S]*?)[ \"\'=:]\d+[ \"\']([\s\S]*?>)", r"\1 NUM \2", s)

# def replaceNumWordsInStr(s):
#     return re.sub("[ \"\'=:]\d+[ \"\']", " NUM ", s)


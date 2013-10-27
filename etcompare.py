"""
comparing two elementtrees for xml equivalence, 
from http://stackoverflow.com/questions/7905380/testing-equivalence-of-xml-etree-elementtree
removed the .tail comparisons (that's the whitespace between the tags i think)
"""

def cmp_el(a,b):
    #print a.tag, b.tag
    #print a.tail, b.tail
    #print "(0)"

    if a.tag < b.tag:
        return -1
    elif a.tag > b.tag:
        return 1
    #we're only interested in the tags - not the stuff in-between
    #elif a.tail < b.tail:
    #    return -1
    #elif a.tail > b.tail:
    #    return 1

    #print "(a)"

    #compare attributes
    aitems = a.attrib.items()
    aitems.sort()
    bitems = b.attrib.items()
    bitems.sort()
    if aitems < bitems:
        return -1
    elif aitems > bitems:
        return 1

    #print "(b)"

    #compare child nodes
    achildren = list(a)
    achildren.sort(cmp=cmp_el)
    bchildren = list(b)
    bchildren.sort(cmp=cmp_el)

    for achild, bchild in zip(achildren, bchildren):
        cmpval = cmp_el(achild, bchild)
        if  cmpval < 0:
            return -1
        elif cmpval > 0:
            return 1    

    #print "(c)"

    #must be equal 
    return 0

def el_equal(a, b):
    #for tree equivality was like this but then didn't need trees.. (yet?)
    #return cmp_el(a.getroot(), b.getroot()) == 0
    return cmp_el(a, b) == 0

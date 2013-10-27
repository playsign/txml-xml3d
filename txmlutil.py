#t = ElementTree()
#s = t.parse(sys.argv[1])
#ents = s.getiterator("entity")

def attrval(el, attrname):
    attr = el.find(".//attribute[@name='%s']" % attrname)
    return attr.attrib['value']

def floatlist(el, attrname):
    return [float(v) for v in attrval(el, attrname).split(',')]

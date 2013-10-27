from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET

import txmlutil

door_txml = """
<component type="EC_DynamicComponent" sync="1" name="door">
   <attribute value="true" type="bool" name="opened"/>
   <attribute value="false" type="bool" name="locked"/>
</component>
"""

#should we call this 'dom': ec attrs as dom attrs, comps as xml (dom?) elements
door_xml3d = '<door locked="false" opened="true" />'
#<door opened="true" locked="false" />
#was lazy and hacked the order - should use some xmldiff
#.. switch the attr order when do, to match the txml one - clearer to read

def txml_to_xml3d(txml_doc):
    root = ET.fromstring(txml_doc)
    #tree = ElementTree(root) #thanks http://stackoverflow.com/questions/647071/python-xml-elementtree-from-a-string-source #.. ah but not needed (yet)

    #xml3d_tree = ElementTree()
    xml3d_elem = None
    if root.tag == 'component':
        comp = root
        ec_type = comp.attrib['type']
        #txmlutil.attrval(comp, 'type')
        if ec_type == "EC_DynamicComponent":
            dc_type = comp.attrib['name']
            xml3d_elem = ET.Element(dc_type)
            #ET.SubElement(xml3d_comp)

            ec_attrs = comp.getiterator('attribute')
            for attr in ec_attrs:
                attr_name = attr.attrib['name']
                attr_val = attr.attrib['value']
                xml3d_elem.attrib[attr_name] = attr_val

    xml3d_doc = ET.tostring(xml3d_elem)
    #xml3d_doc = ET.tostring(xml3d_tree)
    return xml3d_doc

def test_txml_to_xml3d(txml_doc, ref_xml3d_doc):
    xml3d_doc = txml_to_xml3d(txml_doc)
    print txml_doc
    print " ====> "
    print xml3d_doc
    print " ----- "
    print ref_xml3d_doc
    assert xml3d_doc == ref_xml3d_doc

def test():
    test_txml_to_xml3d(door_txml, door_xml3d)

if __name__ == '__main__':
    test()

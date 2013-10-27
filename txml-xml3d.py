from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET

import txmlutil
import etcomp

#copy-pasted & cleaned from:
#https://github.com/realXtend/naali/blob/tundra/bin/scenes/Door/door.txml
door_txml = """
<entity id="1">
  <component type="EC_Mesh" sync="1">
   <attribute value="0,0,0,90,0,180,1,1,1" name="Transform"/>
   <attribute value="slidingdoor.mesh" name="Mesh ref"/>
   <attribute value="slidingdoor.skeleton" name="Skeleton ref"/>
   <attribute value="lasi_vaalvihrea.material" name="Mesh materials"/>
   <attribute value="0" name="Draw distance"/>
   <attribute value="true" name="Cast shadows"/>
  </component>
  <component type="EC_DynamicComponent" sync="1" name="door">
    <attribute value="true" type="bool" name="opened"/>
    <attribute value="false" type="bool" name="locked"/>
  </component>
</entity>
"""

#should we call this 'dom'?: 
#ec attrs as dom attrs, comps as xml (dom?) elements
#xml3d specific is the group idea and how the mesh ref is etc so is well named.
door_xml3d = """
<group>
  <mesh src="slidingdoor.mesh" /> 
  <door locked="false" opened="true" />
</group>
"""
#<door opened="true" locked="false" />
#was lazy and hacked the order - should use some xmldiff
#.. switch the attr order when do, to match the txml one - clearer to read

def txml_to_xml3d(txml_doc):
    root = ET.fromstring(txml_doc)
    #tree = ElementTree(root) #thanks http://stackoverflow.com/questions/647071/python-xml-elementtree-from-a-string-source #.. ah but not needed (yet)

    #xml3d_tree = ElementTree()
    xml3d_group = None #now we support just one entity
    if root.tag == 'entity': #'component':
        ent = root
        xml3d_group = ET.Element('group')

        #comps = ent.getiterator('component')
        for comp in ent: #in the reX EC spec ents only have comps
            ec_type = comp.attrib['type']
            #txmlutil.attrval(comp, 'type')
            if ec_type == "EC_DynamicComponent":
                xml3d_type = comp.attrib['name']

            else: #is a normal EC where the type attr tells the type etc.
                #for old tundra style with EC_ in the type string
                if ec_type.startswith("EC_"):
                    ec_type = ec_type[3:]
                xml3d_type = ec_type.lower()

            xml3d_elem = ET.SubElement(xml3d_group, xml3d_type)

            #this didn't just work in general - ends up with this kind of xml:
            #<mesh Cast shadows="true" Draw distance="0">
            #.. but for DynamicComponent's it's the right thing
            if ec_type == "EC_DynamicComponent":
                for attr in comp: #.. and comps have only attrs
                    attr_name = attr.attrib['name']
                    attr_val = attr.attrib['value']
                    xml3d_elem.attrib[attr_name] = attr_val

            else:
                if xml3d_type == "mesh":
                    xml3d_elem.attrib['src'] = txmlutil.attrval(comp, 'Mesh ref')

            #probably what we'd need is preserving all the attrs for all comps,
            #perhaps have a mapping dict for known xml3d ones and
            #then pass unknown ones through with whitespace -> '_' conversion?

    return xml3d_group #xml3d_tree

def test_txml_to_xml3d(txml_doc, ref_xml3d_doc):
    ref_xml3d_root = ET.fromstring(ref_xml3d_doc)
    #ref_xml3d = ElementTree(ref_xml3d_root)

    xml3d = txml_to_xml3d(txml_doc)

    print txml_doc
    print " ====>\n"
    #print xml3d.tostring()
    print ET.tostring(xml3d)
    print " ----- "
    print ET.tostring(ref_xml3d_root)
    assert etcomp.el_equal(xml3d, ref_xml3d_root)

def test():
    test_txml_to_xml3d(door_txml, door_xml3d)

if __name__ == '__main__':
    test()

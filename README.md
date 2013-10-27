txml-xml3d
==========

realXtend Tundra txml &lt;-> xml3d converter

Currently works to convert a single entity TXML to a xml3d
group. Works for DynamicComponent where reuses the attribute values directly, and for Mesh component where fetches the 'Mesh ref' parameter to src attribute.

Written in a test driven fashion, running this executes the test with this output:

```xml
user@TONI ~/src/txml-xml3d (master)
$ python txml-xml3d.py

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

 ====>

<group><mesh src="slidingdoor.mesh" /><door locked="false" opened="true" /></group>
 -----
<group>
  <mesh src="slidingdoor.mesh" />
  <door locked="false" opened="true" />
</group>
```

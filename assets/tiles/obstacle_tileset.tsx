<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.11.0" name="test" tilewidth="64" tileheight="32" tilecount="17" columns="0">
 <grid orientation="orthogonal" width="1" height="1"/>
 <tile id="2" type="wall">
  <image source="black square.png" width="32" height="32"/>
 </tile>
 <tile id="4" type="one_way_platform">
  <image source="one way platform.png" width="32" height="32"/>
 </tile>
 <tile id="6" type="moving_platform">
  <image source="moving_platform.png" width="64" height="32"/>
 </tile>
 <tile id="7" type="spike">
  <image source="spikes.png" width="32" height="32"/>
 </tile>
 <tile id="9" type="sign">
  <image source="sign.png" width="32" height="32"/>
 </tile>
 <tile id="10" type="ladder">
  <image source="ladder_mid.png" width="32" height="32"/>
 </tile>
 <tile id="11" type="ladder">
  <image source="ladder_top.png" width="32" height="32"/>
 </tile>
 <tile id="12" type="box">
  <image source="dynamic_objects/box.png" width="32" height="32"/>
 </tile>
 <tile id="14" type="button">
  <image source="buttonBlue.png" width="32" height="32"/>
  <animation>
   <frame tileid="14" duration="100"/>
   <frame tileid="15" duration="100"/>
  </animation>
 </tile>
 <tile id="15">
  <image source="buttonBlue_pressed.png" width="32" height="32"/>
 </tile>
 <tile id="16" type="switch">
  <properties>
   <property name="init_pos" value="left"/>
  </properties>
  <image source="switchLeft.png" width="32" height="32"/>
  <animation>
   <frame tileid="16" duration="100"/>
   <frame tileid="17" duration="100"/>
   <frame tileid="18" duration="100"/>
   <frame tileid="17" duration="100"/>
  </animation>
 </tile>
 <tile id="17" type="switch">
  <properties>
   <property name="init_pos" value="center"/>
  </properties>
  <image source="switchMid.png" width="32" height="32"/>
  <animation>
   <frame tileid="16" duration="100"/>
   <frame tileid="17" duration="100"/>
   <frame tileid="18" duration="100"/>
   <frame tileid="17" duration="100"/>
  </animation>
 </tile>
 <tile id="18" type="switch">
  <properties>
   <property name="init_pos" value="right"/>
  </properties>
  <image source="switchRight.png" width="32" height="32"/>
  <animation>
   <frame tileid="16" duration="100"/>
   <frame tileid="17" duration="100"/>
   <frame tileid="18" duration="100"/>
   <frame tileid="17" duration="100"/>
  </animation>
 </tile>
 <tile id="19" type="binary_switch">
  <image source="binary_switch_left.png" width="32" height="32"/>
  <animation>
   <frame tileid="19" duration="100"/>
   <frame tileid="18" duration="100"/>
  </animation>
 </tile>
 <tile id="20" type="bubble">
  <image source="bubble.png" width="32" height="32"/>
  <animation>
   <frame tileid="20" duration="100"/>
   <frame tileid="21" duration="100"/>
  </animation>
 </tile>
 <tile id="21">
  <image source="bubble squished.png" width="32" height="32"/>
 </tile>
 <tile id="22" type="ladder">
  <properties>
   <property name="show" value="false"/>
  </properties>
  <image source="ladder_invis.png" width="32" height="32"/>
 </tile>
</tileset>

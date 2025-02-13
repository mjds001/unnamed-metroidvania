<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.11.0" name="test" tilewidth="64" tileheight="32" tilecount="10" columns="0">
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
  <image source="box.png" width="32" height="32"/>
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
</tileset>

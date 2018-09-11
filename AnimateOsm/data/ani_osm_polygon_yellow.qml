<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyAlgorithm="0" simplifyDrawingHints="1" simplifyMaxScale="1" version="3.3.0-Master" readOnly="0" minScale="1e+08" simplifyLocal="1" hasScaleBasedVisibilityFlag="0" labelsEnabled="0" maxScale="0" simplifyDrawingTol="1">
  <renderer-v2 forceraster="0" enableorderby="0" symbollevels="0" type="RuleRenderer">
    <rules key="{a1dce3bf-f542-47f8-b4b8-253d56552d2b}">
      <rule symbol="0" filter="&quot;frame_age&quot; = 1" key="{0478e64b-8666-495e-8105-ab3e8c2392a8}" label="new"/>
      <rule symbol="1" filter="&quot;frame_age&quot; > 1" key="{91b40b6d-d020-44f0-a7c0-181907260c70}" label="decay"/>
    </rules>
    <symbols>
      <symbol name="0" clip_to_extent="1" alpha="1" type="fill">
        <layer locked="0" class="SimpleFill" pass="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="255,232,23,80"/>
          <prop k="joinstyle" v="miter"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,232,23,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="1"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="1" clip_to_extent="1" alpha="1" type="fill">
        <layer locked="0" class="SimpleFill" pass="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="255,232,23,55"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,232,23,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.5"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineColor" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="color_hsv(54, min(((91/3)+(3*&quot;frame_age&quot;)), 91), 100)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="simple">
    <settings>
      <text-style fontCapitals="0" isExpression="0" textOpacity="1" fontUnderline="0" fontFamily="Sans Serif" textColor="0,0,0,255" multilineHeight="1" fontLetterSpacing="0" useSubstitutions="0" fontItalic="0" blendMode="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" namedStyle="Normal" fontSizeUnit="Point" previewBkgrdColor="#ffffff" fontWordSpacing="0" fontStrikeout="0" fontWeight="50" fieldName="osm_id" fontSize="10">
        <text-buffer bufferSizeUnits="MM" bufferDraw="0" bufferBlendMode="0" bufferSize="1" bufferJoinStyle="128" bufferNoFill="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferColor="255,255,255,255" bufferOpacity="1"/>
        <background shapeBorderColor="128,128,128,255" shapeOffsetY="0" shapeRotation="0" shapeSVGFile="" shapeOpacity="1" shapeRadiiUnit="MM" shapeRotationType="0" shapeBorderWidth="0" shapeRadiiX="0" shapeSizeX="0" shapeSizeType="0" shapeType="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="MM" shapeFillColor="255,255,255,255" shapeBlendMode="0" shapeRadiiY="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64" shapeSizeUnit="MM" shapeSizeY="0" shapeDraw="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetUnit="MM"/>
        <shadow shadowOffsetAngle="135" shadowRadiusUnit="MM" shadowOpacity="0.7" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowColor="0,0,0,255" shadowOffsetUnit="MM" shadowUnder="0" shadowScale="100" shadowOffsetDist="1" shadowBlendMode="6" shadowRadius="1.5" shadowRadiusAlphaOnly="0" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetGlobal="1" shadowDraw="0"/>
        <substitutions/>
      </text-style>
      <text-format formatNumbers="0" rightDirectionSymbol=">" placeDirectionSymbol="0" plussign="0" decimals="3" leftDirectionSymbol="&lt;" wrapChar="" reverseDirectionSymbol="0" addDirectionSymbol="0" multilineAlign="4294967295"/>
      <placement fitInPolygonOnly="0" rotationAngle="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" yOffset="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" repeatDistanceUnits="MM" quadOffset="4" maxCurvedCharAngleIn="25" centroidWhole="0" offsetType="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" preserveRotation="1" dist="0" repeatDistance="0" placementFlags="10" maxCurvedCharAngleOut="-25" centroidInside="0" distUnits="MM" xOffset="0" placement="0" distMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MM" priority="5"/>
      <rendering scaleMin="0" labelPerPart="0" scaleMax="0" zIndex="0" obstacleFactor="1" limitNumLabels="0" maxNumLabels="2000" fontLimitPixelSize="0" obstacleType="0" fontMaxPixelSize="10000" minFeatureSize="0" displayAll="0" scaleVisibility="0" upsidedownLabels="0" drawLabels="1" obstacle="1" fontMinPixelSize="3" mergeLines="0"/>
      <dd_properties>
        <Option type="Map">
          <Option name="name" value="" type="QString"/>
          <Option name="properties"/>
          <Option name="type" value="collection" type="QString"/>
        </Option>
      </dd_properties>
    </settings>
  </labeling>
  <customproperties>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory width="15" penAlpha="255" scaleDependency="Area" diagramOrientation="Up" height="15" labelPlacementMethod="XHeight" sizeScale="3x:0,0,0,0,0,0" enabled="0" sizeType="MM" lineSizeType="MM" backgroundColor="#ffffff" backgroundAlpha="255" rotationOffset="270" penColor="#000000" opacity="1" barWidth="5" penWidth="0" minimumSize="0" lineSizeScale="3x:0,0,0,0,0,0" scaleBasedVisibility="0" minScaleDenominator="0" maxScaleDenominator="1e+08">
      <fontProperties style="" description="Sans Serif,9,-1,5,50,0,0,0,0,0"/>
      <attribute color="#000000" label="" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="0" dist="0" zIndex="0" showAll="1" linePlacementFlags="18" priority="0" obstacle="0">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <fieldConfiguration>
    <field name="osm_id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="user">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="timestamp">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="epoch">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="frame_age">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0"/>
  <aliases>
    <alias name="" index="0" field="osm_id"/>
    <alias name="" index="1" field="user"/>
    <alias name="" index="2" field="timestamp"/>
    <alias name="" index="3" field="epoch"/>
    <alias name="" index="4" field="frame_age"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="osm_id"/>
    <default expression="" applyOnUpdate="0" field="user"/>
    <default expression="" applyOnUpdate="0" field="timestamp"/>
    <default expression="" applyOnUpdate="0" field="epoch"/>
    <default expression="" applyOnUpdate="0" field="frame_age"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0" field="osm_id"/>
    <constraint unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0" field="user"/>
    <constraint unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0" field="timestamp"/>
    <constraint unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0" field="epoch"/>
    <constraint unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0" field="frame_age"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="osm_id"/>
    <constraint exp="" desc="" field="user"/>
    <constraint exp="" desc="" field="timestamp"/>
    <constraint exp="" desc="" field="epoch"/>
    <constraint exp="" desc="" field="frame_age"/>
  </constraintExpressions>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="&quot;timestamp&quot;" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column name="osm_id" hidden="0" width="-1" type="field"/>
      <column name="user" hidden="0" width="-1" type="field"/>
      <column name="timestamp" hidden="0" width="203" type="field"/>
      <column name="epoch" hidden="0" width="145" type="field"/>
      <column name="frame_age" hidden="0" width="-1" type="field"/>
      <column hidden="1" width="-1" type="actions"/>
    </columns>
  </attributetableconfig>
  <editform tolerant="1">/home/raymond/git/animateOsm</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="epoch" editable="1"/>
    <field name="frame_age" editable="1"/>
    <field name="osm_id" editable="1"/>
    <field name="timestamp" editable="1"/>
    <field name="user" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="epoch" labelOnTop="0"/>
    <field name="frame_age" labelOnTop="0"/>
    <field name="osm_id" labelOnTop="0"/>
    <field name="timestamp" labelOnTop="0"/>
    <field name="user" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <expressionfields/>
  <previewExpression>osm_id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>

::::::: collapse With your own set

## With your own set

Set up Emio using your own legs and connectors. You should add your own leg's meshes in `home/emio-labs/assets/data/meshes/legs`
and the connector's mesh in `home/emio-labs/assets/data/meshes/centerparts`.

For the legs you should provide:
1. A surface mesh in the `stl` format for the visualization.
2. A volume mesh in the `vtk` format, if you want to use the tetra model.
3. A `txt` file with coordinates in the format [x, y, z, qx, qy, qz, qw], if you want to use the beam and cosserat models.

For the connector you should provide:
1. A surface mesh in the `stl` format for the visualization.
2. A volume mesh in the `vtk` format, if you want to use the tetra model (deformable option).
3. A `json` file defining the positions and orientations for attaching the legs.


:::::: highlight
::::: group-grid {style="grid-template-rows:repeat(7, 0fr);"}
**Motor n°0**
#input("custom1leg", "leg name")
:::: select custom1orientation
::: option clockwiseup
::: option counterclockwiseup
::: option clockwisedown
::: option counterclockwisedown
::::
:::: select custom1model
::: option beam
::: option cosserat
::: option tetra
::::
#input("custom1massdensity", "mass density")

#input("custom1youngmodulus", "young modulus")

#input("custom1poissonratio", "poisson ratio")

**Motor n°1**
#input("custom2leg", "leg name")
:::: select custom2orientation
::: option clockwiseup
::: option counterclockwiseup
::: option clockwisedown
::: option counterclockwisedown
::::
:::: select custom2model
::: option beam
::: option cosserat
::: option tetra
::::
#input("custom2massdensity", "mass density")

#input("custom2youngmodulus", "young modulus")

#input("custom2poissonratio", "poisson ratio")

**Motor n°2**
#input("custom3leg", "leg name")
:::: select custom3orientation
::: option clockwiseup
::: option counterclockwiseup
::: option clockwisedown
::: option counterclockwisedown
::::
:::: select custom3model
::: option beam
::: option cosserat
::: option tetra
::::
#input("custom3massdensity", "mass density")

#input("custom3youngmodulus", "young modulus")

#input("custom3poissonratio", "poisson ratio")

**Motor n°3**
#input("custom4leg", "leg name")
:::: select custom4orientation
::: option clockwiseup
::: option counterclockwiseup
::: option clockwisedown
::: option counterclockwisedown
::::
:::: select custom4model
::: option beam
::: option cosserat
::: option tetra
::::
#input("custom4massdensity", "mass density")

#input("custom4youngmodulus", "young modulus")

#input("custom4poissonratio", "poisson ratio")


:::::

::::: group-grid {style="grid-template-rows:repeat(7, 0fr)"}
**Connector**
#input("customcenterpartname", "name")
:::: select customcenterparttype
::: option rigid
::: option deformable
::::
:::: select customcenterpartmodel
::: option beam
::: option cosserat
::: option tetra
::::
#input("customcenterpartmassdensity", "mass density") 

#input("customcenterpartyoungmodulus", "young modulus")

#input("customcenterpartpoissonratio", "poisson ratio")

**Configuration**
:::: select customconfiguration
::: option compact
::: option extended
::::

<div></div>
<div></div>
<div></div>
<div></div>
<div></div>

**Camera**
:::: select customcamera
::: option disable
::: option enable
::::

<input type="text" id="customnbtracker" value="" placeholder="# of trackers" title="# of trackers" onchange="filled(event)" data-condition="customcamera==enable"/>

<select id="customshowfeed" title="Show feed" onchange="selected(event)" data-condition="customcamera==enable">
  <option value="disable">hide feed</option>
  <option value="enable">show feed</option>
</select>

:::::

#runsofa-button("assets/labs/sandbox/sandbox.py", "--legsName" "custom1leg" "custom2leg" "custom3leg" "custom4leg" "--legsModel" "custom1model" "custom2model" "custom3model" "custom4model" "--legsMassDensity" "custom1massdensity" "custom2massdensity" "custom3massdensity" "custom4massdensity" "--legsYoungModulus" "custom1youngmodulus" "custom2youngmodulus" "custom3youngmodulus" "custom4youngmodulus" "--legsPoissonRatio" "custom1poissonratio" "custom2poissonratio" "custom3poissonratio" "custom4poissonratio" "--legsPositionOnMotor" "custom1orientation" "custom2orientation" "custom3orientation" "custom4orientation" "--centerPartName" "customcenterpartname" "--centerPartMassDensity" "customcenterpartmassdensity" "--centerPartPoissonRatio" "customcenterpartpoissonratio" "--centerPartYoungModulus" "customcenterpartyoungmodulus" "--centerPartType" "customcenterparttype" "--centerPartModel" "customcenterpartmodel" "--configuration" "customconfiguration" "--camera" "customcamera" "--cameraFeed" "customshowfeed" "--nbTrackers" "customnbtracker")
::::::
:::::::

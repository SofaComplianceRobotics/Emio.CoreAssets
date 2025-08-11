::::::: collapse With the original set

## With the original set

Set up Emio using the legs and connectors that were originally provided with the robot.

:::::: highlight
::::: group-grid {style="grid-template-rows:repeat(4, 0fr)"}
**Motor n°0**
![](assets/data/images/legs/blueleg-counterclockwisedown.png){data-condition="m1orientation==counterclockwisedown m1leg==blueleg"}
![](assets/data/images/legs/blueleg-clockwisedown.png){data-condition="m1orientation==clockwisedown m1leg==blueleg"}
![](assets/data/images/legs/whiteleg-counterclockwisedown.png){data-condition="m1orientation==counterclockwisedown m1leg==whiteleg"}
![](assets/data/images/legs/whiteleg-clockwisedown.png){data-condition="m1orientation==clockwisedown m1leg==whiteleg"}
![](assets/data/images/legs/blueleg-counterclockwiseup.png){data-condition="m1orientation==counterclockwiseup m1leg==blueleg"}
![](assets/data/images/legs/blueleg-clockwiseup.png){data-condition="m1orientation==clockwiseup m1leg==blueleg"}
![](assets/data/images/legs/whiteleg-counterclockwiseup.png){data-condition="m1orientation==counterclockwiseup m1leg==whiteleg"}
![](assets/data/images/legs/whiteleg-clockwiseup.png){data-condition="m1orientation==clockwiseup m1leg==whiteleg"}
:::: select m1leg 
::: option blueleg
::: option whiteleg
::: option None
::::
:::: select m1orientation
::: option clockwiseup
::: option counterclockwiseup
::: option clockwisedown
::: option counterclockwisedown
::::
:::: select m1model
::: option beam
::: option cosserat
::: option tetra
::::

**Motor n°1**
![](assets/data/images/legs/blueleg-counterclockwisedown.png){data-condition="m2orientation==counterclockwisedown m2leg==blueleg"}
![](assets/data/images/legs/blueleg-clockwisedown.png){data-condition="m2orientation==clockwisedown m2leg==blueleg"}
![](assets/data/images/legs/whiteleg-counterclockwisedown.png){data-condition="m2orientation==counterclockwisedown m2leg==whiteleg"}
![](assets/data/images/legs/whiteleg-clockwisedown.png){data-condition="m2orientation==clockwisedown m2leg==whiteleg"}
![](assets/data/images/legs/blueleg-counterclockwiseup.png){data-condition="m2orientation==counterclockwiseup m2leg==blueleg"}
![](assets/data/images/legs/blueleg-clockwiseup.png){data-condition="m2orientation==clockwiseup m2leg==blueleg"}
![](assets/data/images/legs/whiteleg-counterclockwiseup.png){data-condition="m2orientation==counterclockwiseup m2leg==whiteleg"}
![](assets/data/images/legs/whiteleg-clockwiseup.png){data-condition="m2orientation==clockwiseup m2leg==whiteleg"}
:::: select m2leg
::: option blueleg
::: option whiteleg
::: option None
::::
:::: select m2orientation
::: option clockwiseup
::: option counterclockwiseup
::: option clockwisedown
::: option counterclockwisedown
::::
:::: select m2model
::: option beam
::: option cosserat
::: option tetra
::::

**Motor n°2**
![](assets/data/images/legs/blueleg-counterclockwisedown.png){data-condition="m3orientation==counterclockwisedown m3leg==blueleg"}
![](assets/data/images/legs/blueleg-clockwisedown.png){data-condition="m3orientation==clockwisedown m3leg==blueleg"}
![](assets/data/images/legs/whiteleg-counterclockwisedown.png){data-condition="m3orientation==counterclockwisedown m3leg==whiteleg"}
![](assets/data/images/legs/whiteleg-clockwisedown.png){data-condition="m3orientation==clockwisedown m3leg==whiteleg"}
![](assets/data/images/legs/blueleg-counterclockwiseup.png){data-condition="m3orientation==counterclockwiseup m3leg==blueleg"}
![](assets/data/images/legs/blueleg-clockwiseup.png){data-condition="m3orientation==clockwiseup m3leg==blueleg"}
![](assets/data/images/legs/whiteleg-counterclockwiseup.png){data-condition="m3orientation==counterclockwiseup m3leg==whiteleg"}
![](assets/data/images/legs/whiteleg-clockwiseup.png){data-condition="m3orientation==clockwiseup m3leg==whiteleg"}
:::: select m3leg
::: option blueleg
::: option whiteleg
::: option None
::::
:::: select m3orientation
::: option clockwiseup
::: option counterclockwiseup
::: option clockwisedown
::: option counterclockwisedown
::::
:::: select m3model
::: option beam
::: option cosserat
::: option tetra
::::

**Motor n°3**
![](assets/data/images/legs/blueleg-counterclockwisedown.png){data-condition="m4orientation==counterclockwisedown m4leg==blueleg"}
![](assets/data/images/legs/blueleg-clockwisedown.png){data-condition="m4orientation==clockwisedown m4leg==blueleg"}
![](assets/data/images/legs/whiteleg-counterclockwisedown.png){data-condition="m4orientation==counterclockwisedown m4leg==whiteleg"}
![](assets/data/images/legs/whiteleg-clockwisedown.png){data-condition="m4orientation==clockwisedown m4leg==whiteleg"}
![](assets/data/images/legs/blueleg-counterclockwiseup.png){data-condition="m4orientation==counterclockwiseup m4leg==blueleg"}
![](assets/data/images/legs/blueleg-clockwiseup.png){data-condition="m4orientation==clockwiseup m4leg==blueleg"}
![](assets/data/images/legs/whiteleg-counterclockwiseup.png){data-condition="m4orientation==counterclockwiseup m4leg==whiteleg"}
![](assets/data/images/legs/whiteleg-clockwiseup.png){data-condition="m4orientation==clockwiseup m4leg==whiteleg"}
:::: select m4leg
::: option blueleg
::: option whiteleg
::: option None
::::
:::: select m4orientation
::: option clockwiseup
::: option counterclockwiseup
::: option clockwisedown
::: option counterclockwisedown
::::
:::: select m4model
::: option beam
::: option cosserat
::: option tetra
::::

:::::

::::: group-grid {style="grid-template-rows:repeat(3, 0fr)"}
**Connector**
![](assets/data/images/centerparts/bluepart.png){data-condition="centerpartname==bluepart"}
![](assets/data/images/centerparts/yellowpart.png){data-condition="centerpartname==yellowpart"}
![](assets/data/images/centerparts/whitepart.png){data-condition="centerpartname==whitepart"}
:::: select centerparttype
::: option rigid
::: option deformable
::::
:::: select centerpartname
::: option bluepart
::: option yellowpart
::: option whitepart
::::

**Configuration**
![](assets/data/images/emio-extended.png){data-condition="configuration==extended"}
![](assets/data/images/emio-compact.png){data-condition="configuration==compact"}
:::: select configuration
::: option compact
::: option extended
::::
:::::

#runsofa-button("assets/labs/sandbox/sandbox.py", "--legsName" "m1leg" "m2leg" "m3leg" "m4leg" "--legsModel" "m1model" "m2model" "m3model" "m4model" "--legsYoungModulus" "" "" "" "" "--legsPositionOnMotor" "m1orientation" "m2orientation" "m3orientation" "m4orientation" "--centerPartName" "centerpartname" "--centerPartType" "centerparttype" "--configuration" "configuration")
::::::
:::::::

# Pen Plotter
## Christian Clephan, Kyle McGrath
### Introduction (both) 

### Hardware Design Overview (christian) 

### Software Design Overiew (Kyle)

### Results (both)

### What we learned (both)

### Additional files (CAD, view?) 



# Pen Plotter Proposal
## Christian Clephan, Kyle McGrath
### Description

Our proposed design will utilize a radial arm rotating around a hub. In the top right corner of the piece of paper will be a 3D rotating hub 
driven by a Pittperson Gearmotor. The gearmotor will provide torque to our radial arm which will consist of a rail system on which a flat bracket carrying the pen is mounted. The rail system will consist of metal tubes that we hope to find around the Aero Hanger and will be supported by 3D printed brackets (translational hub). The pen carrying bracket will be moved translationally by a belt. The belt will be obtained from McMaster-Carr and it will also be driven by a Pittperson Gearmotor. At the end of the rail system, we will mount a wheel in order to allow for free rotation of the system. At the end of the translational belt system there will be a platform to hold a gear, and on the other side a rod connecting to the free moving wheel. The wheel will likely be a hobby wheel for RC cars that we will obtain from Zacsters, or 3D printing could be an option. The pen carrier will be raised and lowered using an SG90 servo obtained from Zacsters. All parts with complex geometry or of small size will likely be 3D printed at Mustang 60. 

For our rail system, we want the rails to extend past the diameter of the paper in order to prevent the wheel from disrupting or damaging the paper. The rails will provide a fixed length between the motor and the wheel while also allowing the pen to move freely back and forth. All components, assembly, and drawing can be found in PenPlotterModel folder of this repository. Below is an drawing of our assembly with some dimensions (belt is not pictured, but would run between two translational gears).

One possible concern with our design is if the provided Pittperson Gearmotors can provide enough torque to drive the radial arm rails. Another concern of ours is implementing the rails to drive the pen radial motion as this is something we are both inexperienced with. 


Table 1. Bill of Materials

| Qty. | Part                  | Source                | Est. Cost |
|:----:|:----------------------|:----------------------|:---------:|
|  2   | Pittperson Gearmotors | ME405 Tub             |     -     |
|  1   | Nucleo with Shoe      | ME405 Tub             |     -     |
|  1   | Purple Sharpie        | Home supply           |     -     |
|  1   | SG90 Servo            | Zacsters              |   $1.50   |
|  3   | Metal Rods            | Aero Hanger Trash     |     -     |
|  1   | 3D Printed Translation Hub    | Mustang 60            |     -     |
|  1   | RC Hobby Wheel        | Zacsters              |   $3.00   |
|  1   | Belt                  | McMaster-Carr         |  $10.43   |
|  1   | 3D Printed Pen Holder | Mustang 60            |     -     |
|  1   | Rotation Hub          | Mustang 60            |     -     |
|  1   | Gear/Platform for Translation | Mustang 60            |     -     |



![alt text](https://github.com/cclephan/PenPlotter/blob/main/PenPlotterModel/PenPlotterV1.PNG?raw=true)

Figure 1. Detailed Drawing of Pen Plotter Assembly

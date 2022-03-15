# Pen Plotter
## Date Updated: March 15, 2022
## Christian Clephan, Kyle McGrath
### Introduction (both) 

Our device was a 2.5 axis pen plotter, capable of taking in HPGL files as input and drawing on a piece of paper as the output. For our device we used polar coordinates. A radial arm moving around a hub was used to create the changes in angle, and the pen was moved radially using a rail system with a belt to provide the radial motion. The remaining 0.5 axis is the moving of the pen up and down. 

The device was intended to be used by its two creators: Christian Clephan and Kyle McGrath to demonstrate their mechatronics knowledge in the Term Project. Our goal was to create a robot which could draw anything, which we were able to accomplish by drawing some parallel lines, arcs, and scripples in the formation of a rectangle.


### Hardware Design Overview (christian) 
Our Pen Plotter has two degrees of freedom controlled by two Pittperson DC motors and the half degree of freedom controlled by 1 servo motor. The servo motor controls the up and down motion of the pen by swinging in an arc downwards and perpendicular to the page, or upwards and parallel (not touching the page). One of the DC motors controls the radial motion of the pen plotter by spinning a timing belt, while housed on the rotational base. The timing belt fits around the motor gear and pulley wheel on the opposite side, which moves a carriage holding the servo motor and pen. The carriage rests on two metal rods which allow it to freely move in the radial direction. The angular direction is controlled by the other DC motor spinning the base holding the plotter. A wheel was attached to the other end of the plotter to allow for rotation as the motor spun the entire system. The spinning base, wheel, carriage, and radial motor housing were all 3D printed. Other materials such as the rods, pulley wheel, and fasteners were found in the lab scrap bin, while the timing belt was purchased from McMaster-Carr. Detailed drawings and CAD models of the hardware can be found at https://github.com/cclephan/PenPlotter/tree/main/PenPlotterModel.

### Software Design Overiew (Kyle)
Link to Doxygen for futher software design details: https://cclephan.github.io/PenPlotter/

The software consisted of utilizing several of our old files used in previous ME 405 labs as well as some new files to manage the HPGL processing. 

The files that were reused from previous labs were the Closed Loop Controller File, the Motor Driver File, and the Encoder Reader File. 

The parsing file would open the respective HPGL file and convert the HPGL coordinates into two rotational commands that are inputted into the closed loop controller file. HPGL coordiantes were provided in X and Y coordinates, these were converted to Polar Coordiantes using Trigonometry. The radial coordinate was then converted to a second theta coordinate for the motor driving the radial motion. 

The servo driver file was also new and included creating a timer, timer channel, and two functions which applied a PWM signal turning the servo motor so the pen is either up or down.

Our Task Diagram for the whole system can be seen in the Doxygen page. Some of the organization for the tasks have changed since the proposal, but this was due to hardware and time limitations. 



### Results (both)
Our system came close to drawing what was inputted from the HPGL file, but there were still several shortcomings. Our most successful attempt was an attempt to draw two parallel lines, a video of which can be seen below. 

We tested our system by providing HPGL inputs and printing the respective commands provided to the motors. We then performed hand calculations to confirm that the commands provided to the motors match what we wanted to do. Initially we noticed that the commands that were provided to the motors did not match the hand calculations that we performed. We believed this was due to our use of Queues as we were saving our commands as integers instead of floats. We changed this and the inputs to the motors more closely followed desired results. 

The first HPGL file that we tested with our system was a straight line that was drawn in Inkscape and exported as an HPGL. One of earlier tests with drawing a straight line can be seen here: https://youtu.be/u9vNNVAs_34. This test was eventually successful and we felt confident with moving forward with drawing two parallel lines. After taking some time to modify the speed of each motor and the period associated with each task, we eventually were able to draw two parallel lines. The video of drawing two parallel lines can be seen here: https://youtube.com/shorts/n7fFq1dV0Q4?feature=share. Some of our later tests that were unsuccessful were attempts to draw rectangles or circles. A failed rectangle attempt can be seen here: https://youtu.be/5r2_hMjXv8Q. We believe our system could have failed these tests because we did not interpolate between points which could have allowed for more defined motion between the points. 


### What we learned (both)

From this project we learned the importance of testing our code early and often. We completed the hardware portion of our project early on in the process, and we made the mistake of believing the software portion of our project wouldn't be too complicated as we planned to reuse several files from older projects. We ran into some difficulty getting all the commands from the HPGL file to read as sometimes commands would get skipped over. We eventually learned this was likely due to either calling queue.read() twice as well as a period error. There were other errors that we were unable to fix and from this we learned to not underestimate how long the software portion of a project will take. 

Another thing we learned is the importance of using states in our code. We believed it would be easier to create code that works first and then implement the states after we had code that worked. In the end our code did not work as expected and we decided it was time to update the code to utilize states. We quickly saw that by using states, readability of the code improved significantly, and we were able to easily spot errors that we had missed. 

### Additional files (CAD, view?) 



# Pen Plotter Proposal
## Date Updated: Feb 17, 2022 
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

"""!
@file mainpage.py
This file contains information regarding software design
@author Christian Clephan
@author Kyle McGrath
@date   09-Feb-2022
@copyright (c) 2022 released under CalPoly

@mainpage

@section sftware Software Design
            This section includes information regarding our pen plottor robot
            software design. Below in Figure 1 is a task diagram of all information that
            will be shared between tasks to accomplish our goal. To operate the robot, the user 
            will run the main file and input an HPGL file that will be processed. The main file 
            will then call the Processing Task which will place the current command (Pen UP or Pen Down) 
            and the theta positions in revolutions that will be input to the radial, rotational,
            and servo tasks. The servo task will output a 0 or a 1 to the servoDriver based on 
            whether the Pen needs to be UP (1) or down (0). 
            The radial and rotational tasks will output the setPoint in ticks
            to the controller task which calls the encoder task to calculate a duty cycle 
            based on the proportional gain and encoder read values. 
            This duty cycle is then input into the motor driver task to drive the motor. <br>
            \image html UpdatedTaskDiagram.png "Figure 1: Squiggly Task Diagram" <br>
            
            The previous Task Diagram could also be seen below in Figure 2. Some changes 
            that we made are that we opted to have all the processing performed on the Nucleo, 
            and we decided to have the User Interface built into the main file. 
            \image html TaskDiagram.png "Figure 2: Previous Task Diagram" <br>

@subsection task_UI Task User Interface
            User inteface task will wait for a user input key command, which
            will either stop the machine, reset the pens position, or accept
            a drawing that is sent my the user to be drawn. <br>
            
            \image html UI_Task.png "Figure 2: User Interface Task FSM" <br>

@subsection task_process Task Processing
            Once the user has input a drawing the processing task will convert
            the drawing to X and Y coordinates. From those X and Y coordinates,
            inverse kinematics will be used to translate X/Y to R and theta
            motor positions. This information will be sent to controller task
            to send PWM to motors. <br>
            
            \image html Processing_Task.png "Figure 3: Processing Task FSM" <br>

@subsection task_controller Task Controller
            Task controller will wait for G-Code/HPGL drawing path to complete,
            and use path data with a proportional gain input to send PWM
            signals to respective motors. <br>
            
            \image html Controller_Task.png "Figure 4: Controller Task FSM" <br>

@subsection task_motor Task Motor
            Task motor will recieve PWM duty cycles from the controller task
            and apply the signal to instantiated motors. <br>
            

@subsection task_encoder Task Encoder
            Task encoder will be the highest priority, constantly sending
            motor positions for radial and angular motors. Task controller will
            receive these values and interpret them to vary PWM for motors.<br>
            
            
"""

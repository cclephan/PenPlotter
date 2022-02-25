# -*- coding: utf-8 -*-
"""!
@file mainpage.py
@author Christian Clephan
@author Kyle McGrath
@date   09-Feb-2022
@copyright (c) 2022 released under CalPoly

@section sftware Software Design
            This section includes information regarding our pen plottor robot
            software design. Below is a task diagram of all information that
            will be shared between tasks to accomplish our goal. To operate the
            robot the user will first press a key command to start processing
            HPGL/G-Code. Calculated pen pathing is then sent to the controller
            task, which will send a duty cycle to motors based on a proportional
            gain and encoder read values. <br>
            
            \image html TaskDiagram.png "Figure 1: Pen Plotter Task Diagram" <br>

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

@subection task_controller Task Controller
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


# -*- coding: utf-8 -*-
"""
@section sftware Software Design

@subsection task_UI Task User Interface
            User inteface task will wait for a user input key command, which
            will either stop the machine, reset the pens position, or accept
            a drawing that is sent my the user to be drawn.

@subsection task_process Task Processing
            Once the user has input a drawing the processing task will convert
            the drawing to X and Y coordinates. From those X and Y coordinates,
            inverse kinematics will be used to translate X/Y to R and theta
            motor positions. This information will be sent to controller task
            to send PWM to motors.

@subection task_controller Task Controller
            Task controller will wait for G-Code/HPGL drawing path to complete,
            and use path data with a proportional gain input to send PWM
            signals to respective motors.

@subsection task_motor Task Motor
            Task motor will recieve PWM duty cycles from the controller task
            and apply the signal to instantiated motors.

@subsection task_encoder Task Encoder
            Task encoder will be the highest priority, constantly sending
            motor positions for radial and angular motors. Task controller will
            receive these values and interpret them to vary PWM for motors.
"""


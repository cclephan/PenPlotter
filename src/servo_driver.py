"""!
@file servo_driver.py
This file contains the ServoDriver Class used to drive MG 996R servo with pen up/down methods
@author Christian Clephan
@author Kyle McGrath
@date   03-March-2022
@copyright (c) 2022 released under CalPoly
"""

import pyb

class ServoDriver:
    """! 
    This class implements a MG 996R servo.
    """
    def __init__(self,en_pin,pwm_pin,timer):
        """! 
        @brief Instantiates servo object by setting enable pin to high and creating timer/timer channel objects for PWM control
        @param en_pin is the enable pin for the servo motor
        @param pwm_pin is the PWM pin used on Nucleo to send signal
        @param timer is the timer number used corresponding to PWM pin
        """
        en_pin.high()
        ##50Hz timer at specified PWM pin timer number on Nucleo
        self.t = pyb.Timer(timer, freq = 50)
        ##Timer channel used to send PWM signal for specified Nucleo pin
        self.tch = self.t.channel(2,pyb.Timer.PWM, pin=pwm_pin)
    
    def pen_down(self):
        '''!
        @brief Send PWM signal moving the pen down in contact with the page
        '''
        self.tch.pulse_width_percent(5)
    
    def pen_up(self):
        '''!
        @brief Send PWM signal moving the pen up to no longer touch the page
        '''
        self.tch.pulse_width_percent(2)

    
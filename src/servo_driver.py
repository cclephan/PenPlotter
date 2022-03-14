"""!
@file servo_driver.py
This file contains the ServoDriver Class
@author Christian Clephan
@author Kyle McGrath
@date   03-March-2022
@copyright (c) 2022 released under CalPoly
"""


import pyb

class ServoDriver:
    #timer 3
    #pin a7
    def __init__(self,en_pin,pwm_pin,timer):
        en_pin.high()
        self.t = pyb.Timer(timer, freq = 50)
        self.tch = self.t.channel(2,pyb.Timer.PWM, pin=pwm_pin)
    
    def pen_down(self):
        self.tch.pulse_width_percent(5)
    
    def pen_up(self):
        self.tch.pulse_width_percent(2)

    
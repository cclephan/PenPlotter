"""!
@file control.py
Closed loop controller containing methods to control an arbitraries motor duty cycle 
@author Christian Clephan
@author Kyle McGrath
@date   02-Jan-2022
@copyright (c) 2022 released under CalPoly
"""

import utime


class ClosedLoop:
    '''!
    @brief                  Interface with closed loop controller
    @details                Contains all methods that will be used in task_hardware to set the duty cycle based on closed
                                loop control.
    '''
        
    def __init__ (self,PID, satLim, setPoint):
        '''!
        @brief Constructs a closed loop controller
        @details Creates variables necessary to instantiate a controller such as timing, PID gains, saturation
        limit, setpoint value, error, and arrays used in recording a step response
        @param PID is a list containing the three gain values for Kp/Ki/Kd
        @param satLim is a list containing the upper and lower bounds of saturation      
        '''
        ## @brief Instantiates PID controller with gains
        self.firstTime = 0
        self.i = True
        self.PID = PID
        # PID Kp(*%/rad)Ki(*%/rad)Kd(*%s2/rad)
        ## @brief Instantiates duty saturation upper and lower bounds
        self.satLim = satLim
        
        self.setPoint = setPoint
        
        ## @brief Sum of error over a difference in time
        self.esum = 0
        ## @brief Previous error
        self.laste = 0
        self.times = []
        self.motorPositions = []
        #self.t0 = utime.ticks_ms()
        
        print("Controller Instantiated")

    def update (self, Read, startTime):
        '''!
        @brief Updates the controller for timing and error between a read value and the setpoint
        @param Read is the value returned by the sensor detecting the current state of the system (encoder position)
        @param startTime is the initial time for a step response.    
        @return Sends back saturated duty value using sat method.
        '''
        ## @brief Error signal which is the difference between a reference and input (current) value.
        tcur = utime.ticks_ms()
        tdif = utime.ticks_diff(tcur,startTime)
        if self.i:
            self.firstTime = tdif
            self.i = False
        self.times.append(tdif-self.firstTime)
        self.motorPositions.append(Read)
        e = self.setPoint - Read
        #Updates sum of error (area under curve)
        # self.esum += (self.laste+e)*tdif/2
        # ## @brief Delta error calculated by taking difference in error values over a time difference
        # dele = (e - self.laste)/tdif
        # # Updates last error
        # self.laste = e
        #print(e)

        
        ## @brief Duty calculation using PID gains and error values
        # duty = self.PID[0]*(e) + self.PID[1]*(self.esum) + self.PID[2]*(dele) 
        duty = self.PID[0]*(e)
        #print(self.motorPositions)
        return duty
        #return self.sat(duty)
                
                
    def get_Times(self):
        '''!
        @brief Returns time array for a step response
        @return Contains array of time over a step response
        '''
        return self.times
    
    def getPositions(self):
        '''!
        @brief Returns motor positions array for a step response
        @return Contains encoder read positions of a motor over a step response
        '''
        return self.motorPositions
    
    def get_PID(self):
        '''!
        @brief Gets PID object
        @details Quick method to determine what controller is using for PID gains.     
        '''
        return self.PID
    
    def set_PID(self, PID):
        '''!
        @brief Sets PID gains.
        @details Sets PID gains to some new list of values for Kp/Ki/Kd 
        @param PID is a list containing the three gain values for Kp/Ki/Kd    
        '''
        self.PID = PID
        
    def set_setPoint(self,setPoint):
        '''!
        @brief Sets or resets setpoint to a certain value
        '''
        self.setPoint = setPoint
        
    def sat(self,sat_duty):
        '''!
        @brief Saturation functionallity
        @details Controls if a duty is too large from what is calculated in update method.
        @param sat_duty is the value sent by what is calculated in update method.
        @return Sends back either the saturated limit if duty is too high or original duty based on bounds.
        '''
        if sat_duty<self.satLim[0]:
            return self.satLim[0]
        elif sat_duty>self.satLim[1]:
            return self.satLim[1]
        return sat_duty
      

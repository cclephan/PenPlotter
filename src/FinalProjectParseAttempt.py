# Kyle McGrath
# ME 405 Lab 1
# 1/14/22
#code inspiration for isFloat from https://stackoverflow.com/questions/2356925/how-to-check-whether-string-might-be-type-cast-to-float-in-python
#code inspiration for stripping and splitting is from https://tutorial.eyehunts.com/python/how-to-remove-space-in-list-python-example-code/
import re
from matplotlib import pyplot as plt
import math

#Check to see if a string is a float 
def isFloat(string):
    try: 
        float(string)
        return True
    except ValueError:
        return False


L = 5 
r = 0.375 #in

#Open the csv file 
with open('circle.hpgl') as file:
    commands= []
    for line in file.readlines():
        currentLine = line.split(";")
        for thing in currentLine:
            test = thing.split(',')
            if ("PD" in test[0] or "PU" in test[0]) and len(test[0]) > 2:
                theShid = re.split('(\d+)', test[0])
                del test[0]
                test.insert(0, theShid[1])
                test.insert(0, theShid[0])
            commands.append(test)
        print(commands)

x_commands = []
y_commands = []  
theta_commands = []
step = 1016/2

for command in commands:
    i = 1
    
    if command[0] == "PU":
        print("Pen Up")
        cur_command = 0
    elif command[0] == "PD":
        print("Pen Down")
        cur_command = 1
    while i < len(command):
        x_var = int(command[i])/step
        x_commands.append(x_var)
        i = i + 1
        y_var = int(command[i])/step
        y_commands.append(y_var)
        i = i + 1
        if x_var != 0:   
            theta1 = math.atan(y_var/x_var) / (2*math.pi)
        else:
            theta1 = math.pi / 2 / (2*math.pi)
        radial = math.sqrt(x_var**2 + y_var**2)
        theta2 = radial/(2*math.pi * r) 
        theta_commands.append((cur_command, theta1, theta2))
        print((theta1, theta2))
        
        
    
# print(x_commands)
# print(y_commands)
# print(theta_commands)


        
        #print(currentLine)
        
    # x_variables = []
    # y_variables = []
    # #Read each line of the file 
    # for line in file.readlines():    
    #     #split the file at the commas 
    #     firstStrip = [x.strip() for x in line.split(',')]
    #     #strip each line of unnecessary white space
    #     readLine = [x for x in firstStrip if x.strip()]
    #     #don't include empty rows 
    #     if len(readLine) == 0:
    #         pass
    #     else:
    #         #Check if the data is a valid integer/float 
    #         if (isFloat(readLine[0])) and (isFloat(readLine[1])):
    #             #print(readLine)
    #             #Append the data to the list of x or y variables 
    #             x_variables.append(float(readLine[0]))
    #             y_variables.append(float(readLine[1]))
                
    # #Plot the data 
    # plt.plot(x_variables, y_variables)
    # plt.scatter(x_variables, y_variables)
    # #x_variables, y_variables = zip(*sorted(zip(x_variables, y_variables)))
    # #print(x_variables)
    # #print(y_variables)
    # plt.xlabel("Time")
    # plt.ylabel("Magnitude")
    # plt.show()
    
        
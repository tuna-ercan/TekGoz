'''
tekgozl.py - library of functions to control the tekgoz robot arm
'''

import serial
import serial.tools.list_ports
import time
import threading


#TODO: Make TekGoz use this once we verify that the other functionality is working
class AngleDict(dict):
    '''
    Custom dictionary class.
    Python doesn't call setters when modifying dict values individually,
    so we define a custom dict type that checks limits.
    '''
    def __init__(self, limits):
        self.limits=limits

    def __setitem__(self, key, value):
        '''
        called when angles are modified. checks if the angles are within limits.
        '''
        # existence check
        if key in self.limits:
            # limit check
            if value>=self.limits[key][0] and value<=self.limits[key][1]:
                super().__setitem__(key, value) # save angle
            else:
                print(f"ERROR: joint {key} value off-limits")
        else:
            print(f"ERROR: joint {key} doesn't exist on the robot")

class TekGoz():
    def __init__(self, portname):
        self.portname=portname # name of serial port to connect to
        self.baudrate=9600 # arduno firmware is set to 9600, so default is 9600
        self.limits={"T" :[0,180],
                     "WP":[75,140],
                     "WR":[0,90],
                     "L" :[0,180],
                     "EP":[0,30],
                     "ET":[0,70]} # angle limits for the servos. [min max]
        self._angles={j:self.limits[j][0] for j in self.limits} # current angles of the servos. Initialized to the min values.
        self.last_time=time.time()
        self.rate_limit = 0.1 # rate limit in seconds
        self.request_list = [] # message list
        self.__thread_starter__()

    def __request_handler_thread__(self):
        while True:
            if self.port.isOpen():
                if((time.time() - self.last_time) >= self.rate_limit and len(self.request_list) > 0):
                    self.port.write(self.request_list.pop(-len(self.request_list))) # send message
                    #print("sent message")
                    self.last_time = time.time()
            else:
                print("ERROR: port not open yet! Call connect()")
                break

    def __thread_starter__(self): 
        threading.Thread(target=self.__request_handler_thread__, args=()).start()
        print("Thread Started")

    def connect(self):
        '''
        establish a serial connection using portname and baudrate
        '''
        self.port=serial.Serial(port=self.portname, baudrate=self.baudrate)

    @property
    def angles(self):
        return self._angles
    
    @angles.setter
    def update_angles(self,new_angles):
        '''
        NOT WORKING. CHANGE DICT TYPE TO AngleDict FOR POTENTIAL FIX.
        called when angles are modified. checks if the angles are within limits.
        
        inputs: 
            new_angles: dict, similar to self.angles
        '''
        raise("the angles setter is currently broken")
        for j in self.angles:
            # existence check
            if j in new_angles:
                # limit check
                if new_angles[j]>=self.limits[j][0] and new_angles[j]<=self.limits[j][1]:
                    self._angles[j]=new_angles[j] # save angle
                else:
                    print(f"ERROR: joint {j} value off-limits")
            else:
                print(f"ERROR: joint {j} doesn't exist in new_angles, should exist")
            

    def send_command(self):
        '''
        add the stored current angle values to the request list.
        '''
        print(f"added to queue: T{self._angles['T']:03}WP{self._angles['WP']:03}WR{self._angles['WR']:03}L{self._angles['L']:03}EP{self._angles['EP']:03}ET{self._angles['ET']:03}\n")
        self.request_list.append(f"T{self._angles['T']:03}WP{self._angles['WP']:03}WR{self._angles['WR']:03}L{self._angles['L']:03}EP{self._angles['EP']:03}ET{self._angles['ET']:03}\n".encode())



    #Set/Get Commands...

    def getT(self):
        return self._angles["T"]

    def setT(self, new_angle):
        if new_angle>=self.limits["T"][0] and new_angle<=self.limits["T"][1]:
            self._angles["T"]=new_angle # save angle
        else:
            print("ERROR: joint T value off-limits")

#

    def getWP(self):
        return self._angles["WP"]

    def setWP(self, new_angle):
        if new_angle>=self.limits["WP"][0] and new_angle<=self.limits["WP"][1]:
            self._angles["WP"]=new_angle # save angle
        else:
            print("ERROR: joint WP value off-limits")

#

    def getWR(self):
        return self._angles["WR"]
                           
    def setWR(self, new_angle):
        if new_angle>=self.limits["WR"][0] and new_angle<=self.limits["WR"][1]:
            self._angles["WR"]=new_angle # save angle
        else:
            print("ERROR: joint WR value off-limits")

#

    def getL(self):
        return self._angles["L"]
                           
    def setL(self, new_angle):
        if new_angle>=self.limits["L"][0] and new_angle<=self.limits["L"][1]:
            self._angles["L"]=new_angle # save angle
        else:
            print("ERROR: joint L value off-limits")

#

    def getEP(self):
        return self._angles["EP"]
                           
    def setEP(self, new_angle):
        if new_angle>=self.limits["EP"][0] and new_angle<=self.limits["EP"][1]:
            self._angles["EP"]=new_angle # save angle
        else:
            print("ERROR: joint EP value off-limits")

#

    def getET(self):
        return self._angles["ET"]
                           
    def setET(self, new_angle):
        if new_angle>=self.limits["ET"][0] and new_angle<=self.limits["ET"][1]:
            self._angles["ET"]=new_angle # save angle
        else:
            print("ERROR: joint ET value off-limits")

#
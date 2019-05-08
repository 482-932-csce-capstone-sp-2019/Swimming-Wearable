import math
import time
import board
import digitalio
import busio
import adafruit_lis3dh
import threading
import random
import json
from gpiozero import LED
from time import sleep
import _thread

# suffix of file to write raw data
RAW_DATA_FILE = "_data.txt"

# file from which target values for workout will be read
INPUT_FILE = "workout-pre.json"

# flag for flipturn occurence
FLIP_TURN = False

# flag for collecting data (turns false when is inactive)
COLLECT = True

# length of the window (in seconds) for which accelerometer data will be analyzed for flip turn detection
WINDOW = 0.25

# pseudo polling rate for accelerometer (in seconds)
RATE = 0.01

# connect vibrotactile feedback motors to GPIO pins
# left side
a = LED(25)
b = LED(16)
c = LED(26)
d = LED(13)

# right side
e = LED(17)
f = LED(27)
g = LED(22)
h = LED(24)

x = [a,b,c,d,e,f,g,h]


# function for buzzing motors
# Uses the GPIO library to buzz the motors
def BUZZ(pattern):

        if (pattern == "startProgram"):

                # hull-a-ba-loo
                for _ in range(0,4):
                        for item in x:
                                item.on()
                        time.sleep(0.2)
                        for item in x:
                                item.off()
                        time.sleep(0.1)

                time.sleep(0.2)

                # ca-neck
                for _ in range(0,2):
                        for item in x:
                                item.on()
                        time.sleep(0.2)
                        for item in x:
                                item.off()
                        time.sleep(0.1)

                time.sleep(0.2)

                # ca-neck
                for _ in range(0,2):
                        for item in x:
                                item.on()
                        time.sleep(0.2)
                        for item in x:
                                item.off()
                        time.sleep(0.1)

        elif( pattern == "startRep"):
                print("start rep")
                # start rep (long buzz)
                for item in x:
                        item.on()
                time.sleep(1.0)

                for item in x:
                        item.off()

        elif ( pattern == "speedUp"):
                print("speed up b ")
                # ca-neck
                for _ in range(0,3):
                        for item in x:
                                item.on()
                        time.sleep(0.2)
                        for item in x:
                                item.off()
                        time.sleep(0.1)

        elif ( pattern == "stop"):
                print("stop")
                # stop rep (2 medium buzz)
                for _ in range(0,2):
                        for item in x:
                                item.on()
                        time.sleep(0.5)

                        for item in x:
                                item.off()

        elif ( pattern == "endProgram"):
                print("end program")
                # ca-neck
                for _ in range(0,3):
                        for item in x:
                                item.on()
                        time.sleep(0.2)
                        for item in x:
                                item.off()
                        time.sleep(0.1)

        else:
                #this should never happpen
                print("Undetected pattern")

                # hull-a-ba-loo
                for _ in range(0,4):
                        for item in x:
                                item.on()
                        time.sleep(0.2)
                        for item in x:
                                item.off()
                        time.sleep(0.1)

                time.sleep(0.2)

                # ca-neck
                for _ in range(0,2):
                        for item in x:
                                item.on()
                        time.sleep(0.2)
                        for item in x:
                                item.off()
                        time.sleep(0.1)

                time.sleep(0.2)

                # ca-neck
                for _ in range(0,2):
                        for item in x:
                                item.on()
                        time.sleep(0.2)
                        for item in x:
                                item.off()
                        time.sleep(0.1)



# Queue for holding window of data
# Current method of flip turn detection relies on a queue and uses the average over a 3 second period
class Queue:

        # Properties
        arr = []
        pop = False

        totX = 0
        totY = 0
        totZ = 0

        # Methods
        def setPop(self, pop):
                self.pop = pop

        def push(self, data):
                self.arr.append(data)
                self.totX += data[0]
                self.totY += data[1]
                self.totZ += data[2]

                if (self.pop) :
                        poppedData = self.popFirst()

        def popFirst(self):
                poppedData = self.arr.pop(0)
                self.totX -= poppedData[0]
                self.totY -= poppedData[1]
                self.totZ -= poppedData[2]
                return poppedData

        def popLast(self):
                poppedData = self.arr.pop(len(self.arr)-1)
                self.totX -= poppedData[0]
                self.totY -= poppedData[1]
                self.totZ -= poppedData[2]
                return poppedData


        def getTotals(self):
                length = len(self.arr)
                return ( float( self.totX / length ), float( self.totY / length ), float( self.totZ / length ) )


# Call this function to check if a flip turn has occured
# Our mentor (Larry) gave us these numbers to determine a flip turn
#       Note that hitting 8 G's over a 3 second period seems pretty hard but we used numbers provided
def check_average():
        avg = myQueue.getTotals()
        if (avg[0] > -1.6074657040557025 and avg[1] > 0.7000170728387815 and avg[2] > 8.430353502139699) :
                print("Flip turn detected")
                return True
        return False

myQueue = Queue()

# The main function of the program is broken down into 3 main steps
#       1 Open the file to read in and wait so swimmer can enter the water
#       2 Create the varibles for flip turn detection later
#       3 Creates variables for the logic of the workout
def main(fileName):
    with open('workout-pre.json') as json_data:
        data = json.load(json_data)

    print ("--------------  1  ------------------\n")
    # begin the program based on a delay to allow the swimmer to enter the water carefully
    print("BUZZ after time(30 seconds)")
    #_thread.start_new_thread(BUZZ, ("startProgram",))
    #time.sleep(30)
    print("Making the file and queue for the program")
    file = open(fileName, "a+")


    print ("--------------  2  ------------------\n")
    # create a list of the sets, set based on the workout-pre.json
    # also get current time for comparison later

    set_list = data["set"]
    rest_list = data["rest_time"]
    # should have 1 more set then the rest between the sets
    if ( len(set_list) - len(rest_list) != 1):
        print("Invalid JSON provided. Rest given should be 1 less then sets")

    #time in seconds since 1970, used to avoid messing with dates, time will be used with seconds
    start_time = int(time.time())

    # Make the queue run until full
    windowEnd = time.time() + WINDOW
    while(time.time() < windowEnd):
            x, y, z = [value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration]
            myQueue.push((x,y,z))
            file.write("%s, %s, %s, %s\n" % (x, y, z, time.time()))
    myQueue.setPop(True)


    print ("--------------  3  ------------------\n")
    # run over the sets based on the given time and BUZZ when rep starts


    next_rep_start = start_time
    next_flip_turn = start_time
    current_set_number = 0

    total_sets = len(set_list)
    # For each set remaining in the workout
    while (current_set_number < total_sets):
        reps_in_set = int(set_list[current_set_number]['reps'])
        distance_per_rep = int(set_list[current_set_number]['distance'])
        time_to_complete = int(set_list[current_set_number]['time_to_complete'])
        target_time = int(set_list[current_set_number]['target_time'])
        time_per_rep = target_time / distance_per_rep * 25

        next_rep_start += time_to_complete
        next_flip_turn += time_per_rep

        # For each rep remaining in the set
        for rep_number in range(0, reps_in_set):

            print("BUZZ performing rep %d" % (rep_number))
            _thread.start_new_thread(BUZZ, ("startRep",))

            # still on the same rep
            while(time.time() < next_rep_start):

                # you missed the target flip turn time
                if ( time.time() > next_flip_turn):
                    print("BUZZ Missed Flip Turn Time")
                    _thread.start_new_thread(BUZZ, ("speedUp",))
                    next_flip_turn += time_per_rep

                else:

                    x, y, z = [value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration]
                    myQueue.push((x,y,z))
                    file.write("%s, %s, %s, %s\n" % (x, y, z, time.time()))


                    if(check_average()):
                        file.write("Flip Turn Detected at %s" % (time.time()))

                time.sleep(RATE)


            next_rep_start += time_to_complete_rep


        # have now completed a set, get the rest time (unless that was last set)
        if(current_set_number == len(rest_list)):
            print("Workout Complete")
            _thread.start_new_thread(BUZZ, ("endProgram",))
        else:
            print("I will wait for " + rest_list[str(current_set_number+1)] + " seconds")
            _thread.start_new_thread(BUZZ, ("stop",))

        current_set_number += 1
        # at end of set do the rest that matches, if last set then done


# Hardware I2C setup.
print("Setting up accelerometer via I2C")
i2c = busio.I2C(board.SCL, board.SDA)
int1 = digitalio.DigitalInOut(board.D6)  # Set to correct pin for interrupt!
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_16_G

#lis3dh.set_tap(1, 30)

# Runnnnnnnnnn
fileName = str(time.time()) + RAW_DATA_FILE
main(fileName)

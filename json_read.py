'''
read the workout-pre.json
sleep (short_time); buzz to tell swimmer that program is now going
turn workout-pre.json into known timestamps with data that it uses
'''

import json
import time

def main():
    with open('workout-pre.json') as json_data:
        data = json.load(json_data)

    print ("--------------  1  ------------------")
    print ("-------------------------------------\n")
    # begin the program based on a delay to allow the swimmer to enter the water carefully
    print("BUZZ after time(60 seconds)")
    print ("-------------------------------------")
    print("-------------------------------------\n")


    print ("--------------  2  ------------------")
    print ("-------------------------------------\n")
    # create a list of the sets, set based on the workout-pre.json
    # also get current time for comparison later

    set_list = data["set"]
    rest_list = data["rest_time"]
    # should have 1 more set then the rest between the sets
    if ( len(set_list) - len(rest_list) != 1):
        print("Invalid JSON provided. Rest given should be 1 less then sets")

    #time in seconds since 9170, used to avoid messing with dates, time will be used with seconds
    start_time = int(time.time())

    print ("-------------------------------------")
    print("-------------------------------------\n")


    print ("--------------  3  ------------------")
    print ("-------------------------------------\n")
    # run over the sets based on the given time and BUZZ when rep starts

    # NOTE may want to redo the way these 2 time variable points are used
    next_time_point = start_time
    next_flip_turn = start_time
    current_set_number = 0
    total_sets = len(set_list)
    while (current_set_number < total_sets):
        reps_in_set = int(set_list[current_set_number]['reps'])
        distance_per_rep = int(set_list[current_set_number]['distance'])
        time_to_complete = int(set_list[current_set_number]['time_to_complete'])
        target_time = int(set_list[current_set_number]['target_time'])
        time_per_rep = target_time / distance_per_rep * 25
        next_time_point += time_to_complete
        next_flip_turn += time_per_rep

        for rep_number in range(0, reps_in_set):

            print("BUZZ performing rep %d" % (rep_number))

            current_lap_number = 0

            while(time.time() < next_time_point):
                # Add data to the queue
                # if (check_average() == FLIP_TURN):
                    # if (time.time() > next_flip_turn /*you flipped after when you want to*/):
                        # BUZZ
                    # current_lap_number += 1
                time.sleep(0.1)
            next_time_point += time_to_complete


        # have now completed a set, get the rest time (unless that was last set)
        if(current_set_number == len(rest_list)):
            print("Workout Complete")
        else:
            print("I will wait for " + rest_list[str(current_set_number+1)] + " seconds")

        current_set_number += 1
        # at end of set do the rest that matches, if last set then done

    print ("-------------------------------------")
    print("-------------------------------------\n")


main()

'''{
  "swimmer": "swimmer-name",
  "set": [
    {
      "reps": "1",
      "distance": "300",
      "time_to_complete": "300",
      "target_time": "240",
      "times": [
        {
          "1": ""
        }
      ]
    },
    {
      "reps": "3",
      "distance": "200",
      "time_to_complete": "240",
      "target_time": "180",
      "times": [
        {
          "1": "",
          "2": "",
          "3": ""
        }
      ]
    },
    {
      "reps": "5",
      "distance": "100",
      "time_to_complete": "120",
      "target_time": "90",
      "times": [
        {
          "1": "",
          "2": "",
          "3": "",
          "4": "",
          "5": ""
        }
      ]
    }
  ],
  "rest_time": {
    "1": "120",
    "2": "180"
  }
}
'''

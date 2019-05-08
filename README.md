# Team Swimming

This program is a simple final version of the device program. Prior versions of the code attempted machine learning which was removed for various reasons.

### Included Files in this repository:

  - `example.py` - Main code to be ran
  - `workout_pre.json` - Pre loaded workout to be swam. Updated by the app
  - `_data.txt` - Printout of all data to be used with the app

## Products Used:

  - [Adafruit LIS3DH](https://www.adafruit.com/product/2809)

### Required Libraries / Prerequisites:

  - [LIS3DH with tutorial (also CircuitPython / Adafruit Blinka)](https://learn.adafruit.com/adafruit-lis3dh-triple-axis-accelerometer-breakout/python-circuitpython)
  - Enable GPIO on pi

### Initial Testing

To get the project into a testable state the first major task is to wire the haptic motors into the [same pinout](https://pinout.xyz/#) as the code. Then after enabling the GPIO on the pi commenting out the workout sections or passing in a BUZZ pattern should make the motors BUZZ.

If the motors are buzzing then the next step is to make sure the accelerometer works.
Having installed the LIS3DH library and wiring the accelerometer in the same way as the link above the hardware side is done. To test print out the data as seen in the LIS3DH tutorial (linked above). That code should be able to display the x,y,z data (assuming all the library requirments are met).

### Run the program

    python3 example.py

### Notes

  - This project is not for the faint of heart.
  - The code was a machine learning version however that was trimmed down. This is a simple workout parsing and buzzing version to provide feedback. The *only* connection currently on the swimmer's movement at the moment is **flip turn detection**.
  - **Flip turn detection** never works, yeah. Our mentor gave us values for the x,y,z of the swimmer over a 3 second window. The z average over the window needs to be over 8 G's, which was never met. We continued to test new values however there was never a consistent detection number.

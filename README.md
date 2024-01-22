MAFCE
===

MAFCE stands for "Mecanismo para la Aplicación de Fuerzas Controladas Electrónicamente" (Mechanism for the Application of Electronically Controlled Forces in Spanish) and it is the machine I designed and built for my Final Project for my Mechanical Engineering Degree.
This project was carried out with the help and support of Beatriz Santamaría Fernández and Miguel Berzal Rubio.
The Final Project paper (in Spanish) can be found [here](https://oa.upm.es/77062/).

The code for reading the HX711 ADC for Weigh Scales on Rasperry PIs (hx711.py script) was taken from [Marcel Zak's repository](https://github.com/gandalf15/HX711/) with a few tweaks, but the rest of the code was developed by me.


![mafce](https://github.com/inigorrix/mafce/blob/main/docs/mafce.jpg?raw=true)

![assembly](https://github.com/inigorrix/mafce/blob/main/docs/assembly.gif?raw=true)

This repository contains both the code of the UI and the instructions for the robot.
The user is able to control the machine using a touchscreen.
Below is an overview of the five tabs of the UI and a brief description of what each of them is for.


![home](https://github.com/inigorrix/mafce/blob/main/docs/home.png?raw=true)

### Home/Help
Welcome to MAFCE (Mechanism for the Application of Forces Controlled Electronically)!
You can access the different tabs of the program by clicking on the menu on the left.
And if you have any questions about how it works, you can read the manual for each tab here.


![sim1](https://github.com/inigorrix/mafce/blob/main/docs/sim1.png?raw=true)

### Weight Simulation
Simulate Weight is the main tab of MAFCE.
Here you select the weight you want to simulate and when you press the START button, the motor will start. There are three ways to simulate the weight: dragging the slider, entering it on the numeric keypad and pressing ENTER, or adding or subtracting the default values. The resolution of the slider can be changed in the Settings tab.

Once the simulation begins, the START button becomes the STOP button. The screen shows the simulated weight at each moment and the error with respect to the weight to be simulated. When the current error is greater than the allowable error, the box is yellow and when it is within range, the box is green. The allowable error value can be modified in the Settings tab.


![mot1](https://github.com/inigorrix/mafce/blob/main/docs/mot1.png?raw=true)

### Motor
The Motor tab allows you to directly control the movement of the motor.
There is a slider to adjust the turning speed. In the Settings tab you can determine the maximum and minimum value of the speed, as well as the number of divisions of the slider.

The motor can be rotated in both directions and in two modes: the first is to rotate while the button is held down and the second is to press the button and the motor rotates automatically until the button is pressed again and then it stops.

At the bottom of the screen the speed is shown in revolutions per minute and revolutions per second. This value is a fairly precise approximation, but not exact.

At the top the weight is shown while the motor is spinning. When it stops, the weight value is the last measured when the motor was spinning.


![scale](https://github.com/inigorrix/mafce/blob/main/docs/scale.png?raw=true)

### Scale
In the Scale tab the simulated weight is shown at all times. This weight is equal to the weight hanging from the load cell plus the weight of the load cell itself. The load cell weight value can be modified from the Settings tab or by pressing the 'Change load cell weight' button.

This tab also allows you to calibrate the load cell. To do this, press the 'Calibrate load cell' button and follow the instructions that appear in the black box, which include hanging a known weight and entering the value of said weight using the numeric keypad.

It also allows obtaining an approximation of the system's rigidity. The estimate of k will be displayed on the screen, but the value must be saved by the user in the Settings tab.


![settings](https://github.com/inigorrix/mafce/blob/main/docs/settings.png?raw=true)

### Settings
The Settings tab offers the possibility of changing the values of some parameters with which the machine works. To do this, select a property from the list and enter the desired value on the numeric keypad and pressing ENTER will convert it to the current value of said property.

The 'Apply changes only to this session' button takes the user to the Simulate Weight tab to use the program with the changes made. The 'Save this settings' button makes all saved values the same as the current values. The saved values are those that the program assigns to each property each time it is started. The 'Undo changes' button makes the current values the same as the saved values. And the 'Restore Defaults' button makes the current values the same as the default values.
# This is version 2 of the Control GUI for my Capstone project.
# It includes a safety system for the fire control, an elevation indicator,
# and the potential for linking to another camera to read the pressure gage.

# OPERATIONAL NOTES:
# The fire button only enables when all three checkboxes are checked, providing a triple-redundant safety.
# The cinch button only enables after the fire button has been pressed.
# The drag deploy button only enables after the cinch button has been pressed.

# SPECIAL NOTE: If the fire, cinch, or drag buttons break, add a global definition directly above its first use inside a function.

from __future__ import division # servo
import Tkinter as tk # GUI
import cv2 # Pressure Gage
from PIL import Image, ImageTk # Pressure Gage
import time # servo and LIDAR
import math # servo
import Adafruit_PCA9685 # servo
import smbus # LIDAR

# Some LIDAR initializers
bus=smbus.SMBus(1)
addr=0x62

##import tkMessageBox as mb # This is just so that there is a dialog box that pops up to confirm the fire.

root = tk.Tk() # initialize the window.
root.geometry('590x420') # Sets the default window size
root.title("Control GUI")

# ****************************************************************************
# This section contains the elevation indicator.
elevationLabel = tk.Label(root, text = "Elevation (deg):", font = 20)
elevationValue = tk.DoubleVar() # this holds the actual elevation value
eleValOut = tk.Label(root, text = "0.0", font = 20) # The specific label for displaying the elevation.

def getElevation(elevation): # a function for changing the elevation value.
    elevationValue.set(elevation)

def updateEle(root, *args): # called when the elevation value is changed.
    eleValOut.config(text = elevationValue.get())

elevationValue.trace("w", updateEle)

elevationLabel.grid(row=0, column=0)
eleValOut.grid(row=0, column=1)

# ****************************************************************************
# This section contains the rotation indicator.
rotationLabel = tk.Label(root, text = "Rotation (deg):", font = 20)
rotationValue = tk.DoubleVar() # this holds the actual rotation value
rotValOut = tk.Label(root, text = "0.0", font = 20) # The specific label for displaying the rotation.

def getRotation(rotation): # a function for changing the rotation value.
    rotationValue.set(rotation)

def updateRot(root, *args): # called when the rotation value is changed.
    rotValOut.config(text = rotationValue.get())

rotationValue.trace("w", updateRot)

rotationLabel.grid(row=1, column=0)
rotValOut.grid(row=1, column=1)

# ****************************************************************************
# This section contains the range indicator.
rangeLabel = tk.Label(root, text = "Distance to Target:", font = 20)
rangeValue = tk.DoubleVar() # this holds the actual range value
ranValOut = tk.Label(root, text = "0.0", font = 20) # The specific label for displaying the range.

def getRange(dist): # a function for changing the range value.
    rangeValue.set(dist)

def updateRan(root, *args): # called when the range value is changed.
    ranValOut.config(text = rangeValue.get())

def rangeFind(): # This section is the LIDAR code
    t_end = time.time() + 5
    while time.time() < t_end:
        bus.write_byte_data(0x62,0x00, 0x04)   
        val_high=bus.read_byte_data(0x62,0x0f)   
        val_low=bus.read_byte_data(0x62,0x10)   
        dist_cm=val_high*256+val_low
        dist_ft=dist_cm*0.0328084
        getRange(dist_ft)
        #print `dist_ft` + " ft   "
        time.sleep(0.05)

rangeValue.trace("w", updateRan)

uRanButton = tk.Button(root, text='Update Range', command=rangeFind)

rangeLabel.grid(row=2, column=0)
ranValOut.grid(row=2, column=1)
uRanButton.grid(row=2, column=2)

# ****************************************************************************
# This section contains the video for reading the pressure gage. It is purely optional.
##picW = 320
##picH = 214
##ImageFrame=tk.Frame(root,width=picW,height=picH)
##lmain=tk.Label(ImageFrame)
##gageLabel = tk.Label(root, text = "Pressure Gage:", font = 20)
##
##cap=cv2.VideoCapture(0) # sets the camera
##
##def getVideo():
##   _,frame = cap.read()
##   hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
##   hsv = cv2.resize(hsv, (picW, picH), interpolation=cv2.INTER_AREA)
##   img=Image.fromarray(hsv)
##   imgtk=ImageTk.PhotoImage(image=img)
##   lmain.imgtk=imgtk
##   lmain.configure(image=imgtk)
##   lmain.after(10,getVideo)
##   
##getVideo() # This actually uses the camera to capture images. You may delete it.
##gageLabel.grid(row=3, column=0)
##ImageFrame.grid(row=3, column=1) # keep these locations the same.
##lmain.grid(row=3, column=1) # keep these locations the same.

# ****************************************************************************
# This section contains the fire control and safety system.
# these are the variables controlled by the checkboxes.
flag1 = tk.BooleanVar()
flag2 = tk.BooleanVar()
flag3 = tk.BooleanVar()
fireState = tk.BooleanVar(value=False)

def fire():
    # Insert whatever code we want here. It could just be a print statement.
    #mb.showinfo('FIRE', 'BOOM')
    print("BOOM")
    fireState.set(True)

fireButton = tk.Button(root, state=tk.DISABLED, text='Fire', command=fire) # sets the fire button to disabled by default.
    
def safetySys(root, *args): # The parameters of this function are automatically generated by the trace call.
    if all([flag1.get(), flag2.get(), flag3.get()]): # If all 3 checkboxes are checked, enable the fire button.
        fireButton.config(state=tk.NORMAL)
    else: # If not, disable the fire button for safety.
        fireButton.config(state=tk.DISABLED)

# The locations of the safety boxes and fire button        
tk.Checkbutton(root, variable=flag1).grid(row=4, column=0)
tk.Checkbutton(root, variable=flag2).grid(row=4, column=1)
tk.Checkbutton(root, variable=flag3).grid(row=4, column=2)
fireButton.grid(row=5, column=1)

# These lines watch for a change in the variables controlled by the checkboxes.
flag1.trace("w", safetySys)
flag2.trace("w", safetySys)
flag3.trace("w", safetySys)

# ****************************************************************************
# This section contains the cinch control
cinchState = tk.BooleanVar(value=False)
def cinch():
    # Insert whatever code we want/need here.
    #mb.showinfo('CINCH', 'WHIRRRRRRRR')
    print("WHIRRRRRRRRR")
    fireState.set(False)
    cinchState.set(True)

cinchButton = tk.Button(root, state=tk.DISABLED, text='Cinch', command=cinch) # sets the cinch button to disabled by default

def enableCinch(root, *args): # if the fire button has been pressed, enable the cinch button.
    if fireState.get():
        cinchButton.config(state=tk.NORMAL) # enables the cinch button.
    else:
        cinchButton.config(state=tk.DISABLED)

fireState.trace("w", enableCinch) # when the fireState variable changes, check if you should enable the cinch button.

cinchButton.grid(row=6, column=1)

# ****************************************************************************
# This section contains the drag device control
def dragDeploy():
    # Insert whatever code we want/need here.
    #mb.showinfo('Deploy Confirm', 'Junk Deorbiting')
    print("Junk Deorbiting")

dragButton = tk.Button(root, state=tk.DISABLED, text='Drag Device', command=dragDeploy) # sets the drag button to disabled by default

def enableDrag(root, *args): # if the cinch button has been pressed, enable the drag device button
    dragButton.config(state=tk.NORMAL) # enables the drag button.

cinchState.trace("w", enableDrag) # when the cinchState variable changes, check if you should enable the drag button.

dragButton.grid(row=7, column=1)

# ****************************************************************************
### debug window. Manually change elevation and rotation.
##dew = tk.Toplevel() # define an entirely seperate window for the entries
##dew.geometry('320x75')
##dew.title("Debug Window")
##deELab = tk.Label(dew, text = "Enter Elevation:", font = 20) # the labels
##deRLab = tk.Label(dew, text = "Enter Rotation:", font = 20)
##deRgLab = tk.Label(dew, text = "Enter Range:", font = 20)
##
##elevationEntry = tk.Entry(dew) # the entry fields
##rotationEntry = tk.Entry(dew)
##rangeEntry = tk.Entry(dew)
##
##def passEle(event):
##    getElevation(elevationEntry.get()) # get the value in the field and pass it to the get function.
##
##def passRot(event):
##    getRotation(rotationEntry.get()) # get the value in the field and pass it to the get function.
##    
##def passRan(event):
##    getRange(rangeEntry.get()) # get the value in the field and pass it to the get function.
##
##elevationEntry.bind("<Return>", passEle) # get the number in the entry field when enter is pressed.
##rotationEntry.bind("<Return>", passRot) # get the number in the entry field when enter is pressed.
##rangeEntry.bind("<Return>", passRan)
##
##deELab.grid(row=0, column=0)
##elevationEntry.grid(row=0, column=1)
##deRLab.grid(row=1, column=0)
##rotationEntry.grid(row=1, column=1)
##deRgLab.grid(row=2, column=0)
##rangeEntry.grid(row=2, column=1)

# ****************************************************************************
# This section is for the motor motion.
pwm = Adafruit_PCA9685.PCA9685()

minMotionX = 380 # The maximum servo motion left and right (pan)
minMotionY = 150
maxMotionX = 470 # The maximum servo motion left and right (pan)
maxMotionY = 670 # The maximum servo motion up and down (tilt)
moveDis = 1 # Tells the key presses how far to move each time

tiltSet = 530 # Sets start and end position of motor
panSet = 413  # Sets start and end position of motor # 410

curX = panSet # Holds the current x position
curY = tiltSet # Holds the current y position # 400

pwm.set_pwm_freq(60) # Set frequency to 60hz, good for servos.
pwm.set_pwm(14, 14, panSet) # Set X starting position
pwm.set_pwm(15, 15, tiltSet) # Set Y starting position # 387
print('Initializing servos on channel 0 and 1, "X" GUI window to quit...')
print('If cv2 color doesnt run: close the program, give it 5 seconds, then try again')

# ------------------------------
# Servo functions
def updatePos():
    
    pwm.set_pwm(15, 15, curY)

    # These Lines Translate curX,curY into reference (X,Y) coordinates for user
    coordX = curX-panSet
    coordY = -(curY-tiltSet) # Sign is flipped because Torxis motors read PWM backwards from mini servos
##    print(coordX,coordY) # Print current X,Y servo positions
    # These Lines output an angle from linear fit calibration based on known angles and PWM signals (coordY) 
    pitchAngle = -.000003*coordY*coordY*coordY + .0016*coordY*coordY + .2399*coordY + .1111
    panAngle = .000002*coordX*coordX*coordX*coordX + .0001*coordX*coordX*coordX - .0041*coordX*coordX + 1.1562*coordX - 1.6779
    getElevation(pitchAngle)
    getRotation(panAngle)
##    print(panAngle,'Pan Degrees')   # Diplays servo pan angle from zero
##    print(pitchAngle,'Tilt Degrees') # Displays servo pitch angle from local horizontal
##    print(' ') # To indent different displayed values per servo position
    
    pwm.set_pwm(14, 14, curX)
    return

def keyMotionUp(event):
    #print("Key Down")
    global curY
    moveDis = 1
    curY -= moveDis
    if curY > maxMotionY: # The "-21" here is to keep the x on the screen. This may be deleted for the actual motors
        curY = maxMotionY
    updatePos()
    return

def keyMotionDown(event):
    #print("Key Up")
    global curY
    moveDis = 1
    curY += moveDis
    if curY < minMotionY:
        curY = minMotionY
    updatePos()
    return

def keyMotionLeft(event):
    #print("Key Left")
    global curX
    moveDis = 1
    curX -= moveDis
    if curX < minMotionX:
        curX = minMotionX
    updatePos()
    return

def keyMotionRight(event):
    #print("Key Right")
    global curX
    moveDis = 1
    curX += moveDis
    if curX > maxMotionX - 12: # The "-12" here is to keep the x on the screen. This may be deleted for the actual motors
        curX = maxMotionX - 12
    updatePos()
    return
# ---------------Fast Key Options-----------------
def keyMotionFastUp(event):
    #print("Key Down")
    global curY
    moveDis = 5
    curY -= moveDis
    if curY > maxMotionY - 21:
        curY = maxMotionY - 21
    updatePos()
    return

def keyMotionFastDown(event):
    #print("Key Up")
    global curY
    moveDis = 5
    curY += moveDis
    if curY < minMotionY:
        curY = minMotionY
    updatePos()
    return

def keyMotionFastLeft(event):
    #print("Key Left")
    global curX
    moveDis = 5
    curX -= moveDis
    if curX < minMotionX:
        curX = minMotionX
    updatePos()
    return

def keyMotionFastRight(event):
    #print("Key Right")
    global curX
    moveDis = 5
    curX += moveDis
    if curX > maxMotionX - 12: 
        curX = maxMotionX - 12
    updatePos()
    return
#------------------------------------

# End of servo functions
# -------------------------------------------
# The other bits: a bind and the prints.
root.bind('<Up>', keyMotionUp)     # These functions detect a directional keypress,
root.bind('<Down>', keyMotionDown) # then call the function that is the second argument.
root.bind('<Left>', keyMotionLeft)
root.bind('<Right>', keyMotionRight)
root.bind('<w>',keyMotionFastUp)
root.bind('<s>',keyMotionFastDown)
root.bind('<a>',keyMotionFastLeft)
root.bind('<d>',keyMotionFastRight)

# ****************************************************************************
root.mainloop() # Displays the GUI until the close button is pressed.
#cap.release() # shuts down the camera when the program is closed.

pwm.set_pwm(14, 14, panSet) # Set X ending position
pwm.set_pwm(15, 15, tiltSet) # Set Y ending position

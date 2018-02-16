# This program uses a GUI to show the position of an X inside a rectangle that can be moved by pressing the keys.
# It includes an easy way to update the servomotor controls (see the updatePos function).
# It should be noted that the positon of the X is actually measured from the top left corner of the rectangle, not from the 
# center of the X. In order to compensate for that, there is an allowance for the size of the box. This may be deleted
# when adding the motors.

import Tkinter as tk #If we are using Python 3, change "Tkinter" to "tkinter"
from PIL import Image,ImageTk  
import cv2
import numpy as np

curX = 0 # Holds the current x position
curY = 0 # Holds the current y position
moveDis = 5 # Tells the key presses how far to move each time
#12 21 # A reminder of the size of the box that the x is in (in pixels)

maxMotionX = 1000 # The maximum servo motion left and right (pan)
maxMotionY = 1000 # The maximum serco motion up and down (tilt)

#***************************************************************************************************************************************
#This section is for functions that need to be defined before running.

def updatePos():
   aim.place(x=curX, y=curY)
   #Put the servo update command here
   #Don't forget to look at the down and right motion functions when updating this.
   return

def mouseMotion(event): # This function is useful for determining the pixel location within the GUI window
   print("Mouse Position: (%s %s)" % (event.x, event.y))
   return

def keyMotionUp(event):
   #print("Key Up")
   global curY
   curY -= moveDis
   if curY < 0:
       curY = 0
   updatePos()
   return

def keyMotionDown(event):
   #print("Key Down")
   global curY
   curY += moveDis
   if curY > maxMotionY - 21: # The "-21" here is to keep the x on the screen. This may be deleted for the actual motors
       curY = maxMotionY - 21
   updatePos()
   return

def keyMotionLeft(event):
   #print("Key Left")
   global curX
   curX -= moveDis
   if curX < 0:
       curX = 0
   updatePos()
   return

def keyMotionRight(event):
   #print("Key Right")
   global curX
   curX += moveDis
   if curX > maxMotionX - 12: # The "-12" here is to keep the x on the screen. This may be deleted for the actual motors
       curX = maxMotionX - 12
   updatePos()
   return

def keyMotionUR(event):
   #print("Key Up-Right")
   global curX, curY
   curX += moveDis
   curY -= moveDis
   if curY < 0:
       curY = 0
   if curX > maxMotionX - 12: # The "-12" here is to keep the x on the screen. This may be deleted for the actual motors
       curX = maxMotionX - 12
   updatePos()
   return

def keyMotionUL(event):
   #print("Key Up-Left")
   global curX, curY
   curX -= moveDis
   curY -= moveDis
   if curY < 0:
       curY = 0
   if curX < 0:
       curX = 0
   updatePos()
   return

def keyMotionDR(event):
   #print("Key Down-Right")
   global curX, curY
   curX += moveDis
   curY += moveDis
   if curY > maxMotionY - 21: # The "-21" here is to keep the x on the screen. This may be deleted for the actual motors
       curY = maxMotionY - 21
   if curX > maxMotionX - 12: # The "-12" here is to keep the x on the screen. This may be deleted for the actual motors
       curX = maxMotionX - 12
   updatePos()
   return

def keyMotionDL(event):
   #print("Key Down-Left")
   global curX, curY
   curX -= moveDis
   curY += moveDis
   if curY > maxMotionY - 21: # The "-21" here is to keep the x on the screen. This may be deleted for the actual motors
       curY = maxMotionY - 21
   if curX < 0:
       curX = 0
   updatePos()
   return
def getVideo():
    # cap = cv2.VideoCapture(0)
    _,frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   
    # lower_red = np.array([30,150,50])
    # upper_red = np.array([255,255,180])
   
    # mask = cv2.inRange(hsv, lower_red, upper_red)
    # res = cv2.bitwise_and(frame,frame, mask= mask)
    img=Image.fromarray(hsv)
    imgtk=ImageTk.PhotoImage(image=img)
    lmain.imgtk=imgtk
    lmain.configure(image=imgtk)
    lmain.after(10,getVideo)
#***************************************************************************************************************************************
#This section is the main program.
root = tk.Tk()
root.resizable(width=False, height=False) # Prevents the user from changing the window size

root.minsize(width=maxMotionX, height=maxMotionY) # Makes the window match the motion of the servo
root.maxsize(width=maxMotionX, height=maxMotionY)

# This is the small bit of text that is going to move around the page.

root.title("display image")
#im=Image.open("MMIII.jpg")
#im=getVideo()
#photo=ImageTk.PhotoImage(im)
ImageFrame=tk.Frame(root,width=600,height=500)
ImageFrame.place(x=0,y=0)
lmain=tk.Label(ImageFrame)
lmain.place(x=0,y=0)

#cv = tk.Canvas()
cap=cv2.VideoCapture(0) # Number 0 or 1 to change which camera you use

#cv.pack(side='top', fill='both', expand='yes')
#cv.create_image(0, 0, image=photo, anchor='nw')
getVideo()
aim = tk.Label(root, text="X", fg = "black")

aim.place(x=curX, y=curY) # Initializes the X to the top left corner

#We can comment in the following line for debug purposes, if we need it.
#root.bind('<Motion>', mouseMotion) # Detects the position of the mouse within the GUI window.
root.bind('<Up>', keyMotionUp) # These functions detect a directional keypress,
root.bind('<Down>', keyMotionDown) # then call the function that is the second argument.
root.bind('<Left>', keyMotionLeft)
root.bind('<Right>', keyMotionRight)
#Currently, holding shift and a horizontal direction moves diagonally up in that direction.
#Similarly, holding Ctrl and a horizontal direction moves diagonally down in that direction.
root.bind('<Shift-Right>', keyMotionUR)
root.bind('<Shift-Left>', keyMotionUL)
root.bind('<Control-Right>', keyMotionDR)
root.bind('<Control-Left>', keyMotionDL)

root.mainloop() # Displays the GUI until the close button is pressed.

cap.release()

# CPPoo
A python input redirection script for 3ds

There are three versions of roughly the same script. Each script has a slightly different layouts for axes (see controller diagrams in BUTTONLAYOUTS/ for actual button layouts).  
**CPPoo.py** is for games that allow the buttons to move the player or camera 
* Analog to digital conversion to map the right thumbstick to A,B,X,Y
* NOT an emulation of  the Circle Pad Pro

**o3ds.py** is for the old/original 3DS (as well as 2DS and 3DS XL)
* The right thumbstick moves a cursor on the touch screen and R2 analog acts as touching the screen in that location. 
* ZL/ZR and c-stick will not work for o3DS models (disabled in luma)

**n3ds.py** is for the 'new' 3DS (as well as  'new' 3DS XL and 'new' 2DS)
* Thumbstick #2 is bound to c-stick

Note: In all versions clicking the pygame touchscreen with the mouse will act as tapping the 3DS touchscreen

CPPoo.py was originally targeted for the xbox 360 controller, so the script may not work if the controller is much different. At a minimum the controller needs 2 axis (up/down and left/right) and a similar number of buttons to the 3DS.  CPPoo is cross platform, but it was tested (and written) on Linux. o3ds.py and n3ds.py are included as more traditional controller setups. 

0) Why xbox 360 controllers?
Because that's my setup. The xbox 360 controller doesn't comply with HID device specifications, so button mapping isn't consistent across platforms. I also only have an o3DS, so n3DS wasn't properly tested. Caveat emptor!


1) Software dependencies 
- Python 3
- Pygame 
- TPPFLUSH


2) Button mapping on controller
Before starting, run `controller_setup.py` in the terminal to create a configuration file for your controller. Without a configuration file the script will use a default button mapping which may not make sense with your controller. CPPoo.py needs at least 2 joysticks to work properly. o3ds.py and n3ds.py expect at least 1 joystick. All three scripts use the keys in the keyboard layout (KB_all.png). 


3) Start up
Before running the script, on the 3ds turn wifi and input redirection in Luma's Rosalina menu (L+d-pad_down+Select) Miscellaneous options > Start InputRedirection. 

The script needs the 'lib' and 'tpp' folders in the same directory to run eg
- CPPoo.py
- n3ds.py
- o3ds.py
- controller_setup.py
- lib/
  - controller.py
  - bottom.png
- (etc)

you can supply the IP address of the 3DS in the command line:
> $ python3 CPPoo.py 192.168.1.99

you can also run the script without the IP address
> $ python3 CPPoo.py 

and a box will pop up asking for the IP address. 

Setting the file to be executed as a program will allow you to double click the file to run it too!


4) Tips and Tricks

These keys are bound to the keyboard
- `Home` key is the 3DS Home button
- `End` key is the 3DS power button
- `Esc` will quit the program 

The image in the popup window asking for 3DS IP address can be changed by changing `/lib/luma.png`

The touchscreen image can similarly be changed by changing `/lib/bottom.png`

If multiple controllers are plugged in, the script will select the one you selected when controller_setup.py was run. If it isn't found  it will use the last controller in its list (list order is arbitrary) with default button mapping.

You can use the n3ds script with an o3DS (but ZL/ZR and c-stick won't work).
You can also use the o3DS script with n3DS (but c-stick isn't bound to anything)


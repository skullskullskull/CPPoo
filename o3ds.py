#!/usr/bin/env python3

from tpp.tppflush import *
import sys
from math import fabs
try:
	import pygame
except ImportError: 
	exit("Pygame required. Exiting.")

try:
	from lib.controller import *
except ImportError:
	joystick_name="??"
	j_axis=[ ]
	
#buttons.py adds the following:
#joystick_name="Microsoft X-Box 360 pad"
#buttons=['B', 'A', 'Y', 'X', 'L', 'R', 'SELECT', 'START', 'Home', 'Home', 'Home']
#j_axis=[0, 1, 3, 4]

done=False

circx,circy = 160,120
deadZone=0.3 #send '0' if fabs joystick(0,1) is less than this value eg joystick_x=0.1, sends joystick_x=0.0

#Default button mapping
buttonMappings = [
	HIDButtons.A,
	HIDButtons.B,
	HIDButtons.X,
	HIDButtons.Y,
	HIDButtons.SELECT, #Z
	HIDButtons.R,
	HIDButtons.L,
	HIDButtons.START,
	HIDButtons.DPADUP,
	HIDButtons.DPADDOWN,
	HIDButtons.DPADLEFT,
	HIDButtons.DPADRIGHT
	]

class KBDButtons(int):
	HOME = pygame.K_HOME
	POWER = pygame.K_END

#street fighter style layout on numberpad ([punches] y,x,L -> 4,5,6)
#might be useful for joy2key apps
KBbutt={
	257: HIDButtons.B, #numberpad 1
	258: HIDButtons.A,
	259: HIDButtons.R,

	260: HIDButtons.Y, #numberpad 4
	261: HIDButtons.X,
	262: HIDButtons.L,

	256: HIDButtons.START, #numberpad 0
	266: HIDButtons.SELECT, #numberpad .
	
	273: HIDButtons.DPADUP, #arrow key up
	274: HIDButtons.DPADDOWN,
	276: HIDButtons.DPADLEFT,
	275: HIDButtons.DPADRIGHT
	}

if len(sys.argv) < 2:
	#this is the pop up window
	import tkinter as tk 
	class App:
		def __init__(self, master):
			frame=tk.Frame(master)
			frame.pack()
			#reads file lastIP to get first line
			try:
				f=open("lastIP","r")
				last_ip=f.readline()
				f.close()
			except FileNotFoundError:
				last_ip=" "
			self.l_IP=tk.StringVar() 
			self.l_IP.set(last_ip)
			#image banner (row 0, col 0)
			lumaIMG = tk.PhotoImage(file="lib/luma.png")
			lumal = tk.Label(frame,image=lumaIMG)
			lumal.image = lumaIMG
			lumal.grid(row=0,columnspan=3)
			#places the 3 other elements (label, text box, button) on row 1
			tk.Label(frame, text='IP:',font=("Courier", 22)).grid(row=1, column=0, sticky=tk.E)
			tk.Entry(frame,bg='white', width=15, textvariable=self.l_IP, font=("Courier", 18)).grid(row=1,column=1, pady=10, sticky=tk.E+tk.W)
			button = tk.Button(frame, text='Go', font=("Courier", 18), command=self.store)
			button.grid(row=1, column=2, sticky=tk.W, pady=10)
			#center label and butt
			frame.grid_columnconfigure(0, weight=1)
			frame.grid_columnconfigure(2, weight=1)			
			master.bind('<Return>', self.store ) #"enter" key
			master.bind('<KP_Enter>', self.store ) # numeric "enter" key
						
		def store(self, *args):
			global IP
			IP=self.l_IP.get() 
			f=open("lastIP","w")
			f.write(IP.strip()) #stores data in text box (as string type)
			f.close()
			root.quit()


	root= tk.Tk()
	root.wm_title('3DS IP')
	App(root)
	root.bind('<Escape>', lambda x: quit())
	root.mainloop()
	root.destroy() #removes window
	server = IP.strip()
else:
	server = sys.argv[1]

server=LumaInputServer(server)

pygame.init()
screen = pygame.display.set_mode((320, 240))

pygame.display.set_caption('touchscreen')
botSr = pygame.image.load('lib/bottom.png')
screen.blit(botSr, (0,0))
if len(j_axis)>=6 :
	pygame.draw.circle(screen, (0,0,0), (circx, circy), 5, 2)
pygame.display.update()

pygame.joystick.init()

joystick_count = pygame.joystick.get_count()
print("Number of joysticks: {}".format(joystick_count) )

if (joystick_count>0):
	#Only loads one joystick if multiple are connected. 
	for i in range(joystick_count):
		joystick = pygame.joystick.Joystick(i)
		name = joystick.get_name()
		if name == joystick_name:
			break

	joystick.init()
	print("Using joystick \"{}\"".format(name))
	if name == joystick_name:
		buttonMappings=buttons
		print("\t--> loading \"{}\" layout".format(joystick_name))
	else :
		print("\t(using default button layout)")

	print("\t{} axes, {} buttons, {} hats".format(joystick.get_numaxes(),joystick.get_numbuttons(),joystick.get_numhats()))
	for i in range(joystick.get_numaxes()):
		j_axis.append(i)
else:
	print("No controller found!\n\t(restricted to limited keyboard button layout)")

print("\nHOME = HOME key \nPOWER = END key\nEnd Program = ESC key")
while done==False:
	#Event L O O P
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done=True
		#Touchscreen input
		if pygame.mouse.get_pressed()[0]:
			pos = pygame.mouse.get_pos()
			server.touch(pos[0], pos[1])
			#print("THSC: ",pos[0],",",pos[1])
			server.send()
		elif event.type == pygame.MOUSEBUTTONUP:
			server.clear_touch()
			server.send()
		
		#Keyboard Mappings
		elif event.type == pygame.KEYDOWN:
			if event.key == KBDButtons.HOME: #home
				server.special_press(Special_Buttons.HOME)
				#print("HOME")
			if event.key == KBDButtons.POWER: #power
				server.special_press(Special_Buttons.POWER)
				#print("POWER")
			if event.key == pygame.K_ESCAPE: #end program
				server.clear_everything()
				done = True
			if event.key in KBbutt:
				server.hid_press(KBbutt[event.key])
			#print(event.key)
			server.send()
				
		elif event.type == pygame.KEYUP:
			if event.key == KBDButtons.HOME: #home
				server.special_unpress(Special_Buttons.HOME)
			if event.key == KBDButtons.POWER: #power
				server.special_unpress(Special_Buttons.POWER)
			if event.key in KBbutt:
				server.hid_unpress(KBbutt[event.key])
			server.send()

		# Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
		if event.type == pygame.JOYBUTTONDOWN :
			#print("Joystick {} button {} pressed.".format(event.joy,event.button))
			server.press(buttonMappings[event.button])
			server.send()
		if event.type == pygame.JOYBUTTONUP:
			#print("Joystick {} button {} released.".format(event.joy,event.button))
			server.unpress(buttonMappings[event.button])
			server.send()
		if event.type == pygame.JOYHATMOTION:
			#print("Joystick {} HATS moved to {}.".format(event.joy, event.value))               
			(xhat, yhat) = event.value #[-1,0,1]
			if (xhat == 1): 
				server.press(HIDButtons.DPADRIGHT)
			elif (xhat == -1): 
				server.press(HIDButtons.DPADLEFT)
			elif (xhat == 0) :
				server.unpress(HIDButtons.DPADRIGHT)
				server.send()
				server.unpress(HIDButtons.DPADLEFT)
			if (yhat == 1): 
				server.press(HIDButtons.DPADUP)
			elif (yhat == -1): 
				server.press(HIDButtons.DPADDOWN)
			elif (yhat == 0) :
				server.unpress(HIDButtons.DPADDOWN)
				server.send()
				server.unpress(HIDButtons.DPADUP)                		
			server.send()
		if event.type == pygame.JOYAXISMOTION:
			#xbox:Left Thumbstick | axis 0 : L/R | axis 1 : U/D
			#xbox: axis 2 : L trigger (-1:1)
			#xbox: Right Thumbstick | axis 3 : L/R | axis 4 : U/D
			#xbox: axis 5 : R trigger (-1:1)
			#if event.axis == 0: print("Joystick {} axis {} moved to {}.".format(event.joy,event.axis, event.value))
			
			if event.axis == j_axis[0] : 
				if fabs(event.value)>deadZone:
					server.circle_pad_coords[0] = int(32767*event.value) #left_joy_x
				else:
					#note: circle_pad_neutral() == circle_pad_coords = [0,0] (that is both X and Y coords are set to zero)
					server.circle_pad_coords[0] = int(0) #left_joy_x
				server.send()
			if event.axis==j_axis[1] : 
				if fabs(event.value)>deadZone:
					server.circle_pad_coords[1] = int(-32767*event.value) #left_joy_y
				else:
					server.circle_pad_coords[1] = int(0) #left_joy_y
				server.send()

#using the right trigger to touch the screen only works if you have a right trigger and right thumbstick
			if len(j_axis)>=6:
				if (event.axis in [j_axis[2], j_axis[3],j_axis[5]]): #r trig = mouse click
					(circx, circy)=(160+int(159*joystick.get_axis(j_axis[2])),120+int(119*joystick.get_axis(j_axis[3])))
					#draw location of touch point but only when joystick moves
					screen.blit(botSr, (0,0))
					pygame.draw.circle(screen, (0,0,0), (circx, circy), 5, 2)
					pygame.display.update()
					if (joystick.get_axis(j_axis[5])>0.0): #Want to be able to "drag"
						server.touch(circx,circy)
						server.send()
						pygame.draw.circle(screen, (255,255,255), (circx, circy), 3, 0)
						pygame.display.update()
					if event.axis == j_axis[5]: #r trig
						if event.value < 0: #less than half depression #notme_irl
							server.clear_touch()
							server.send()

print("\nClearing everything and closing program")
server.clear_everything()
pygame.quit()

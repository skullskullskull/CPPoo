#!/usr/bin/env python3

import sys
from math import fabs
try:
	import pygame
except ImportError: 
	exit("Pygame required. Exiting.")

done=False

pygame.init()
pygame.joystick.init()
pygame.font.init()

joystick_count = pygame.joystick.get_count()
print("Number of joysticks: {}".format(joystick_count) )

if joystick_count is 0:
	exit("No joystick found to calibrate")

jnum=0
if joystick_count is not 1:
	for i in range(joystick_count):
		joystick = pygame.joystick.Joystick(i)
		name = joystick.get_name()
		print("{}) {}".format(i,name))

	print("\nWhich # joystick do you want to use and configure?")
	jnum = input(">").strip()

joystick = pygame.joystick.Joystick(int(jnum))
joystick.init()
print("Using joystick: \"{}\"".format(joystick.get_name()))

axes = joystick.get_numaxes()
buttons = joystick.get_numbuttons()
hats = joystick.get_numhats()
print("\t{} axes, {} buttons, {} hats".format(axes,buttons,hats))

i=0
button_s = []
for it in range (0,joystick.get_numbuttons()):
	button_s.append("Special_Buttons.HOME") #fill with "home" because the alternative is out of bounds errors

button_a = ["A", "B", "X", "Y", "L", "R", "START", "SELECT", "ZL","ZR"]

screen = pygame.display.set_mode((150, 25)) #window is needed for keyboard presses
myfont = pygame.font.SysFont("Helvetica", 20)
label = myfont.render("Controller setup", False, (255,255,255))
screen.blit(label, (0, 0))
pygame.display.update()

print("\nMapping the buttons. Press Esc to quit.")
print("press key for {} (press space to skip)".format(button_a[i]))
while i<len(button_a):
	#Event L O O P
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: # If user clicked close
			exit("EXITING: Not saving configuration.")
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE: #ESC 
				exit("EXITING: Not saving configuration.")
			if event.key == pygame.K_SPACE:
				print("\t{} button not set".format(button_a[i]))
				i+=1
				if (i<len(button_a)):
					print("press key for {} (press space to skip)".format(button_a[i]))
		elif event.type == pygame.JOYBUTTONDOWN:
			print("\t{}: button {} ".format(button_a[i],event.button))
			if button_a[i] in ["ZL", "ZR"]: 
				button_s[int(event.button)]="N3DS_Buttons."+button_a[i]
			else:
				button_s[int(event.button)]="HIDButtons."+button_a[i]
			i+=1
			if (i<len(button_a)):
				print("press key for {} (press space to skip)".format(button_a[i]))

	
print("\nMapping the analog inputs.")

i=0
j_axis=[ ]
j_axis_h=["Left thumbstick horizontal", "Left thumbstick vertical","Right thumbstick horizontal","Right thumbstick vertical","Left analog trigger", "Right analog trigger" ]
axes = joystick.get_numaxes()
print (j_axis_h[i])
while i< axes :
	for event in pygame.event.get(): 
		if event.type == pygame.JOYAXISMOTION and fabs(event.value) > 0.5 and event.axis not in j_axis :
			print("\t{}: axis {} ".format(j_axis_h[i],event.axis))
			j_axis.append(event.axis)
			i+=1
			if (i< axes):
				print("press {}".format(j_axis_h[i]))

f=open("lib/controller.py","w") # saving it as a python file so I don't have to parse it later
f.write("from lib.tppflush import *\n\n")
f.write("joystick_name=\"{}\"".format(joystick.get_name()))
f.write("\nbuttons = [ ")
f.write(", ".join(map(str, button_s))+" ]")
#it turns out this was not a good idea.
f.write("\nj_axis="+str(j_axis))
f.close()

print("\nController config saved")

pygame.quit()

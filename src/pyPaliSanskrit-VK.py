#!/usr/bin/python
#Copyright 2018 Raryel C. Souza

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.


#pyPaliSanskritVK
#Virtual keyboard for input of Pāli/Sanskrit Diacritics

#Based on the project py-virtual-keyboard (https://github.com/surajsinghbisht054/py-VirtualKeyBoard), 
#developed by S.S.B Group (surajsinghbisht054@gmail.com / http://bitforestinfo.blogspot.com/) written in python using Tkinter And pyautogui

#Modifications for Pāli/Sanskrit Diacritics by Raryel C. Souza

# ========== Configurations ====================
BUTTON_BACKGROUND 		= "black"
MAIN_FRAME_BACKGROUND 	= "cornflowerblue"
BUTTON_LOOK 			= "groove" #flat, groove, raised, ridge, solid, or sunken
TOP_BAR_TITLE 			= "pyPaliSanskrit-VK"
TRANSPARENCY 			= 0.7
FONT_COLOR 				= "white"

# ==============================================

# import modules
try:
    import Tkinter
except:
    import tkinter as Tkinter

import pyautogui
import pyperclip
import time
import platform

keys =[ 
[
# =========================================
# ===== Keyboard Configurations ===========
# =========================================

	
	[
		("Character_Keys"),
		({'side':'top','expand':'yes','fill':'both'}),
		[
			('Ā','Ḍ','Ī','Ḷ','Ṃ','Ṁ','Ṅ','Ṇ','Ñ','Ṭ','Ū'),
			('ā','ḍ','ī','ḷ','ṃ','ṁ','ṅ','ṇ','ñ','ṭ','ū'),
			('Ḥ','Ḹ','Ṛ','Ṝ','Ṣ','Ś'),
			('ḥ','ḹ','ṛ','ṝ','ṣ','ś'),
		]
	]
],
]

# Create key event
def create_keyboard_event(numlock, capslock, controler, key):
	return

##  Frame Class
class Keyboard(Tkinter.Frame):
	def __init__(self, *args, **kwargs):
		Tkinter.Frame.__init__(self, *args, **kwargs)
		

		# Function For Creating Buttons
		self.create_frames_and_buttons()



	# Function For Extracting Data From KeyBoard Table
	# and then provide us a well looking
	# keyboard gui
	def create_frames_and_buttons(self):
		# take section one by one
		for key_section in keys:
			# create Sperate Frame For Every Section
			store_section = Tkinter.Frame(self)
			store_section.pack(side='left',expand='yes',fill='both',padx=10,pady=10,ipadx=10,ipady=10)
			
			for layer_name, layer_properties, layer_keys in key_section:
				store_layer = Tkinter.LabelFrame(store_section)#, text=layer_name)
				#store_layer.pack(side='top',expand='yes',fill='both')
				store_layer.pack(layer_properties)
				for key_bunch in layer_keys:
					store_key_frame = Tkinter.Frame(store_layer)
					store_key_frame.pack(side='top',expand='yes',fill='both')
					for k in key_bunch:
						
						if len(k)<=3:
							store_button = Tkinter.Button(store_key_frame, text=k, width=2, height=2, font=('Arial', 12))
						else:
							store_button = Tkinter.Button(store_key_frame, text=k.center(5,' '), height=2)
						if " " in k:
							store_button['state']='disable'
						
						store_button['relief']=BUTTON_LOOK
						store_button['bg']=BUTTON_BACKGROUND
						store_button['fg']=FONT_COLOR

						store_button['command']=lambda q=k: self.button_command(q)
						store_button.pack(side='left',fill='both',expand='yes')
		return

		# Function For Detecting Pressed Keyword.
	def button_command(self, event):
                #for unicode characters it is easier to use this workaround than to send to pyautogui.press()
                pyperclip.copy(event)

                #on windows is necessary to change the focus to the app that will receive the text input before pasting it
                if platform.system() == "Windows":
                    pyautogui.hotkey("alt", "tab")
                    #after switching the focus with alt tab give a small interval for the focus update
                    time.sleep(0.1)
                    #paste the text on the focused app
                    pyautogui.hotkey("ctrl", "v")
                    #bring the focus back to the virtual keyboard
                    pyautogui.hotkey("alt", "tab")
                #on linux and macos the focus change is not necessary. Can paste the text straight away
                else:
                    pyautogui.hotkey("ctrl", "v")                
                return

# Creating Main Window
def main():
	root = Tkinter.Tk(className=TOP_BAR_TITLE)
	k=Keyboard(root, bg=MAIN_FRAME_BACKGROUND)
	root.wait_visibility(root)

        #block maximize/minimize button
	root.resizable(0,0)

	#floating window always on top
	root.wm_attributes("-topmost", 1)
	root.wm_attributes('-alpha',TRANSPARENCY)
	
	k.pack(side='top')

        #screen dimensions
	screenWidth = root.winfo_screenwidth()
	screenHeight = root.winfo_screenheight()

        #window dimensions
	windowWidth = k.winfo_reqwidth()
	windowHeight = k.winfo_reqheight()
	
	#position the virtual keyboard on the bottom right corner of the screen
	x = (screenWidth-windowWidth)
	y = (screenHeight-windowHeight-90)
	root.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, x, y))
	
	root.mainloop()
	return

# Function Trigger
if __name__=='__main__':
	main()


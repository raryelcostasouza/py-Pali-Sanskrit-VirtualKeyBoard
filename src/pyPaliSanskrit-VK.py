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
TOPBAR_BACKGROUND 		= "skyblue"

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
import threading

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
        
        #semaphore variable used to prevent multiple key pressing
        self.lock = False


    # Function For Extracting Data From KeyBoard Table
    # and then provide us a well looking
    # keyboard gui
    def create_frames_and_buttons(self):
        # take section one by one
        for key_section in keys:
            # create Sperate Frame For Every Section
            store_section = Tkinter.Frame(self)
            store_section.pack(side='left',expand='yes',fill='both',padx=0,pady=0,ipadx=0,ipady=0)
            
            for layer_name, layer_properties, layer_keys in key_section:
                store_layer = Tkinter.LabelFrame(store_section)#, text=layer_name)
                #store_layer.pack(side='top',expand='yes',fill='both')
                store_layer.pack(layer_properties)
                for key_bunch in layer_keys:
                    store_key_frame = Tkinter.Frame(store_layer)
                    store_key_frame.pack(side='top',expand='yes',fill='both')
                    for k in key_bunch:
                        store_button = Tkinter.Button(store_key_frame, text=k, width=2, height=2, font=('Arial', 16))
                        
                        store_button['relief']=BUTTON_LOOK
                        store_button['bg']=BUTTON_BACKGROUND
                        
                        #for MacOS as the buttons have clear blackground need to use a black font
                        if platform.system() == "Darwin":
                            FONT_COLOR = "black"
                        else:
                            FONT_COLOR = "white"
                            
                        store_button['fg'] = FONT_COLOR

                        store_button['command']=lambda q=k: self.actionClickButton(q)
                        store_button.pack(side='left',fill='both',expand='yes')
        return

    # Listener function for clicked button
    def actionClickButton(self, event):
        
        #thread for typing the clicked button on the focused app
        
        #MacOS version
        def actionMac():
            #Lock the semaphore variable for preventing multiple keys pressing
            self.lock = True 
            pyperclip.copy(event)

            #switch focus to the other app that will receive the key input
            pyautogui.hotkey("command", "tab")
            
            #paste the text on the focused app
            pyautogui.hotkey("command", "v")
            
            #Release the semaphore variable
            self.lock = False
        
        #Windows version
        def actionWindows():
            #Lock the semaphore variable for preventing multiple keys pressing
            self.lock = True 
            pyperclip.copy(event)
            
            #switch focus to the other app that will receive the key input
            pyautogui.hotkey("alt", "tab")
            
            #after switching the focus with alt tab give a small interval for the focus update
            time.sleep(0.1)
            
            #paste the sanskrit/pali letter on the focused app
            pyautogui.hotkey("ctrl", "v")
            
            #Release the semaphore variable
            self.lock = False
            
        
        if platform.system() == "Linux":
            #on Linux the focus change is not necessary. Can paste the text straight away
            pyperclip.copy(event)
            pyautogui.hotkey("ctrl", "v")
        else:
            
            #for MacOS and Windows it is necessary to switch the focus manually to the other app before pasting the text
            #so use a separate thread to handle the task to avoid gui freezing
            
            #if the semaphore variable is not locked
            if not self.lock:
                #open a separate thread to execute the sequence of commands without freezing the GUI
                if platform.system() == "Windows":
                    t = threading.Thread(target=actionWindows)
                else:
                    t = threading.Thread(target=actionMac)
                t.start()
        return

#listener for moving the window on Linux
class top_moving_mechanism:
	def __init__(self, root, label):
		self.root = root
		self.label = label

	def motion_activate(self, kwargs):
		w,h = (self.root.winfo_reqwidth(), self.root.winfo_reqheight())
		(x,y) = (kwargs.x_root, kwargs.y_root)
		self.root.geometry("%dx%d+%d+%d" % (w,h,x,y))
		return


# Creating Main Window
def main():
    root = Tkinter.Tk(className=TOP_BAR_TITLE)
    k=Keyboard(root, bg=MAIN_FRAME_BACKGROUND)
    k.pack(side='bottom')
    #block maximize/minimize button
    root.resizable(0,0)

    #floating window always on top
    
    root.wm_attributes("-topmost", 1)
    if platform.system() == "Windows":
        #adjustments to put the window on the bottom right corner without covering the task bar
        yAdjust = 90
        xAdjust = 10
    #for Mac OS
    elif platform.system() == "Darwin":
        yAdjust = 110
        xAdjust = 10
    else:
        #on Linux the overrideredirect option need to be on to send the output to other app without having to change focus manually
        #so the default system window decorations will be suppressed
        root.overrideredirect(True)
        
        #create the window top decoration and the close button
        f = Tkinter.Frame(root)
        t_bar=Tkinter.Label(f, text=TOP_BAR_TITLE, bg=TOPBAR_BACKGROUND)
        t_bar.pack(side='left',expand="yes", fill="both")
        Tkinter.Button(f, text="[X]", command= root.destroy).pack(side='right')
        
        #listener for moving the window
        mechanism = top_moving_mechanism(root, t_bar)
        t_bar.bind("<B1-Motion>", mechanism.motion_activate)
        
        f.pack(side='top', expand='yes',fill='both')
        
        #adjustments to put the window on the bottom right corner without covering the task bar
        yAdjust = 50
        xAdjust = 0
    
    
    root.wait_visibility(root)
    #screen dimensions
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()

    #window dimensions
    windowWidth = k.winfo_reqwidth()
    windowHeight = k.winfo_reqheight()
    
    #on Linux the title bar dimensions need to be added to the window height calculation
    if platform.system() == "Linux":
        windowHeight += f.winfo_reqheight()
    
    #position the virtual keyboard on the bottom right corner of the screen
    x = (screenWidth-windowWidth-xAdjust)
    y = (screenHeight-windowHeight-yAdjust)
    root.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, x, y))
    
    root.mainloop()
    return

# Function Trigger
if __name__=='__main__':
    main()


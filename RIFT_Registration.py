#Base Libraries
from logging import PlaceHolder
import pandas as pd
import os
from openpyxl import *
from datetime import datetime
import time

#Graphic Libraries
import tkinter.messagebox
import tkinter
import customtkinter
import threading

#Image Libraries

#SIZE
COMPLETE_WIDTH = 700
COMPLETE_HEIGHT = 800

#Working Directories
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
FILE_NAME=".\dump\\test.xlsx"
FILE_PATH = os.path.join(CURRENT_DIRECTORY,FILE_NAME)

#Base Settings
customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class Registration(customtkinter.CTk):

    APP_WIDTH = COMPLETE_WIDTH
    APP_HEIGHT = COMPLETE_HEIGHT

    def __init__(self):
        super().__init__()
        WIDTH = self.winfo_screenwidth()
        HEIGHT = self.winfo_screenwidth()

        app_center_coordinate_x = (WIDTH/2) - (Registration.APP_WIDTH )
        app_center_coordinate_y = (HEIGHT/2) - (Registration.APP_HEIGHT)

        self.title("Plataforma RIFT")
        self.geometry(f"{Registration.APP_WIDTH}x{Registration.APP_HEIGHT}+{int(app_center_coordinate_x)}+{int(app_center_coordinate_y)}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        self.configure(fg_color=("#189FE7"))

        #GUI TITLE
        self.homeLabel = customtkinter.CTkLabel(master=self,
                                                    corner_radius=7,
                                                    height=40,
                                                    fg_color=("white", "grey38"),  # <- custom tuple-color
                                                    text_font=("Arial",14),
                                                    text="Hookup Registration")
        self.homeLabel.grid(row=0,column=0,columnspan=2,padx=15,pady=10)

        #BASE FRAME
        self.frame_home = customtkinter.CTkFrame(master=self,
                                                    width= Registration.APP_WIDTH,
                                                    height= Registration.APP_HEIGHT,
                                                    fg_color="black",
                                                    corner_radius=10)
        self.frame_home.grid(row=1,column=0,padx=15, pady=20,sticky="nsew")


        #BOAT NAME
        self.boat_name = customtkinter.CTkLabel(master=self.frame_home,
                                                    corner_radius=7,
                                                    text="Enter Boat ID: ")
        self.boat_name.grid(row=0,column=0,padx=10,pady=20)

        #BOAT INPUT
        self.boat_input= customtkinter.CTkEntry(master=self.frame_home,
                                            width=Registration.APP_WIDTH/2+50,
                                            placeholder_text="Boat ID")
        self.boat_input.grid(row=0,column=1, columnspan=2, pady=20, padx=20, sticky="we")

        #SEARCH BUTTON
        self.search_button= customtkinter.CTkButton(master=self.frame_home,
                                            width=Registration.APP_WIDTH/2-50,
                                            text="Search",
                                            command=self.search)
        self.search_button.grid(row=1,column=0,columnspan=3,pady=20, padx=20, sticky="we")

        #SEARCH FRAME
        self.search_frame = customtkinter.CTkFrame(master=self.frame_home,
                                                    width= Registration.APP_WIDTH,
                                                    height= Registration.APP_HEIGHT,
                                                    fg_color="white",
                                                    corner_radius=10)
        self.search_frame.grid(row=2,column=0,columnspan=4,padx=15, pady=20,sticky="nsew")

        #BOAT NAME
        self.search_boat_name = customtkinter.CTkEntry(master=self.search_frame,
                                                    corner_radius=7,
                                                    width= Registration.APP_WIDTH/2-50,
                                                    placeholder_text="Boat Name",
                                                    text="Boat")
        self.search_boat_name.grid(row=0,column=0,columnspan=2,padx=10,pady=20)
        self.search_boat_name.configure(state=tkinter.DISABLED)

        #CAPTAIN NAME
        self.search_captain_name = customtkinter.CTkEntry(master=self.search_frame,
                                                    corner_radius=7,
                                                    width= Registration.APP_WIDTH/2-50,
                                                    placeholder_text="Captain Name",
                                                    text="Captain")
        self.search_captain_name.grid(row=0,column=3,columnspan=2,padx=10,pady=20)
        self.search_captain_name.configure(state=tkinter.DISABLED)

        #CATEGORY SELECT LABEL
        self.category_combobox_label = customtkinter.CTkLabel(master=self.frame_home,
                                                    corner_radius=7,
                                                    text="Select Category: ")
        self.category_combobox_label.grid(row=3,column=0,columnspan=1,padx=15, pady=20,sticky="nsew")

        #CATEGORY SELECT
        self.category_combobox = customtkinter.CTkOptionMenu(master=self.frame_home,
                                                    values=["Billfish", "Rodeo", "Junior","Kids", "Women", "None"])
        self.category_combobox.grid(row=3,column=1,columnspan=2,padx=15, pady=20,sticky="nsew")
        self.category_combobox.set("None")


        #FISH SELECT LABEL
        self.fish_combobox_label = customtkinter.CTkLabel(master=self.frame_home,
                                                    corner_radius=7,
                                                    text="Select Fish: ")
        self.fish_combobox_label.grid(row=4,column=0,columnspan=1,padx=15, pady=20,sticky="nsew")

        #FISH SELECT
        self.fish_combobox = customtkinter.CTkOptionMenu(master=self.frame_home,
                                                    values=["Fish", "None"])
        self.fish_combobox.grid(row=4,column=1,columnspan=2,padx=15, pady=20,sticky="nsew")
        self.fish_combobox.set("None")

        #HOOKUP TIME LABEL
        self.hookup_time_label = customtkinter.CTkLabel(master=self.frame_home,
                                                    corner_radius=7,
                                                    text="Hookup Time: ")
        self.hookup_time_label.grid(row=5,column=0,columnspan=1,padx=15, pady=20,sticky="nsew")

        #HOOKUP TIME
        self.hookupTime = customtkinter.CTkLabel(master=self.frame_home,
                                                    corner_radius=7,
                                                    text=datetime.now().strftime("%H:%M:%S"),
                                                    width= Registration.APP_WIDTH/2-50)
        self.hookupTime.grid(row=5,column=1,columnspan=1,padx=15, pady=20,sticky="nsew")

        #REGISTER HOOKUP
        self.hookup_button = customtkinter.CTkButton(master=self.frame_home,
                                            width=Registration.APP_WIDTH/2-50,
                                            text="Register Hookup",
                                            command=self.register_hookup)
        self.hookup_button.grid(row=6,column=0,columnspan=3,padx=15, pady=20,sticky="nsew")

        #RELEASE TIME LABEL
        self.release_time_label = customtkinter.CTkLabel(master=self.frame_home,
                                                    corner_radius=7,
                                                    text="Release Time: ")
        self.release_time_label.grid(row=7,column=0,columnspan=1,padx=15, pady=20,sticky="nsew")

        #RELEASE TIME
        self.release_time = customtkinter.CTkLabel(master=self.frame_home,
                                                    corner_radius=7,
                                                    text=datetime.now().strftime("%H:%M:%S"),
                                                    width= Registration.APP_WIDTH/2-50)
        self.release_time.grid(row=7,column=1,columnspan=1,padx=15, pady=20,sticky="nsew")

        #CLEAN RELEASE CHECK
        self.clean_release=customtkinter.CTkCheckBox(master=self.frame_home,
                                                    text="Clean Release")
        self.clean_release.grid(row=7,column=2,columnspan=1,padx=15, pady=20,sticky="nsew")

        #DISCARD BUTTON
        self.discard_button = customtkinter.CTkButton(master=self.frame_home,
                                            text="Discard",
                                            command=self.discard)
        self.discard_button.grid(row=8,column=0,columnspan=1,padx=15, pady=20,sticky="nsew")

        #CHECK XLSX BUTTON
        self.discard_button = customtkinter.CTkButton(master=self.frame_home,
                                            text="View Worksheet",
                                            command=self.view)
        self.discard_button.grid(row=8,column=1,columnspan=1,padx=15, pady=20,sticky="nsew")

        #REGISTER RELEASE
        self.release_button = customtkinter.CTkButton(master=self.frame_home,
                                            text="Register Release",
                                            command=self.register_release)
        self.release_button.grid(row=8,column=2,columnspan=1,padx=15, pady=20,sticky="nsew")

    #Register hookup
    def register_hookup(self):
        return True
    #Register release
    def register_release(self):
        return True
    #View XLSX file
    def view(self):
        return True
    #Discard all changes
    def discard(self):
        return True
    #Search ID
    def search(self):
        return True
    #Update HookupTime
    def updateClock(self):
        time.sleep(1)
        while True:
            self.hookupTime.configure(placeholder_text=datetime.now().strftime("%H:%M:%S"))
            time.sleep(1)
    #Close Program
    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = Registration()
    t1 = threading.Thread(target=app.mainloop())
    t2 = threading.Thread(target=app.updateClock())

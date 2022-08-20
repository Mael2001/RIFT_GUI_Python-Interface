#Base Libraries
from email.mime import image
import os
import webbrowser
import logging
import threading
import time

#Subsystems
import RIFT_Inscription
import RIFT_Registration

#Graphic Libraries
import tkinter
import customtkinter

#Image Libraries
from PIL import Image, ImageTk

#SIZE
COMPLETE_WIDTH = 600
COMPLETE_HEIGHT = 800

#Working Directories
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

#Base Configuration
customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green



class App(customtkinter.CTk):

    APP_WIDTH = COMPLETE_WIDTH
    APP_HEIGHT = COMPLETE_HEIGHT

    def __init__(self):
        super().__init__()
        #Base Configuration
        self.title("Plataforma RIFT")
        self.geometry(f"{App.APP_WIDTH}x{App.APP_HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        image = Image.open("./images/HomeImage.jpeg").resize((self.APP_WIDTH, self.APP_HEIGHT))
        self.bg_image = ImageTk.PhotoImage(image)

        self.image_label = tkinter.Label(master=self, image=self.bg_image)
        self.image_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


        #RIFT INSCRIPTION
        rift_inscription = customtkinter.CTkButton(master=self,
                                                    text="Inscriptions",
                                                    height=80,
                                                    width=230,
                                                    corner_radius=5,
                                                    fg_color="white",
                                                    text_color="black",
                                                    text_font=("Adobe Ming Std L",25),
                                                    command=self.open_inscriptions)
        rift_inscription.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)

        #RIFT REGISTRATION
        rift_registration = customtkinter.CTkButton(master=self,
                                                    text="Registrations",
                                                    height=80,
                                                    width=230,
                                                    corner_radius=5,
                                                    fg_color="white",
                                                    text_color="black",
                                                    text_font=("Adobe Ming Std L",25),
                                                    command=self.open_registration)
        rift_registration.place(relx=0.7, rely=0.7, anchor=tkinter.CENTER)

        #RIFT PAGE
        rift_website = customtkinter.CTkButton(master=self,
                                                    text="Website",
                                                    height=80,
                                                    width=230,
                                                    corner_radius=5,
                                                    fg_color="white",
                                                    text_color="black",
                                                    text_font=("Adobe Ming Std L",25),
                                                    command=self.open_website)
        rift_website.place(relx=0.3, rely=0.81, anchor=tkinter.CENTER)

        #RIFT LeaderBoard
        rift_leaderBoard = customtkinter.CTkButton(master=self,
                                                    text="Leaderboard",
                                                    height=80,
                                                    width=230,
                                                    corner_radius=5,
                                                    fg_color="white",
                                                    text_color="black",
                                                    text_font=("Adobe Ming Std L",25),
                                                    command=self.open_leaderboard)
        rift_leaderBoard.place(relx=0.7, rely=0.81, anchor=tkinter.CENTER)

    #Open ./RIFG_Inscription
    def open_inscriptions(self):
        logging.info("Opening Inscriptions")
        inscriptions = RIFT_Inscription.Inscription(self)
        inscriptions.resizable(False,False)
    #Open ./RIFG_Registration
    def open_registration(self):
        logging.info("Opening Registration")
        registration = RIFT_Registration.Registration(self)
        registration.resizable(False,False)
    #Open Competition Website
    def open_website(self):
        logging.info("Opening Website")
        webbrowser.open('https://letsfishroatan.com/')
    #Open Leaderboards Page'
    def open_leaderboard(self):
        logging.info("Opening Leaderboards")
        webbrowser.open('https://www.letsfishroatan.com/#TOURNAMENT')
    #Close Program
    def on_closing(self, event=0):
        self.destroy()
        x.stop()


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Initializing Application")
    app = App()
    app.resizable(False,False)
    app.mainloop()
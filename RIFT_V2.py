#Base Libraries
from email.mime import image
import os
import webbrowser

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
COMPLETE_HEIGHT = 400

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
        WIDTH = self.winfo_screenwidth()
        HEIGHT = self.winfo_screenwidth()

        app_center_coordinate_x = (WIDTH/2) - (App.APP_WIDTH )
        app_center_coordinate_y = (HEIGHT/2) - (App.APP_HEIGHT * 2)
        #Base Configuration
        self.title("Plataforma RIFT")
        self.geometry(f"{App.APP_WIDTH}x{App.APP_HEIGHT}+{int(app_center_coordinate_x)}+{int(app_center_coordinate_y)}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        self.configure(fg_color=("#189FE7"))
        #Titulo
        #bckImage = Image.open(os.path.join(CURRENT_DIRECTORY,"/images/bg.png"))
        bckImage = Image.open(".\images\\bg.png")
        bckImage_resized = bckImage.resize((WIDTH,HEIGHT))
        bckImage = ImageTk.PhotoImage(bckImage_resized)


        #GUI BACKGROUND
        homeBckImage = customtkinter.CTkLabel(master=self,
                                                    corner_radius=7,
                                                    image=bckImage)
        homeBckImage.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        #GUI TITLE
        homeLabel = customtkinter.CTkLabel(master=self,
                                                    corner_radius=7,
                                                    height=80,
                                                    fg_color=("white", "grey38"),  # <- custom tuple-color
                                                    text_font=("Arial",14),
                                                    text="RIFT PLATFORM\n" +
                                                        "Homepage")
        homeLabel.grid(row=0,column=0,columnspan=2,padx=15,pady=10)

        #BASE FRAME
        frame_home = customtkinter.CTkFrame(master=self,
                                                    width= App.APP_WIDTH,
                                                    height= App.APP_HEIGHT,
                                                    fg_color=None,
                                                    corner_radius=10)
        frame_home.grid(row=1,column=0,padx=15, pady=20,sticky="nsew")

        #RIFT INSCRIPTION
        rift_inscription = customtkinter.CTkButton(master=frame_home,
                                                    text="Inscriptions",
                                                    width=App.APP_WIDTH-50,
                                                    text_color="white",
                                                    command=self.open_inscriptions)
        rift_inscription.grid(row=0,column=0,padx=10,pady=20)

        #RIFT REGISTRATION
        rift_registration = customtkinter.CTkButton(master=frame_home,
                                                    text="Registrations",
                                                    width=App.APP_WIDTH-50,
                                                    text_color="white",
                                                    command=self.open_registration)
        rift_registration.grid(row=1,column=0,padx=10,pady=20)

        #RIFT PAGE
        rift_website = customtkinter.CTkButton(master=frame_home,
                                                    text="Website",
                                                    width=App.APP_WIDTH-50,
                                                    text_color="white",
                                                    command=self.open_website)
        rift_website.grid(row=2,column=0,padx=10,pady=20)

        #RIFT LeaderBoard
        rift_leaderBoard = customtkinter.CTkButton(master=frame_home,
                                                    text="Leaderboard",
                                                    width=App.APP_WIDTH-50,
                                                    text_color="white",
                                                    command=self.open_leaderboard)
        rift_leaderBoard.grid(row=3,column=0,padx=10,pady=20)

    #Open ./RIFG_Inscription
    def open_inscriptions(self):
        inscriptions = RIFT_Inscription.Inscription()
        inscriptions.mainloop()
    #Open ./RIFG_Registration
    def open_registration(self):
        registration = RIFT_Registration.Registration()
        registration.mainloop()
    #Open Competition Website
    def open_website(self):
        webbrowser.open('https://letsfishroatan.com/')
    #Open Leaderboards Page
    def open_leaderboard(self):
        webbrowser.open('https://letsfishroatan.com/')
    #Close Program
    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
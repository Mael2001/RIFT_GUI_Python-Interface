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
COMPLETE_HEIGHT = 500

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
        image_size = 140
        logo = ImageTk.PhotoImage(Image.open("./images/NoBckLogo.png").resize((image_size, image_size)))
        image = Image.open("./images/bg_gradient.jpg").resize((self.APP_WIDTH, self.APP_HEIGHT))
        self.bg_image = ImageTk.PhotoImage(image)

        self.image_label = tkinter.Label(master=self, image=self.bg_image)
        #self.image_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        #TITLE FRAME
        title_Frame = customtkinter.CTkFrame(master=self,
                                                    corner_radius=0,
                                                    bg_color=None,
                                                    fg_color="#189FE7")
        title_Frame.grid(row=0,column=0,padx=15, pady=0,sticky="nsew")
        #LEFT LOGO
        button_1 = customtkinter.CTkButton(master=title_Frame, image=logo, text="", fg_color=None, width=50, height=50,corner_radius=10)
        button_1.grid(row=0, column=0, columnspan=1, padx=15, pady=10)
        button_1.configure(state=tkinter.DISABLED)
        #GUI TITLE
        homeLabel = customtkinter.CTkLabel(master=title_Frame,
                                                    corner_radius=7,
                                                    height=80,
                                                    width=100,
                                                    bg_color=None,
                                                    fg_color=("white", "grey38"),  # <- custom tuple-color
                                                    text_font=("Arial",14),
                                                    text="RIFT PLATFORM\n" +
                                                        "Homepage")
        homeLabel.grid(row=0,column=1,columnspan=3,padx=25,pady=10)
        #RIGHT LOGO
        button_2 = customtkinter.CTkButton(master=title_Frame, image=logo, text="", fg_color=None, width=50, height=50,corner_radius=10)
        button_2.grid(row=0, column=4, columnspan=1, padx=20, pady=10)
        button_2.configure(state=tkinter.DISABLED)

        #BASE FRAME
        frame_home = customtkinter.CTkFrame(master=self,
                                                    width= App.APP_WIDTH,
                                                    height= App.APP_HEIGHT,
                                                    bg_color=None,
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
    #Open Leaderboards Page'
    def open_leaderboard(self):
        webbrowser.open('https://www.letsfishroatan.com/#TOURNAMENT')
    #Close Program
    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
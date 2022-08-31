#Base Libraries
import threading
from cgitb import grey
import time
import cv2
import os
from stat import S_IREAD, S_IWRITE

#Graphic Libraries
import tkinter.messagebox
import tkinter
import customtkinter
import easygui
from tkinter import Tk
from tkinter.filedialog import askopenfilename

#Image Libraries
from PIL import Image, ImageTk

#SIZE
COMPLETE_WIDTH = 600
COMPLETE_HEIGHT = 800

#Weights Paths
IMAGE_WEIGHT_PATH = ''
VIDEO_WEIGHT_PATH = ''

#Cfg Paths
VIDEO_DETECTOR_CFG_PATH = './dump/configs/video/yolo-obj.cfg'
IMAGE_DETECTOR_CFG_PATH = './dump/configs/image/yolo-obj.cfg'

#Classes Names
IMAGE_CLASSES= './dump/configs/image/fishes.names'
VIDEO_CLASSES= './dump/configs/video/fishing.names'

class Detector(customtkinter.CTkToplevel):

    APP_WIDTH = COMPLETE_WIDTH
    APP_HEIGHT = COMPLETE_HEIGHT
    print(IMAGE_WEIGHT_PATH)

    def __init__(self,parent):
        super().__init__(parent)
        WIDTH = self.winfo_screenwidth()
        HEIGHT = self.winfo_screenwidth()

        app_center_coordinate_x = (WIDTH/2) - (Detector.APP_WIDTH )
        app_center_coordinate_y = (HEIGHT/2) - (Detector.APP_HEIGHT)

        self.set_default_image_weight()
        self.set_default_video_weight()

        self.title("RIFT Image and Video Detector")
        self.geometry(f"{Detector.APP_WIDTH}x{Detector.APP_HEIGHT}+{int(app_center_coordinate_x)}+{int(app_center_coordinate_y)}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        self.configure(fg_color=("#189FE7"))
        image = Image.open("./images/HomeImage.jpeg").resize((self.APP_WIDTH, self.APP_HEIGHT))
        self.bg_image = ImageTk.PhotoImage(image)

        self.image_label = tkinter.Label(master=self, image=self.bg_image)
        self.image_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        #GUI TITLE
        self.homeLabel = customtkinter.CTkLabel(master=self,
                                                    corner_radius=7,
                                                    height=40,
                                                    fg_color=("white", "grey38"),  # <- custom tuple-color
                                                    text_font=("Arial",14),
                                                    text="Image and Video Detector")
        #self.homeLabel.place(relx=0.5, rely=0.02, anchor=tkinter.CENTER)

        #Image Detector
        image_detector = customtkinter.CTkButton(master=self,
                                                    text="Image Detector",
                                                    height=80,
                                                    width=230,
                                                    corner_radius=5,
                                                    fg_color="white",
                                                    text_color="black",
                                                    text_font=("Adobe Ming Std L",25),
                                                    command=self.open_image_detector)
        image_detector.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)

        #Load Image Weight
        image_weight = customtkinter.CTkButton(master=self,
                                                    text="Image Weight",
                                                    height=80,
                                                    width=230,
                                                    corner_radius=5,
                                                    fg_color="white",
                                                    text_color="black",
                                                    text_font=("Adobe Ming Std L",25),
                                                    command=self.define_image_weight)
        image_weight.place(relx=0.7, rely=0.7, anchor=tkinter.CENTER)


        #Video Detector
        video_detector = customtkinter.CTkButton(master=self,
                                                    text="Video Detector",
                                                    height=80,
                                                    width=230,
                                                    corner_radius=5,
                                                    fg_color="white",
                                                    text_color="black",
                                                    text_font=("Adobe Ming Std L",25),
                                                    command=self.open_video_detector)
        video_detector.place(relx=0.3, rely=0.81, anchor=tkinter.CENTER)


        #Load Video Weight
        video_weight = customtkinter.CTkButton(master=self,
                                                    text="Video Weight",
                                                    height=80,
                                                    width=230,
                                                    corner_radius=5,
                                                    fg_color="white",
                                                    text_color="black",
                                                    text_font=("Adobe Ming Std L",25),
                                                    command=self.define_video_weight)
        video_weight.place(relx=0.7, rely=0.81, anchor=tkinter.CENTER)


    #Image Detector
    def open_image_detector(self):
        Tk().withdraw()
        file_path = askopenfilename()
        if (not file_path.lower().endswith(('.jpg', '.jpeg'))):
            self.trigger_error("Invalid file was selected", "Invalid File")
            return
        img = cv2.imread(file_path)

        limit_sup_height = 750
        limit_sup_width = 1000

        limit_inf_height = 400
        limit_inf_width = 600

        if img.shape[1] > limit_sup_width or img.shape[0] > limit_sup_height:
            width = limit_sup_width
            height = limit_sup_height
            dim = (width, height)
        elif img.shape[1] > 900 and img.shape[0] > 700:
            width = limit_sup_width
            height = limit_sup_height
            dim = (width, height)
        elif img.shape[1] < limit_inf_width or img.shape[0] < limit_inf_height:
            width = limit_inf_width
            height = limit_inf_height
            dim = (width, height)
        else:
            width = img.shape[1]
            height = img.shape[0]
            dim = (width, height)

        # resize image
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        with open(IMAGE_CLASSES, "r") as f:
            classes = f.read().splitlines()
        model = self.create_detection_model(IMAGE_WEIGHT_PATH, IMAGE_DETECTOR_CFG_PATH)

        classIds, scores, boxes = model.detect(
            resized, confThreshold=0.10, nmsThreshold=0.4
        )
        data_mod1 = classIds, classes
        confidence = str(scores)
        detects = str(self.count_objects(data_mod1))
        print(f'Detections:{detects}\tImage: {file_path}\tConfidence: {confidence}')
        for (classId, score, box) in zip(classIds, scores, boxes):
            cv2.rectangle(
                resized,
                (box[0], box[1]),
                (box[0] + box[2], box[1] + box[3]),
                color=(0, 0, 255),
                thickness=2,
            )

            text = "%s: %.4f" % (classes[classId], score)
            cv2.putText(
                resized,
                text,
                (box[0]+5, box[1] + 25),
                cv2.FONT_HERSHEY_DUPLEX,
                1,
                color=(0, 0, 255),
                thickness=2,
            )
            cv2.imshow("Image Prediction", resized)

    #Set Default Image Weight
    def set_default_image_weight(self):
        global IMAGE_WEIGHT_PATH
        if(IMAGE_WEIGHT_PATH == ''):
            for filename in os.listdir("./dump/weights/image"):
                if (filename.lower().endswith(('.weights'))):
                    IMAGE_WEIGHT_PATH = os.path.abspath(f'./dump/weights/image/{filename}')

    #Set Default Image Weight
    def set_default_video_weight(self):
        global VIDEO_WEIGHT_PATH
        if(VIDEO_WEIGHT_PATH == ''):
            for filename in os.listdir("./dump/weights/video"):
                if (filename.lower().endswith(('.weights'))):
                    VIDEO_WEIGHT_PATH = os.path.abspath(f'./dump/weights/video/{filename}')

    #Image Weight Selector
    def define_image_weight(self):
        Tk().withdraw()
        filename = askopenfilename()
        if (filename.lower().endswith(('.weights'))):
            IMAGE_WEIGHT_PATH = filename
        elif(filename.lower().endswith(('.cfg'))):
            IMAGE_DETECTOR_CFG_PATH = filename
        else:
            self.trigger_error("Invalid file was selected", "Invalid File")

    #Video Detector
    def open_video_detector(self):
        Tk().withdraw()
        filename = askopenfilename()
        if (not file_path.lower().endswith(('.mp4'))):
            self.trigger_error("Invalid file was selected", "Invalid File")
            return
        COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
        class_names = []
        with open(VIDEO_CLASSES, "r") as f:
            class_names = [cname.strip() for cname in f.readlines()]
        cap = cv2.VideoCapture(filename)
        model = self.create_detection_model(VIDEO_WEIGHT_PATH, VIDEO_DETECTOR_CFG_PATH)

        while True:
            _, frame = cap.read()
            width = int(frame.shape[1])
            height = int(frame.shape[0])
            dim = (width, height)
            print(dim)
            frame_resize = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            start = time.time()
            classes, scores, boxes = model.detect(frame_resize, 0.50, 0.2)
            data_mod = classes, class_names
            confidence = str(scores)
            detects = str(self.count_objects(data_mod1))
            print(f'Detections:{detects}\tImage: {file_path}\tConfidence: {confidence}')
            end = time.time()
            for (classid, score, box) in zip(classes, scores, boxes):
                color = COLORS[int(classid) % len(COLORS)]
                label = f"{class_names[classid[0]]} : {score}"
                cv2.rectangle(frame_resize, box, color, 2)
                cv2.putText(
                    frame_resize,
                    label,
                    (box[0]+5, box[1] + 25),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.5,
                    color,
                    2,
                )
            fps_label = f"FPS: {round((1.0/(end - start)),2)}"
            cv2.putText(
                frame_resize,
                fps_label,
                (0, 25),
                cv2.FONT_HERSHEY_DUPLEX,
                1,
                (0, 0, 0),
                5,
            )
        cv2.imshow("Video Predictions", frame_resize)
        if cv2.waitKey(1) == 27:
            return
        cap.release()
        cv2.destroyAllWindows()

    #Video Weight Selector
    def define_video_weight(self):
        Tk().withdraw()
        filename = askopenfilename()
        if (filename.lower().endswith(('.weights'))):
            VIDEO_WEIGHT_PATH = filename
        elif(filename.lower().endswith(('.cfg'))):
            VIDEO_DETECTOR_CFG_PATH = filename
        else:
            self.trigger_error("Invalid file was selected", "Invalid File")
    #Create Detection Model
    def create_detection_model(self,weight, cfg):
        net = cv2.dnn.readNet(weight, cfg)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=(640, 640), scale=1 / 255)
        return model

    #Count Objects
    def count_objects(self,data):
        classes, class_names = data
        counts = dict()
        for i in range(len(classes)):
            # grab class index and convert into corresponding class name
            class_index = int(classes[i])
            class_name = class_names[class_index]
            counts[class_name] = counts.get(class_name, 0) + 1
        return counts
    #Error Box Trigger
    def trigger_error(self,ErrorMsg,Error):
        tkinter.messagebox.showerror(title=Error, message=ErrorMsg)
    #Close Program
    def on_closing(self, event=0):
        self.destroy()
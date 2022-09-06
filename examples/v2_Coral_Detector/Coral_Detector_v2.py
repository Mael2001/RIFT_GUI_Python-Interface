from cgitb import grey
import time
import tkinter as tk
from tkinter import Frame, Image, Label, Radiobutton, Text, filedialog
from tkinter.constants import CENTER, FALSE, TRUE
from tkinter.font import BOLD, Font
import cv2
from tkinter import messagebox
from tkinter import font
import os
from stat import S_IREAD, S_IWRITE
from tkinter import ttk 

root = tk.Tk()
root.title('Coral Detector')

HEIGHT = 700
WIDTH = 700

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

bg_image = tk.PhotoImage(file='bgn_12.png')
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)
s = ttk.Style()

#frame = tk.Frame(root, bg='#016f84')
#frame.place(relx=0.185, rely=0.62, relwidth=0.6, relheight = 0.2)

def isChecked_C1():

  if CheckVar1.get() == 1:
        estado = TRUE
  else:
         estado = FALSE
        
  return(estado)

def isChecked_C2(): 

   if CheckVar2.get() == 1:
        estado = TRUE
   else:
         estado = FALSE
        
   return(estado)

def open_imagefile():
  os.chmod("Image_Detections.txt", S_IREAD)
  os.system("notepad.exe Image_Detections.txt")

def open_videofile():

  os.chmod("Video_Detections.txt", S_IREAD)
  os.system("notepad.exe Video_Detections.txt")
  
def weights_inuse_img():

  weights = "E6_yolov4-obj_10000.weights"

  return(weights) 

def weights_inuse_vid():

  weights = "E6_yolov4-obj_10000.weights"

  return(weights) 

frame = ttk.Frame(root)
frame.place(relx=0.19, rely=0.44, relwidth=0.6, relheight = 0.25)

CheckVar1 = tk.IntVar()
CheckVar2 = tk.IntVar()
C1 = ttk.Checkbutton(root, text = "Mostrar Visualización", command=isChecked_C1, variable = CheckVar1, onvalue = 1, offvalue = 0, width = 20)
C2 = ttk.Checkbutton(root, text = "Registrar Detecciones",command=isChecked_C2, variable = CheckVar2, onvalue = 1, offvalue = 0, width = 20)
C1.place(relx=0.29, rely=0.45, relheight=.04)
C2.place(relx=0.51, rely=0.45, relheight=0.04)

def count_objects(data): 

 classes, class_names = data

 counts = dict()
     
 for i in range(len(classes)):
            # grab class index and convert into corresponding class name
            class_index = int(classes[i])
            class_name = class_names[class_index]
            
            counts[class_name] = counts.get(class_name, 0) + 1

 return(counts)

def is_empty(any_structure):
    if any_structure:
        #print('Structure is not empty.')
        return False
    else:
        #print('Structure is empty.')
        return True

def image_detection():

 os.chmod("Image_Detections.txt", S_IWRITE)

 if isChecked_C1() == FALSE and isChecked_C2() == FALSE:
    
  file_path = []
  file_path = filedialog.askopenfilenames()

  file_txt = "Image_Detections.txt"
  file = open(file_txt, "w")
 
  file.truncate(0)

  file.seek(0) 

  file.write("                        BICA Fish Detector")
  file.write("\n\n") 
  file.write("(Read-Only)Recommendation: Save your detections to a file with a custom name using the Save As option.")
  file.write("\n\n") 

  for index, tuple in enumerate(file_path, 0): 
   
   img_relative_path = os.path.relpath(file_path[index])
   img_rel=str(img_relative_path)
   
   image = str(file_path[index])
   img = cv2.imread(image) 

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
   resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

   with open("obj_names.txt", "r") as f: 
         classes = f.read().splitlines()
 
   net = cv2.dnn.readNet(weights_inuse_img(), "yolov4-obj.cfg")
   net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
   net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

   model = cv2.dnn_DetectionModel(net)
   model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)

   classIds, scores, boxes = model.detect(resized, confThreshold=0.10, nmsThreshold=0.4)
   
   data_mod1 = classIds, classes

   file = open(file_txt, "a")

   confidence = str(scores)

   if is_empty(count_objects(data_mod1)) == False:
       detects = str(count_objects(data_mod1))
       file.write("Detections: " + detects + "\t" + "Image: " + img_rel + "\t" + "Confidence: " + confidence + "\t") 

   else: 
       file.write("Fish Found: 0"+ "\t" + "Image: " + img_rel)
       file.write("\n") 
       continue

   file.write("\n") 

   for (classId, score, box) in zip(classIds, scores, boxes):
    cv2.rectangle(resized, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
                  color=(0, 0, 255), thickness=2) 
 
    text = '%s: %.4f' %(classes[classId], score)
    cv2.putText(resized, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_DUPLEX, 1, color=(0, 0, 255), thickness=2)

    cv2.imshow('Detecciones de Roya', resized)

   if len(file_path) <= 1:
    cv2.waitKey(0)

   else: 
    cv2.waitKey(2000)
   
   cv2.destroyAllWindows()

 else:

  file_path = []
  file_path = filedialog.askopenfilenames()

  file_txt = "Image_Detections.txt"
  file = open(file_txt, "w")
 
  file.truncate(0)

  file.seek(0) 

  file.write("                        BICA Fish Detector")
  file.write("\n\n") 
  file.write("(Read-Only)Recommendation: Save your detections to a file with a custom name using the Save As option.")
  file.write("\n\n") 

  for index, tuple in enumerate(file_path, 0):

   img_relative_path = os.path.relpath(file_path[index])
   img_rel=str(img_relative_path)
 
   image = str(file_path[index])
   img = cv2.imread(image) 

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
   resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
  
   log_detections = isChecked_C2()

   with open("obj_names.txt", "r") as f: 
         classes = f.read().splitlines()
 
   net = cv2.dnn.readNet(weights_inuse_img(), "yolov4-obj.cfg")
   net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
   net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

   model = cv2.dnn_DetectionModel(net)
   model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)

   classIds, scores, boxes = model.detect(resized, confThreshold=0.10, nmsThreshold=0.4)
   
   data_mod1 = classIds, classes

   if log_detections == TRUE: 

     file = open(file_txt, "a")

     confidence = str(scores)

     if is_empty(count_objects(data_mod1)) == False:
       detects = str(count_objects(data_mod1))
       file.write("Detections: " + detects + "\t" + "Image: " + img_rel + "\t" + "Confidence: " + confidence + "\t") 

     else: 
       file.write("Fish Found: 0"+ "\t" + "Image: " + img_rel)
       file.write("\n") 
       continue

     file.write("\n") 
   else: 
      file.write("For image:" + img_rel + "\t\t") 
      file.write("Warning: Please select *Log Detections* Checkbox to be able to see the detections in the images you selected!")
      file.write("\n")

   for (classId, score, box) in zip(classIds, scores, boxes):
    cv2.rectangle(resized, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
                  color=(0, 0, 255), thickness=2)
 
    text = '%s: %.4f' % (classes[classId], score)
    cv2.putText(resized, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_DUPLEX, 1, color=(0, 0, 255), thickness=2)

    show_display = isChecked_C1()
  
   if show_display == 1:
     cv2.imshow('Image', resized)

   if len(file_path) <= 1:
    cv2.waitKey(0)

   else: 
    cv2.waitKey(2000)

  cv2.destroyAllWindows()

def video_detection(): 

 os.chmod("Video_Detections.txt", S_IWRITE)

 if isChecked_C1() == FALSE and isChecked_C2() == FALSE:

  file_path1 = filedialog.askopenfilename()

  COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

  class_names = []
  with open("obj_names.txt", "r") as f: 
    class_names = [cname.strip() for cname in f.readlines()]

    cap = cv2.VideoCapture(file_path1)
  
  net = cv2.dnn.readNet(weights_inuse_vid(), "yolov4-obj.cfg")
  net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
  net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

  model = cv2.dnn_DetectionModel(net)
  model.setInputParams(size=(416, 416), scale=1/255)

  file_txt = "Video_Detections.txt"
  file = open(file_txt, "w")
 
  file.truncate(0)

  file.seek(0)

  vid_relative_path = os.path.relpath(file_path1)
  vid_rel=str(vid_relative_path)

  file.write("                        BICA Fish Detector")
  file.write("\n\n") 
  file.write("Detections performed on(Video): " + vid_rel) 
  file.write("\n")
  file.write("(Read-Only)Recommendation: Save your detections to a file with a custom name using the Save As option.")
  file.write("\n\n")
 
  while True: 

    _, frame = cap.read()

    scale_percent = 40 # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
  
    frame_resize =  cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
     
    start = time.time()

    classes, scores, boxes = model.detect(frame_resize, 0.50, 0.2)

    data_mod = classes, class_names

    file = open(file_txt, "a")

    confidence = str(scores)

    if is_empty(count_objects(data_mod)) == False:
      detects = str(count_objects(data_mod))
      file.write("Detections: " + detects + "\t" + "Confidence: " + confidence + "\t") 
    else: 
      continue

    file.write("\n") 

    end = time.time()

    for (classid, score, box) in zip(classes, scores, boxes):

        color = COLORS[int(classid) % len(COLORS)]

        label = f"{class_names[classid]} : {score}"

        #print(class_names[classid[0]])

        cv2.rectangle(frame_resize, box, color, 2)

        cv2.putText(frame_resize, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_DUPLEX, 0.5, color, 2)

    fps_label = f"FPS: {round((1.0/(end - start)),2)}"

    cv2.putText(frame_resize, fps_label, (0, 25), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 5)
    cv2.putText(frame_resize, fps_label, (0, 25), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 3)

    cv2.imshow("Detections", frame_resize)
  
    if cv2.waitKey(1) == 27:
      break 

  cap.release()  
  cv2.destroyAllWindows()

 else: 

   file_path1 = filedialog.askopenfilename()

   COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

   class_names = []
   with open("obj_names.txt", "r") as f: 
    class_names = [cname.strip() for cname in f.readlines()]

    cap = cv2.VideoCapture(file_path1)
  
   net = cv2.dnn.readNet(weights_inuse_vid(), "yolov4-obj.cfg")
   net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
   net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

   model = cv2.dnn_DetectionModel(net)
   model.setInputParams(size=(416, 416), scale=1/255)

   file_txt = "Video_Detections.txt"
   file = open(file_txt, "w")
 
   file.truncate(0)

   file.seek(0)

   vid_relative_path = os.path.relpath(file_path1)
   vid_rel=str(vid_relative_path)

   file.write("                        BICA Fish Detector")
   file.write("\n\n") 
   file.write("Detections performed on(Video): " + vid_rel) 
   file.write("\n")
   file.write("(Read-Only)Recommendation: Save your detections to a file with a custom name using the Save As option.")
   file.write("\n\n")
 
   while True: 

    _, frame = cap.read()

    scale_percent = 100 # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

    print(dim)
  
    frame_resize = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
     
    start = time.time()

    classes, scores, boxes = model.detect(frame_resize, 0.50, 0.2)

    data_mod = classes, class_names

    log_detections = isChecked_C2()

    if log_detections == TRUE: 

     file = open(file_txt, "a")

     confidence = str(scores)

     if is_empty(count_objects(data_mod)) == False:
       detects = str(count_objects(data_mod))
       file.write("Detections: " + detects + "\t" + "Confidence: " + confidence + "\t") 
     else: 
       continue
    else:
       continue

    file.write("\n") 

    end = time.time()

    for (classid, score, box) in zip(classes, scores, boxes):

        color = COLORS[int(classid) % len(COLORS)]

        label = f"{class_names[classid[0]]} : {score}"

        cv2.rectangle(frame_resize, box, color, 2)

        cv2.putText(frame_resize, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_DUPLEX, 0.5, color, 2)

    fps_label = f"FPS: {round((1.0/(end - start)),2)}"

    cv2.putText(frame_resize, fps_label, (0, 25), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 5)
    cv2.putText(frame_resize, fps_label, (0, 25), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 3)

    show_display = isChecked_C1()

    if show_display == TRUE:

      cv2.imshow("Detections", frame_resize)
  
    if cv2.waitKey(1) == 27:
       break 

   cap.release()  
   cv2.destroyAllWindows()

button = ttk.Button(root, text="Detectar en Imagen", command=image_detection)
button.place(relx=0.23, rely=0.50, relheight=.08, relwidth=.22)
#button['font'] = cv2.FONT_HERSHEY_COMPLEX 

button2 = ttk.Button(root, text="Detectar en Video", command=video_detection)
button2.place(relx=0.53, rely=0.50, relheight=.08, relwidth=.22)
#button2['font'] = cv2.FONT_HERSHEY_COMPLEX 

button = ttk.Button(root, text="Ver Archivo (I)", command=open_imagefile)
button.place(relx=0.23, rely=0.58, relheight=.08, relwidth=.22)
#button['font'] = cv2.FONT_HERSHEY_COMPLEX 

button2 = ttk.Button(root, text="Ver Archivo (V)", command=open_videofile)
button2.place(relx=0.53, rely=0.58, relheight=.08, relwidth=.22)
#button2['font'] = cv2.FONT_HERSHEY_COMPLEX 

s.configure('TButton', font = ('Centaur', 15))


root.resizable(False, False)
root.mainloop()
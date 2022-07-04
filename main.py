from sqlalchemy import column
import readVideo
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
import helper
import clip_manager
from obtain_ROI import get_ROI_from_pictures
import os
root = Tk()

def submit(KDAscan,Healthscan,FPScount,SecAfter,Secb4,path,folder,LoadingPicturePath = None,InGamePicturePath = None,EndGamePicturePath= None):
    root.destroy()
    helper.fps = FPScount
    helper.HPbarbool = Healthscan
    helper.KDAbool = KDAscan
    helper.path = path
    helper.SecB4 = Secb4
    helper.SecAfter =SecAfter
    helper.SaveFolder = folder
    readVideo.xyz()

def check_submit(KDAscan,Healthscan,FPScount,SecAfter,Secb4,path,folder,LoadingPicturePath,InGamePicturePath,EndGamePicturePath):
    print("KDAboolean: {0}, Healthboolean: {1}, FPScount: {2}, SecB4: {3}, SecAFter {4}, path {5}, folder {6}".format(KDAscan,Healthscan,FPScount,Secb4,SecAfter,path,folder))
    print("LoadingPicturePath: {0}, InGamePicturePath: {1}, EndGamePicturePath {2}".format(LoadingPicturePath,InGamePicturePath,EndGamePicturePath))
    try:
        Secb4 = int(Secb4)
        SecAfter = int(SecAfter)
    except:
        tkinter.messagebox.showinfo("Error",  "Enter Intagers for time period to collect before and after an event.")
    else:
        if not os.path.isfile(path) or not (".jpg" in path or ".png" in path or ".mp4" in path):
            tkinter.messagebox.showinfo("Error",  "Not a valid path for video.")
        elif not os.path.isdir(folder):
            tkinter.messagebox.showinfo("Error",  "Not a valid output folder.")

        if os.path.isfile(LoadingPicturePath) and (".jpg" in LoadingPicturePath or ".png" in LoadingPicturePath) :
            get_ROI_from_pictures(LoadingPicturePath)
        if os.path.isfile(InGamePicturePath) and (".jpg" in InGamePicturePath or ".png" in InGamePicturePath):
            get_ROI_from_pictures(InGamePicturePath)
        if os.path.isfile(EndGamePicturePath) and (".jpg" in EndGamePicturePath or ".png" in EndGamePicturePath):
            get_ROI_from_pictures(EndGamePicturePath)
        submit(KDAscan,Healthscan,FPScount,SecAfter,Secb4,path,folder)

#de-bug method for button testing
def getBool(variable):
    print(str(variable) + ": " + str(variable.get()))

#File explorer function
def open_videos(FilePath_Box):
    file = filedialog.askopenfile(initialdir="C/", title="Select a file", filetypes=[('Video files', '*.mp4')])
    if file is not None:
        FilePath_Box.set(file.name)

def open_file_pictures(FilePath_Box):
    file = filedialog.askopenfile(initialdir="C/", title="Select a file", filetypes=[("Image files","*.png *.jpg"),('All files','*.*')])
    if file is not None:
        FilePath_Box.set(file.name)

def open_folder(OutputFolder_Box):
    folder = filedialog.askdirectory()
    if folder is not None:
        OutputFolder_Box.set(folder)

def create_scanner_frame(container,KDAscan,Healthscan):
    frame = tkinter.Frame(container)
    scannerLabel = Label(frame, text= "What scanners do you want to use to trigger clips? \n You may select more than one.")

    KDAButton = Checkbutton(frame, text ="KDA scanner",
                            variable = KDAscan,
                            onvalue = True,
                            offvalue = False,
                            )
    HealthButton = Checkbutton(frame, text ="Helathbar scanner",
                            variable = Healthscan,
                            onvalue = True,
                            offvalue = False,
                            )

    scannerLabel.grid(column=0,row=0)                        
    KDAButton.grid(row=1,column=0,sticky=W)
    HealthButton.grid(row=1,column=1,sticky=W)    
    
    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=5)
    return frame

def create_input_frame(container,FilePath,OutputFolder):
    frame = tkinter.Frame(container)

    FilePathLabel = Label(frame, text= "Input video file Path")
    OutputFolderLabel = Label(frame, text= "Output clips folder Path")

    FilePath_Box = Entry(frame,textvariable=FilePath)
    InputbrowseButton = Button(frame, text="Browse", command=lambda:open_videos(FilePath))

    OutputFolder_Box = Entry(frame,textvariable=OutputFolder)
    OutputbrowseButton = Button(frame, text="Browse", command=lambda:open_folder(OutputFolder))

    FilePathLabel.grid(row=0,column=0,sticky=W)
    FilePath_Box.grid(row=0,column=1,sticky=W)
    InputbrowseButton.grid(row=0,column=2)
    OutputFolderLabel.grid(row=1,column=0,sticky=W)
    OutputFolder_Box.grid(row=1,column=1,sticky=W)
    OutputbrowseButton.grid(row=1,column=2,sticky=W)

    return frame

def create_fps_buttons_frame(container,FPScount):
    frame = tkinter.Frame(container)
    SelectFPSLabel = Label(frame, text= "What FPS is the video in?")

    #Radio buttons
    values = (("30 FPS",30),("60 FPS",60))
    for index,fps in enumerate(values):
        r = Radiobutton(frame,
                        text = fps[0],
                        value = fps[1],
                        variable=FPScount)
        r.grid(row=1,column=index)

    SelectFPSLabel.grid(row=0,column=0,sticky=W)

    return frame

def create_seconds_input_frame(container,SecB4,SecAfter):
    frame = tkinter.Frame(container)
    SecB4_Label = Label(frame,text="Seconds before event to record")
    SecAfter_Label = Label(frame,text="Seconds After event to record")
    SecB4_Box = Entry(frame,text="Seconds before event to record",textvariable=SecB4)
    SecAfter_Box = Entry(frame,text="Seconds After event to record",textvariable=SecAfter)    
    frame = tkinter.Frame(container)
    SecB4_Label.grid(row=0,column=0)
    SecB4_Box.grid(row=0,column=1)
    SecAfter_Label.grid(row=1,column=0)
    SecAfter_Box.grid(row=1,column=1)
    return frame

def create_pictures_frame(container,LoadingPicture,InGamePicture,EndGamePicture):
    frame = tkinter.Frame(container)
    LoadingImageLabel = Label(frame, text= "Image containing a loading screan")
    IngameImageLabel = Label(frame, text= "Image containing in game UI")
    EndgameImageLabel = Label(frame, text= "Image containing the victory or defeat banner")

    LoadingImage_Box = Entry(frame,textvariable=LoadingPicture)
    IngameImage_Box = Entry(frame,textvariable=InGamePicture)
    EndgameImage_Box = Entry(frame,textvariable=EndGamePicture)

    LoadingImageButton = Button(frame, text="Browse", command=lambda:open_file_pictures(LoadingPicture))
    IngameImageButton = Button(frame, text="Browse", command=lambda:open_file_pictures(InGamePicture))
    EndgameImageButton = Button(frame, text="Browse", command=lambda:open_file_pictures(EndGamePicture))

    LoadingImageLabel.grid(row=0,column=0,sticky=W)
    LoadingImage_Box.grid(row=0,column=1,sticky=W)
    LoadingImageButton.grid(row=0,column=2)
    IngameImageLabel.grid(row=1,column=0,sticky=W)
    IngameImage_Box.grid(row=1,column=1,sticky=W)
    IngameImageButton.grid(row=1,column=2,sticky=W)
    EndgameImageLabel.grid(row=2,column=0,sticky=W)
    EndgameImage_Box.grid(row=2,column=1,sticky=W)
    EndgameImageButton.grid(row=2,column=2,sticky=W)

    return frame

def main():
    clip_manager.__init__()
    helper.__init__()
    
    #variables
    KDAscan = tkinter.BooleanVar(root, name="KDAscan", value=helper.KDAbool)
    Healthscan = BooleanVar(root, name = "Healthscan",value=helper.HPbarbool)
    FilePath = StringVar(name = "FilePath")
    OutputFolder = StringVar(name = "OutputFolder", value= helper.SaveFolder)
    FPScount = IntVar(root, name= "FPScount", value = helper.fps)
    SecB4 = IntVar(root, name ="SecB4", value=helper.SecB4)
    SecAfter = IntVar(root,name="SecAfter",value=helper.SecAfter)
    LoadingPicturePath = StringVar(name = "LoadingPicture", value= helper.LoadingPicture)
    InGamePicturePath = StringVar(name = "InGamePicture", value= helper.InGamePicture)
    EndGamePicturePath = StringVar(name = "EndGamePicture", value= helper.EndGamePicture)

    #Labels and Entry Boxes
    root.title("Window")

    #GUI set up
    scanner_frame = create_scanner_frame(root,KDAscan,Healthscan)
    scanner_frame.grid(column=0,row=0)
    
    input_frame = create_input_frame(root,FilePath,OutputFolder)
    input_frame.grid(column=0,row=1,sticky=W)

    fps_buttons = create_fps_buttons_frame(root,FPScount)
    fps_buttons.grid(column=0,row=2,sticky=W)

    seconds_input = create_seconds_input_frame(root,SecB4,SecAfter)
    seconds_input.grid(column=0,row=3,sticky=W)

    create_pictures = create_pictures_frame(root,LoadingPicturePath,InGamePicturePath,EndGamePicturePath)
    create_pictures.grid(column=0,row=4)

    #Buttons
    submitButton = Button(root, text="Submit", command=lambda: check_submit(KDAscan.get(),Healthscan.get(),
                                                                FPScount.get(),SecAfter.get(),SecB4.get(),
                                                                FilePath.get(),OutputFolder.get(),
                                                                LoadingPicturePath.get(),InGamePicturePath.get(),EndGamePicturePath.get()))   

    submitButton.grid(row=10,column=0,sticky=E)
    root.mainloop()

if __name__ == "__main__":
    main()
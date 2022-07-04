from google.protobuf import text_format as pbtf
import numpy as np
import json


with open ("settings.json") as f:
    settingJson = json.load(f)
dictBox = settingJson["dictBox"]
fps = settingJson["fps"]
KDAbool = settingJson["KDAbool"]
HPbarbool = settingJson["HPbarbool"]
SecB4 = settingJson["SecB4"]
SecAfter = settingJson["SecAfter"]
path = r"workspace/videos/full vod_Trim6_Trim.mp4"
LoadingPicture = None
InGamePicture = None
EndGamePicture = None
SaveFolder = settingJson["SaveFolder"]
detections = None
compareImageDict = {}


def __init__():
    with open ("settings.json") as f:
        settingJson = json.load(f)
    dictBox = settingJson["dictBox"]
    fps = settingJson["fps"]
    KDAbool = settingJson["KDAbool"]
    HPbarbool = settingJson["HPbarbool"]
    SecB4 = settingJson["SecB4"]
    SecAfter = settingJson["SecAfter"]
    path = r"workspace/videos/full vod_Trim6_Trim.mp4"
    LoadingPicture = r"workspace\videos\loading.jpg"
    InGamePicture = r"workspace\videos\ingame.jpg"
    EndGamePicture = r"workspace\videos\end.jpg"
    SaveFolder = settingJson["SaveFolder"]
    detections = None
    compareImageDict = {}

def printStuff():
    print(fps,KDAbool,HPbarbool,SecB4,SecAfter,path,SaveFolder
    )

def create_box_dictionary():
    item_id = None
    item_name = None
    with open(r"workspace\label_map.pbtxt") as file:
        for line in file:
            if "id" in line:
                item_id = int(line.split(":", 1)[1].strip())
            elif "name" in line:
                item_name = line.split(":", 1)[1].replace("'", "").strip()
            elif item_name is not None and item_id is not None:
                if item_name == "loading":
                    dictBox.update({item_id-1:{"score":0.4, "label":item_name,"box":[0,1,0,1]}})
                elif item_name == "defeat":
                    dictBox.update({item_id-1:{"score":0.4, "label":item_name,"box":[0,1,0,1]}})
                elif item_name == "victory":
                    dictBox.update({item_id-1:{"score":0.4, "label":item_name,"box":[0,1,0,1]}})                    
                else:
                    dictBox.update({item_id-1:{"score":0.4, "label":item_name,"box":[]}})
    return dictBox

def get_Label(label):
    for key in dictBox.keys():
        if label in dictBox:
            return(dictBox[label]["label"])


def main():
    __init__()
    print(dictBox["0"])
    print(get_Label("0"))

    pass


if __name__ == "__main__":
    main()
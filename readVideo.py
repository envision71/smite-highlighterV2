import numpy as np
from sympy import fps
from obtain_ROI import get_ROI
import clip_manager
import clip_maker
import cv2 as cv
import helper

def ROI(frame):
    dictBox = get_ROI(frame)

def xyz():
    hpFlag = True
    path = helper.path
    dictBox = helper.dictBox
    inGameFlag = False
    loadingFlag = False
    HPbarFlag = False
    KDAFlag = False
    KillsFlag = False
    defeatFlag = False
    victoryFlag = False
    comapreImage = np.array
    if ".mp4" in path:
        cap = cv.VideoCapture(path)

        while cap.isOpened():
            ret, frame = cap.read()
            frameNum = int(cap.get(cv.CAP_PROP_POS_FRAMES))
            if not ret:
                clip_maker.create_clip()
                cap.release()
                break
            if cv.waitKey(1) & 0xFF == ord('q'):
                print(dictBox)
                cap.release()
                clip_maker.create_clip()
                break
            cv.imshow("window",cv.resize(frame, (800, 600)))
            
            if not HPbarFlag or not KDAFlag or not KillsFlag:
                dictBox = get_ROI(frame)


            for key,value in dictBox.items():
                if not inGameFlag:
                    if value["label"] == "loading":
                        if not value["box"] == [0,1,0,1]:
                            inGameFlag == True
                # if value["label"] == "victory" and value["box"] == [0,1,0,1]: 
                #     dictBox = get_ROI(frame)
                # if (value["label"] == "victory" and not value["box"] == [0,1,0,1]) or (value["label"] == "defeat" and not value["box"] == [0,1,0,1]):
                #     inGameFlag = False
                  
                
                if not value["box"] == []:
                    y1 = int(value["box"][2])
                    y2 = int(value["box"][3])
                    x1 = int(value["box"][0])
                    x2 = int(value["box"][1])
                    crop_img = frame[y1:y2,x1:x2]
                    placeholder =  cv.cvtColor(crop_img, cv.COLOR_BGR2GRAY)
                    if not inGameFlag and value["label"] == "loading":
                        err = np.sum((helper.compareImageDict["loading"].astype("float") - placeholder.astype("float")) ** 2 )
                        err /= float(helper.compareImageDict["loading"].shape[0] * crop_img.shape[1])
                        if 20 <= err <= 30:
                            inGameFlag = True
                    

                    if inGameFlag:
                        
                        if value["label"] == "HPbar" and not value["box"] == []:
                            HPbarFlag = True
                        if value["label"] == "KDA" and not value["box"] == []:
                            KDAFlag = True                    
                        if value["label"] == "Kills" and not value["box"] == []:
                            KillsFlag = True 
                        if helper.HPbarbool:
                            if(value["label"] == "HPbar"):
                                mask = cv.inRange(crop_img,(0,0,0),(10,20,35))
                                ratio = ((mask.size-cv.countNonZero(mask)))/(mask.size)
                                mask = cv.putText(crop_img,str(ratio), (10,20),
                                            cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2,
                                            cv.LINE_AA )
                                if ratio > 0.3 and not hpFlag:
                                    hpFlag = True
                                if ratio <= 0.3 and hpFlag:
                                    hpFlag = False
                                    clip_manager.add_clip(value["label"],frameNum,
                                                            int(frameNum/helper.fps) - int(helper.SecB4),
                                                            int(frameNum/helper.fps) + int(helper.SecAfter))
                        else: HPbarFlag = True

                        if helper.KDAbool:
                            if value["label"] == "Kills":
                                err = np.sum((helper.compareImageDict["Kills"].astype("float") - placeholder.astype("float")) ** 2 )
                                err /= float(helper.compareImageDict["Kills"].shape[0] * crop_img.shape[1])
                                helper.compareImageDict["Kills"] = placeholder
                                # print(err)
                                if 200 < err < 1950:
                                    print("warning: " +str(err))
                                    cv.imshow("placeholder",placeholder)
                                    cv.imshow(str(value["label"]),cv.resize(frame, (800, 600)))
                                    clip_manager.add_clip(value["label"],frameNum,
                                            int(frameNum/helper.fps) - int(helper.SecB4),
                                            int(frameNum/helper.fps) + int(helper.SecAfter))
                        else: 
                            KDAFlag = True
                            KillsFlag = True
                        
                    cv.imshow(str(value["label"]),crop_img)
                    cv.imshow("testing", helper.compareImageDict["loading"])
    else:
        return
    

def main():
    clip_manager.__init__()
    path = r"C:\Users\Tdog\Pictures\Screenshots\Screenshot (4).png"
    path = r"workspace\videos\full vod_Trim6_Trim_Trim.mp4"
    xyz()



if __name__ == "__main__":
    main()
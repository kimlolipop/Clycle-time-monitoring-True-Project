import cv2
import numpy as np
import pandas as pd
from collections import Counter
from ast import literal_eval


video_path = 'D:/Git project/cycle_time_monitoring/Clycle-time-monitoring-True-Project/double-process.avi'
csv_path = 'weight.csv'

def read_weight(csv_path):
    df = pd.read_csv(csv_path)
    
    method = df['method'].tolist()
    state = df['state'].tolist()
    coordinate = df['coordinate'].tolist()
    upper = df['upper'].tolist()
    lower = df['lower'].tolist()
    
    print(method, state, coordinate, upper, lower)
    
    return method, state, coordinate, upper, lower


def detail_video(cap):
    # fps
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Get the total numer of frames in the video. value same as image frame
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    #Time of video(sec)
    if frame_count != 0:
        duration = frame_count / fps
    else: 
        duration = 0
        
    return fps, frame_count, duration
    

def setup_param(method):
    
    bgsubknn = []
    fg = []
    L_status = []
    crop_frame = []
    relay = []
    relay_status = []
    
    
    dict_method = dict(Counter(method)) # {'image subtraction' : 2 , 'color space' : 1}
    no_method = len(method) # 3
    duplicate_method = list(dict_method.keys()) # ['image subtraction', 'color space']
    no_image_subtraction = dict_method['image subtraction'] # 2
    no_color_space = dict_method['color space'] # 1
    
    # image subtraction==================================
    for i in range(no_image_subtraction):
        bgsubknn.append(cv2.createBackgroundSubtractorKNN(40))
        crop_frame.append([])
        fg.append([])
        relay.append([])
        relay_status.append(False)
        L_status.append(False)
        
    # color space=========================================
    for i in range(no_color_space):
        crop_frame.append([])
        fg.append([])
        relay.append([])
        relay_status.append(False)
        L_status.append(False)
    
    relay.append([])
    
    return bgsubknn, relay, relay_status, L_status, no_method, crop_frame, fg, no_image_subtraction, no_color_space
    
    
    
    

def main(video_path ,csv_path):
    cap = cv2.VideoCapture(video_path)
    
    # weight
    method, state, coordinate, upper, lower = read_weight(csv_path)
    
    # detail
    fps, frame_count, duration = detail_video(cap)
    
    # setup param
    (bgsubknn, relay, relay_status, L_status, no_method, 
     crop_frame, fg, no_image_subtraction, no_color_space) = setup_param(method)
    
    for i in range(len(relay)):
        relay[i] = 0
    relay[-1] = 30 # relay will have more than point of interest +1
    time = 0 
#     print(sum(L_status), len(L_status))
    count = 0
    
    # read video
    while True:
        ret, img = cap.read()
        if not ret:
            break
        time += 1
        
        frame = cv2.GaussianBlur(img ,(5,5),0)   
        cv2.imshow('frame', img)
        
        
# ============== loop follow param =============================================
        no_count_color_space = 0
        no_count_img_subtraction = 0
        for z in range(no_method):
            if state[z] != -1:
                crop_frame[z] = crop(frame, coordinate[z])
                
        # ================== pre process follow method ==================
                if method[z] == 'image subtraction':
                    fg[z] = img_subtrack(crop_frame[z], bgsubknn[no_count_img_subtraction])
                    no_count_img_subtraction += 1 
                    
                    
                elif method[z] == 'color space':
                    fg[z] = color_space(crop_frame[z], upper[z], lower[z])
                    no_count_color_space += 1
                    
        # ========================= check status ==========================
                # threshold + relay management
#                 print(state[z])
#                 print(time)
                if state[z] == 1:
#                     print('a')
#                     print("z: {2} locate1: {0}, locate2: {1}".format((np.sum(fg[0])), (np.sum(fg[1])), z))
#                     print(relay[z])
                    
                    if np.sum(fg[z]) > 100000 and relay[z] > relay[-1]: # relay[-1] = threshold when start video
                        L_status[z] = True
                        relay_status[z] = True
                        relay[z] = 0
                        print('a')
                        
                elif state[z] > 1:
                    if np.sum(fg[z]) > 100000 and relay[z] > relay[-1] and relay_status[z-1] == True:
                        L_status[z] = True
                        relay_status[z] = True
                        relay[z] = 0
                        print('b')
                        
#         print(sum(L_status), len(L_status), time, np.sum(fg[0]),np.sum(fg[1]))      
        print(count, relay[0], relay_status[0],L_status[0], relay[1],relay_status[1], L_status[1],relay[2],relay_status[2],L_status[2],time, np.sum(fg[0]),np.sum(fg[1]))      

        # recheck line 3
        if sum(L_status) == len(L_status):
            for k in range(len(relay_status)):
                L_status[k]= False
            if sum(relay_status) == len(relay_status):
                for k in range(len(relay_status)):
                    relay_status[k]= False
                count += 1
#                 print('process:', count)

        for k in range(len(relay_status)):
            if relay_status[k] == False:
                relay[k] += 1


#             if relay[k] >= relay[-1]:
#                 relay_status[k] = True
#                 relay[k] = 0
                

                
                
                
                
        
        
        cv2.imshow('frame2', crop_frame[0])
        cv2.imshow('frame3', crop_frame[1])
#         cv2.imshow('frame4', crop_frame[2])
        cv2.imshow('frame7', fg[0])
        cv2.imshow('frame8', fg[1])
#         cv2.imshow('frame9', fg[2])
        
        key = cv2.waitKey(100)
        if key ==27:
            break
    print('total process:',count)
    
    
    

    
def crop(frame, coordinate):
    coor = literal_eval(coordinate)
    x1 = coor[0] 
    y1 = coor[1] 
    x2 = coor[2]
    y2 = coor[3]
    
    crop_frame = frame[y1:y2, x1:x2]
    return crop_frame
    
    
def img_subtrack(frame, bgsubknn):
    fg = bgsubknn.apply(frame)
    return fg


def color_space(frame, upper, lower):
    HLS = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    lower_color = np.array(literal_eval(lower))
    upper_color = np.array(literal_eval(upper))
    fg = cv2.inRange(HLS ,lower_color, upper_color)

    return fg
    

main(video_path, csv_path)

    
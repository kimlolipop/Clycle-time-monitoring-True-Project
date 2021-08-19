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
        L_status.append(False)
        
    # color space=========================================
    for i in range(no_color_space):
        crop_frame.append([])
        L_status.append(False)
        
        
    
    return bgsubknn, L_status, no_method, crop_frame, fg, no_image_subtraction, no_color_space
    

def main(video_path ,csv_path):
    cap = cv2.VideoCapture(video_path)
    
    # weight
    method, state, coordinate, upper, lower = read_weight(csv_path)
    
    # detail
    fps, frame_count, duration = detail_video(cap)
    
    # setup param
    (bgsubknn, L_status, no_method, 
     crop_frame, fg, no_image_subtraction, no_color_space) = setup_param(method)
     
    
    # read video
    while True:
        ret, img = cap.read()
        if not ret:
            break
        frame = cv2.GaussianBlur(img ,(5,5),0)   
        cv2.imshow('frame', img)
        
        
# ============== loop follow param =============================================
        # image subtraction
        no_count_function = -1 # use for L_status/ count loop current method
        for i in range(no_image_subtraction):
            no_count_function += 1
            if state[no_count_function] != -1:
                coor = literal_eval(coordinate[no_count_function])
                
                x1 = coor[0] 
                y1 = coor[1] 
                x2 = coor[2] 
                y2 = coor[3] 
                
                crop_frame[no_count_function] = frame[y1:y2, x1:x2]
                
                if method[i] == 'image subtraction':
                    fg[i] = img_subtrack(crop_frame[no_count_function], bgsubknn[i])
        
        # color space
        for i in range(no_color_space):
            no_count_function += 1
            if state[no_count_function] != -1:
                coor = literal_eval(coordinate[no_count_function])

                x1 = coor[0] 
                y1 = coor[1] 
                x2 = coor[2] 
                y2 = coor[3] 

                crop_frame[no_count_function] = frame[y1:y2, x1:x2]
                
                # edit tommorow / mock value color space
                if method[i] == 'color space':
                    fg[i] = color_space(crop_frame[no_count_function])
        
                
        # add L status
        
        
        # L status
        
        
        cv2.imshow('frame2', crop_frame[0])
        cv2.imshow('frame3', crop_frame[1])
        cv2.imshow('frame7', fg[0])
        cv2.imshow('frame8', fg[1])
        
        key = cv2.waitKey(1)
        if key ==27:
            break
        
    
    
    

    
    
    
    
def img_subtrack(frame, bgsubknn):
    return bgsubknn.apply(frame)
#     return x



def color_space(frame):
    print('error')
    return 10
    

main(video_path, csv_path)

    
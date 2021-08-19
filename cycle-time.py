import cv2
import numpy as np

#ใช่แบบนี้ไม่ต้องเก็บ buffer เอง
path = 'double-process.avi'
cap = cv2.VideoCapture(path)

# setting record
# frame_width = int(cap.get(3))
# frame_height = int(cap.get(4))
# out = cv2.VideoWriter('outpy_2.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

# Get the frames per second
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)

# Get the total numer of frames in the video. value same as image frame
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
print(frame_count)

#Time of video(sec)
duration = frame_count / fps
print(duration)

# bgsubknn = cv2.createBackgroundSubtractorKNN(40) # มักจะดีกว่า , default จะเก็บ buffer 400 - 500 grame
# L1 = np.r_[50:53]
# L2 = np.r_[60:63]


L1_status, L2_status = False, False
count = 0
relay = [0, 50, 0]
relay_status = False

timer = 0
process_time = 0
cycle_time = []
std_time = 9
green = (0, 255, 0)
red = (0, 0, 255)


bgsubknn1 = cv2.createBackgroundSubtractorKNN(40)
bgsubknn2 = cv2.createBackgroundSubtractorKNN(40)
y1 = 140
y2 = 200
x1 = 50
x2 = 200

yy1 = 170
yy2 = 250
xx1 = 430
xx2 = 500

process_n = 0 # flase=process, True=double-process
process_s = 0

c=0
u=1
while True:
    ret, img = cap.read()
    if not ret:
        break
    frame = cv2.GaussianBlur(img ,(5,5),0)

    c += 1
    timer += 1
    
    
    crop_frame1 = frame[y1:y2, x1:x2]
    crop_frame2 = frame[yy1:yy2, xx1:xx2]

    fg1 = bgsubknn1.apply(crop_frame1)
    fg2 = bgsubknn2.apply(crop_frame2)

#     print(relay_status)
    # print(np.sum(fg1))
    relay[2] += 1 # action
    if np.sum(fg1) > 100000 and c > 100 and relay[2] > 50:
        L1_status = True
        process_n += 1
    
        relay[2] = 0
    else:
        u=1


    if np.sum(fg2) > 80000 and c > 100 and relay_status == True:
        L2_status = True
    else:
        u=1



    # check status
    # print(L1_status, L2_status, relay_status, np.sum(fg1))
    
    if L1_status and L2_status:
        L1_status = False
        L2_status = False

        if relay_status:
            relay_status = False
            L1_status = False
            L2_status = False
            process_n = 0

            count += 1
            print(count)
            

            process_time = timer/fps
            cycle_time.append(process_time)

            print(cycle_time)
            print(sum(cycle_time)/len(cycle_time))
            timer = 0

    process_s = process_n
    # condition relay
    if relay_status == False:
        relay[0] += 1
        

    if relay[0] >= relay[1]:
        relay_status = True
        relay[0] = 0

    
    cv2.putText(img, 'Timer: ' + str(round(timer/fps)) + ' Sec', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(img, 'Std. time = ' + str(round(std_time)) + ' Sec', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    if process_time > std_time:
        color = red
        cv2.putText(img, 'process_time = ' + str(round(process_time)) + ' Sec', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5,color, 2)
    else:
        color = green
        cv2.putText(img, 'process_time = ' + str(round(process_time)) + ' Sec', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    if process_s == 0:
        txt = 'none'
    elif process_s == 1:
        txt = 'process'
    elif process_s >= 2:
        txt = 'double-process'
    
    cv2.putText(img, 'status: ' + txt, (400, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    

    # out.write(frame)
    cv2.imshow('frame', img)
    cv2.imshow('frame2', fg1)
    cv2.imshow('frame3', fg2)


    key = cv2.waitKey(1)
    if key ==27:
        break

print(cycle_time)
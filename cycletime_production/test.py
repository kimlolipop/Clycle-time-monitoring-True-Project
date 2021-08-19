# import pandas as pd

# df = pd.read_csv('weight.csv')


# me = df['method'].tolist()

# print(me)


# print(df['method'].iloc[0])
# print(len(df['method']))

# import cv2

# cap = cv2.VideoCapture('D:/Git project/cycle_time_monitoring/Clycle-time-monitoring-True-Project/double-process.avi')

# while True:
#         ret, img = cap.read()
#         if not ret:
#             break
#         frame = cv2.GaussianBlur(img ,(5,5),0)   
#         cv2.imshow('frame', img)


#         key = cv2.waitKey(1)
#         if key ==27:
#             break

from ast import literal_eval

a = "[1,2,3]"
print(literal_eval(a))


# def parser(str: str):
#     trim_str = str[1:-1]
#     array = trim_str.split(',')
#     print(array)
#     return array

import pandas as pd

df = pd.DataFrame()

coor = [[1,2,3,4],[10,20,30,40]]

df['coor'] = coor
print(df)



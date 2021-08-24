import os
import pandas as pd
import numpy as np 
from ast import literal_eval

def combine(path):
    filename = os.listdir(path)
#     filename = os.listdir('parameter/')

    method_lst = []
    state_lst = []
    threshold_lst = []
    coordinate_lst = []
    upper_lst = []
    lower_lst = []
    
    
    for i in range(len(filename)):
        method, state, threshold,coordinate, upper, lower = read_weight(filename[i])
        for j in range(len(method)):
        
            method_lst.append(method[j])
            state_lst.append(state[j])
            threshold_lst.append(threshold[j])
            coordinate_lst.append(coordinate[j])
            upper_lst.append(upper[j])
            lower_lst.append(lower[j])
        print(i)
#         print(method, state, threshold, coordinate, upper, lower)
    
    print("Real==>", method_lst, state_lst, threshold_lst, coordinate_lst, upper_lst, lower_lst)
    return method_lst, state_lst, threshold_lst, coordinate_lst, upper_lst, lower_lst
    
    


def read_weight(csv_path):
    df = pd.read_csv('parameter/' + csv_path)
    
    method = df['method'].tolist()
    state = df['state'].tolist()
    coordinate = df['coordinate'].tolist()
    upper = df['upper'].tolist()
    lower = df['lower'].tolist()
    threshold = df['threshold'].tolist()
    
    for j in range(len(threshold)):
        threshold[j] = literal_eval(threshold[j])
    
    return method, state, threshold, coordinate, upper, lower


# def test(csv_path):
#     df = pd.read_csv(csv_path)
    
#     method = df['method'].tolist()
#     state = df['state'].tolist()
#     coordinate = df['coordinate'].tolist()
#     upper = df['upper'].tolist()
#     lower = df['lower'].tolist()
#     threshold = df['threshold'].tolist()
    
#     for j in range(len(threshold)):
#         threshold[j] = literal_eval(threshold[j])
    
    
#     print("test==>",method, state, threshold, coordinate, upper, lower)
    
#     return method, state, threshold, coordinate, upper, lower

# combine()
# print('/n /n')
# test('parameter/fin.csv')
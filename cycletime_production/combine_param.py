import os

def combine():
    filename = os.listdir('parameter/')
    method, state, threshold,coordinate, upper, lower = read_weight(csv_path)
combine()

def read_weight(csv_path):
    df = pd.read_csv('parameter/' + csv_path)
    
    method = df['method'].tolist()
    state = df['state'].tolist()
    coordinate = df['coordinate'].tolist()
    upper = df['upper'].tolist()
    lower = df['lower'].tolist()
    threshold = df['threshold'].tolist()
    print(method, state, coordinate, upper, lower)
    
    return method, state, threshold, coordinate, upper, lower
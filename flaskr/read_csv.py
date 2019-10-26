import pandas as pd


def get_room_num(data):
    rooms = []
    for i in range(len(data)):
        room_name = data.iloc[i][2]
        rooms.append(room_name)
    return len(set(rooms))


def get_empty_room_num(path):
    data = pd.read_csv(path)
    num_rooms = get_room_num(data)
    init_value = [num_rooms for i in range(5)]
    result_data = {
        'Mon': init_value.copy(), 
        'Tue': init_value.copy(), 
        'Wed': init_value.copy(), 
        'Thu': init_value.copy(), 
        'Fri': init_value.copy()}

    for i in range(len(data)):
        row = data.iloc[i]
        day, time = row[0], row[1]
        result_data[day][time - 1] -= 1

    return result_data

if __name__ == '__main__':
    path = "../data.csv"
    data = get_empty_room_num(path)
    print(data)

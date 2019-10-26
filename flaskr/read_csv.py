import pandas as pd
import copy

from flaskr.models import Event

class RoomData(object):
    def __init__(self, csv_path):
        data = pd.read_csv(csv_path)
        self.all_rooms = self.get_all_rooms(data)
        self.class_rooms = self.get_class_rooms(data)
        self.event_rooms = self.get_event_rooms()

    def get_all_rooms(self, data):
        rooms = []
        for i in range(len(data)):
            room_name = data.iloc[i][2]
            rooms.append(room_name)
        return list(set(rooms))

    def get_class_rooms(self, data):
        init_value = [[] for i in range(5)]
        result_data = {
            'Mon': copy.deepcopy(init_value),
            'Tue': copy.deepcopy(init_value),
            'Wed': copy.deepcopy(init_value),
            'Thu': copy.deepcopy(init_value),
            'Fri': copy.deepcopy(init_value)}

        for i in range(len(data)):
            row = data.iloc[i]
            day, time, room = row[0], row[1]-1, row[2]
            result_data[day][time].append(room)
        
        return result_data

    def get_event_rooms(self):
        init_value = [[] for i in range(5)]
        result_data = {
            'Mon': copy.deepcopy(init_value),
            'Tue': copy.deepcopy(init_value),
            'Wed': copy.deepcopy(init_value),
            'Thu': copy.deepcopy(init_value),
            'Fri': copy.deepcopy(init_value)}
        events = Event.query.all()
        print("Events", events)
        for event in events:
            result_data[event.day][int(event.time)].append(event)
            print(result_data)
        return result_data

    def get_empty_rooms(self):
        init_value = [[] for _ in range(5)]
        result_data = {
            'Mon': [], 
            'Tue': [], 
            'Wed': [],
            'Thu': [],
            'Fri': []}
        print(result_data)
        for day, schedule in self.class_rooms.items():
            for time in range(len(schedule)):
                empy_rooms = list(set(self.all_rooms) - set(schedule[time]))
                print(empy_rooms)
                result_data[day].append(empy_rooms)

        return result_data

if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    data = RoomData(path)
    print(data.all_rooms)
    print(data.get_empty_rooms())

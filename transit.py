from ctypes import Array


class Station:
    def __init__(self, name):
        self.name = name
        self.lines = []
        self.next = []
        self.prev = []
    
    def add_line(self, line_obj):
        self.lines.append(line_obj)
    
    def add_next(self, st):
        self.next.append(st)
        
    def add_prev(self, st):
        self.prev.append(st)
    
    def __str__(self):
        return self.name

class Line:
    def __init__(self):
        self.stations = []
        self.number = 0
            
    def add_station(self, station):
        self.stations.append(station)
    
    def get_stations(self):
        return self.stations
    
    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number
    
    def __str__(self):
        result = ""
        for st in self.stations:
            result += st.name + " "
        return result

class Network:
    def __init__(self):
        self.lines = []
        self.stations = [] # array used to prevent duplicate station objects, where two or more lines share a station with the same name
    
    def add_line(self, line):
        self.lines.append(line)
    
    # returns False if station with that name doesn't exist in self.stations. returns Station object if station with that name is found in self.stations
    def get_station_obj(self, station_name):
        for station in self.stations:
                if station_name == station.name:
                    return station
        return False
    
    # reads file, line by line. adds station objects to new line objects, and line objects to lines array
    def generate_network_from_file(self, file_to_read):
        network_file = open(file_to_read, 'r') # file_to_read: String = "file.txt"
        
        for row in network_file:
            row_separated = row.split(",")
            
            new_line = Line()
            
            prev_st = None
            count = 0
            for item in row_separated:
                item = item.replace('\n', '')
                
                if count == 0:
                    new_line.set_number(item)
                    count = 1
                    continue
                
                # checked_st = False: station doesn't exist yet - checked_st = Station obj: station with that name already exists
                checked_st = self.get_station_obj(item)
                
                if not checked_st:
                    new_st = Station(item)
                    new_line.add_station(new_st)
                    self.stations.append(new_st)
                    
                    new_st.add_line(new_line)
                    if not prev_st == None:
                        new_st.add_prev(prev_st)
                        prev_st.add_next(new_st)
                    prev_st = new_st # prev_st, new_st, new_st (next loop)
                    
                    continue
                
                # check_if_station_exists() returned Station object
                new_st = checked_st
                
                new_line.add_station(new_st)
                new_st.add_line(new_line)
                
                if not prev_st == None:
                    if new_st not in prev_st.next:
                        prev_st.add_next(new_st)
                    if prev_st not in new_st.prev:
                        new_st.add_prev(prev_st)
                        
                prev_st = new_st
                
            self.lines.append(new_line)
    
    def print_stations(self):
        for st in self.stations:
            print(st.name)
        
    # returns [starting station, line to, station, line to, goal station] or [starting station, line to, goal station]
    # example: route_between_stations("Helsfyr", "Økern") returns ["Helsfyr", 1,2,3,4, "Tøyen", 5, "Økern"]
    def route_between_stations(self, start_st_name, goal_st_name):
        # get station objects
        start_st = self.get_station_obj(start_st_name)
        goal_st = self.get_station_obj(goal_st_name)
        
        if not start_st or not goal_st:
            raise Exception("Invalid station")
        
        # get which lines both stations are on
        shared_lines = [i for i in start_st.lines if i in goal_st.lines] # list comprehension to find shared elements in start_st.lines and end_st.lines
        
        route = []
        
        # case 1: stations are on same line
        if len(shared_lines) >= 1:
            route.extend([start_st.name, [x.get_number() for x in shared_lines], goal_st.name])
            ## route.extend([start_st.name, shared_lines, goal_st.name])
            return route
        
        # unfinished! case 2: stations are on different lines
        def rec_find_path(current, route_so_far):
            if current == goal_st:
                return route_so_far
            
            route_so_far.append(current)
            for index, st in enumerate(current.next):
                rec_find_path(st.next[index], route_so_far)
        rec_find_path(start_st, [])
        
        return route
    
    # helper function for case 2 (transfer(s) needed) in router
    def station_nexts(self, station):
        # print("Current: " + str(station.name) + " | Possible nexts: " + str([x.name for x in station.next])) - debugging
        for st in station.next:
            self.station_nexts(st)
    
    # helper function for case 2 (transfer(s) needed) in router
    def station_prevs(self, station):
        # print("Current: " + str(station.name) + " | Possible prevs: " + str([x.name for x in station.prev])) - debugging
        for st in station.prev:
            self.station_prevs(st)
    
    def __str__(self):
        result = ""
        for line in self.lines:
            result += "Line " + str(line.get_number()) + ": "
            for st in line.get_stations():
                result += st.name + ", "
            result += "\n\n"
        return result

def main():
    net = Network()
    net.generate_network_from_file("stations.txt")
    
    # route without transfer:
    print(net.route_between_stations("Helsfyr", "Ensjø"))
    
    # route with transfer (not functioning yet):
    ## print(net.route_between_stations("Vinderen", "Blindern"))

if __name__ == "__main__":
    main()
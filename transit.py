from ctypes import Array
from queue import * # type: ignore

class Station:
    def __init__(self, name):
        self.name = name
        self.lines = []
        self.neighbors = []
    
    def add_line(self, line_obj):
        self.lines.append(line_obj)
    
    def add_neighbor(self, st):
        self.neighbors.append(st)
    
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
                
                if count == 0: # first item of each line is number of transit line. for example "1,Frognerseteren,Voksenkollen,etc."
                    new_line.set_number(item)
                    count = 1
                    continue
                
                new_st = self.get_station_obj(item) # False: station doesn't exist yet | Station obj: station with that name already exists
                if not new_st: # get_station_obj(item: String) returned False
                    new_st = Station(item)
                    new_st.add_line(new_line)
                    new_line.add_station(new_st)
                    self.stations.append(new_st)
                else: # get_station_obj(item: String) returned Station object
                    new_line.add_station(new_st)
                    new_st.add_line(new_line)
                
                if prev_st != None:
                    if new_st not in prev_st.neighbors:
                        prev_st.add_neighbor(new_st)
                    if prev_st not in new_st.neighbors:
                        new_st.add_neighbor(prev_st)
                prev_st = new_st
            self.lines.append(new_line)
    
    
    
    # reconstructs the path taken to get from start: Station to goal: Station, given came_from: Dict. returns list of Station objects.
    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        if goal not in came_from:
            return []
        
        current_line = None
        while current != start:
            path.append((current, current_line))
            current_line = [line for line in current.lines if came_from[current] in line.get_stations()][0]
            current = came_from[current]
        path.append((start, current_line))
        path.reverse()
        return path
    
    # implementation of a Breadth-first search algorithm
    def breadth_first_search(self, start_name, goal_name):
        start = self.get_station_obj(start_name)
        goal = self.get_station_obj(goal_name)
        if not start or not goal: raise Exception("Invalid station")
        
        frontier = Queue()
        frontier.put(start)
        came_from = {} # [Station, Optional[Station]]
        came_from[start] = None
        
        while not frontier.empty():
            current = frontier.get()
            
            if current == goal:
                # print("Visiting " + current.name + "\n  Found goal!")
                break
                
            # print("Visiting " + current.name + "\n  Current line(s): " + str([x.number for x in current.lines]) + "\n  Reachable stations: " + str([x.name for x in current.neighbors]))
            for next in current.neighbors:
                if next not in came_from:
                    frontier.put(next)
                    came_from[next] = current
        
        return self.reconstruct_path(came_from, start, goal)    
    
    def all_stations_on_network(self):
        return [x.name for x in self.stations]
    
    def route_interface(self):
        algorithm = self.breadth_first_search # default algorithm
        choice = int(input("Please choose a routing algorithm.\n1: Breadth-first search\n> "))
        
        match choice:
            case 1:
                algorithm = self.breadth_first_search
            case _:
                raise Exception("Invalid choice")
        
        print()
        start = input("What station are you starting at?\n> ")
        goal = input("What station are you going to?\n> ")
        path = algorithm(start, goal)
        
        print()
        print("Route from " + start + " to " + goal + ":")
        
        prev_line = None # to check if transfer had been made, with "if line != prev_line"
        count = 0 # to check if for loop is at start or goal, or not
        for station, line in path:
            count += 1
            
            if count == len(path):
                    print(station.name)
            
            if line:
                if count == 1:
                    print("  Take Line " + str(line.get_number()) + " from " + station.name + " to", end=' ')
                    
                elif prev_line and line != prev_line and count > 0:
                    print(station.name)
                    print("  Transfer to Line " + str(line.get_number()) + " and take it to", end=' ')
                    
                prev_line = line
        print()
    
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
    
    net.route_interface()

if __name__ == "__main__":
    main()
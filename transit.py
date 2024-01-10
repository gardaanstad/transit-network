from ctypes import Array


class Station:
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
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
    
    # reads file, line by line. adds station objects to new line objects, and line objects to lines array
    def generate_network_from_file(self, file_to_read):
        
        def check_if_station_exists(station_name):
            for station in self.stations:
                    if station_name == station.get_name():
                        return station
            return False
        
        network_file = open(file_to_read, 'r') # file_to_read: String = "file.txt"
        
        for row in network_file:
            row_separated = row.split(",")
            
            new_line = Line()
            
            count = 0
            for item in row_separated:
                item = item.replace('\n', '')
                
                if count == 0:
                    new_line.set_number(item)
                    count = 1
                    continue
                
                # checked_st = False means station doesn't exist yet, checked_st = Station obj means station with that name already exists
                checked_st = check_if_station_exists(item) 
                
                if not checked_st:
                    new_station = Station(item)
                    new_line.add_station(new_station)
                    self.stations.append(new_station)
                    continue
                
                # check_if_station_exists() returned Station object
                new_line.add_station(checked_st)
            self.lines.append(new_line)
    
    def print_stations(self):
        for st in self.stations:
            print(st.get_name())
    
    def __str__(self):
        result = ""
        for line in self.lines:
            result += "Line " + str(line.get_number()) + ": "
            for st in line.get_stations():
                result += st.get_name() + ", "
            result += "\n\n"
        return result

def main():
    net = Network()
    net.generate_network_from_file("stations.txt")
    print(net)
    net.print_stations()

if __name__ == "__main__":
    main()
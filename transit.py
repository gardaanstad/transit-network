import csv

class Station:
    name = ""
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
    def __str__(self):
        return self.name

class Line:
    stations = []
    number = 0
            
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
            result += str(st)
        return result

class Network:
    lines = []
    stations = []
    
    def add_line(self, line):
        self.lines.append(line)
    
    def generate_network_from_file(self, file_to_read):
        with open(file_to_read) as file_obj:
            reader = csv.reader(file_obj)
            for row in reader:
                current_line = Line()
                
                count = 0
                for item in row:
                    print("count: " + str(count) + " - item: " + item)
                    if count == 0:
                        current_line.set_number(item)
                    else:
                        for station in self.stations:
                            if station.get_name() == item:
                                current_line.add_station(station)
                                continue
                        
                        new_station = Station(item)
                        current_line.add_station(new_station)
                        self.stations.append(new_station)
                    
                    count += 1
    
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
    net.generate_network_from_file("stations.csv")
    print(net)

if __name__ == "__main__":
    main()
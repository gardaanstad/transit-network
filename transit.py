import csv

class Station:
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name

class Line:
    stations = []

    def __init__(self, nr):
        self.nr = nr
    
    def add_station(self, station):
        self.stations.append(station)
    
    def get_stations(self):
        return self.stations
    
    def get_nr(self):
        return self.nr

class Network:
    lines = []

    def __init__(self, city_name):
        self.city_name = city_name
    
    def add_line(self, line):
        self.lines.append(line)
    
    def __str__(self):
        result = ""
        for line in self.lines:
            result += "Line " + line.get_nr() + ": "
            for st in line.get_stations():
                result += st.get_name() + ", "
            result += "\n"

        return result

def generate_network(file_to_read, city_name):
    network = Network(city_name)

    with open(file_to_read) as file_obj:
        reader = csv.reader(file_obj)

        for row in reader:
            count = 0
            for item in row:
                if count == 0:
                    current_line = Line(item)
                    print(item)
                else:
                    current_station = Station(item)
                    current_line.add_station(current_station)
                
                count += 1

            network.add_line(current_line)
    
    return network

def main():
    network_oslo = generate_network("stations.csv", "Oslo")
    print(network_oslo)

if __name__ == "__main__":
    main()
from queue import * # type: ignore

class Station:
    def __init__(self, name):
        self.name = name
        self.lines = []
        self.neighbors = []
    
    def add_line(self, line):
        self.lines.append(line)
    
    def add_neighbor(self, st):
        self.neighbors.append(st)
    
    def __str__(self):
        return self.name

def get_all_stations(network):
    if not network:
        return None
    
    stations = []
    for line in network:
        for st in network[line]:
            if st not in stations:
                stations.append(st)
                
    return stations

# returns False if station with that name doesn't exist. returns Station object if station with that name is found
def get_station_obj(network, station_name):
    all_stations = get_all_stations(network)
    if not all_stations:
        return False
    
    station = [x for x in all_stations if station_name == x.name]
    
    return False if not station else station[0]

# reads file, line by line. adds station objects to network dictionary (key is line number, value is array of stations)
def generate_network_from_file(file_to_read):
    network = {}
    
    with open(file_to_read) as network_file:
        for row in network_file:
            row_separated = row.split(",")
            line = 0
            
            prev_st = None
            count = 0
            for item in row_separated:
                item = item.replace('\n', '')
                
                if count == 0: # first item of each line is number of transit line
                    line = item
                    network[line] = []
                    count = 1
                    continue
                
                new_st = get_station_obj(network, item) # False: station doesn't exist yet | Station obj: station with that name already exists
                
                if not new_st: # get_station_obj(network, item: String) returned False
                    new_st = Station(item)
                    new_st.add_line(line)
                    network[line] += [new_st]
                else: # get_station_obj(network, item: String) returned Station object
                    new_st.add_line(line)
                    network[line] += [new_st]
                
                if prev_st != None:
                    if new_st not in prev_st.neighbors:
                        prev_st.add_neighbor(new_st)
                    if prev_st not in new_st.neighbors:
                        new_st.add_neighbor(prev_st)
                prev_st = new_st   
    return network

# reconstructs the path taken to get from start: Station to goal: Station, given came_from: Dict. returns list of Station objects.
def reconstruct_path(network, came_from, start, goal):
    current = goal
    path = []
    if goal not in came_from:
        return []
    
    current_line = None
    while current != start:
        path.append((current, current_line))
        current_line = [line for line in current.lines if came_from[current] in network[line]][0]
        current = came_from[current]
    path.append((start, current_line))
    path.reverse()
    return path

# implementation of a Breadth-first search algorithm
def breadth_first_search(network, start_name, goal_name):
    start = get_station_obj(network, start_name)
    goal = get_station_obj(network, goal_name)
    if not start or not goal: raise Exception("Invalid station")
    
    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in current.neighbors:
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current
    
    return reconstruct_path(network, came_from, start, goal)

def route_interface(network):
    algorithm = breadth_first_search # default algorithm
    
    start = input("What station are you starting at?\n> ")
    goal = input("What station are you going to?\n> ")
    path = algorithm(network, start, goal)
    
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
                print("  Take Line " + str(line) + " from " + station.name + " to", end=' ')
                
            elif prev_line and line != prev_line and count > 0:
                print(station.name)
                print("  Transfer to Line " + str(line) + " and take it to", end=' ')
                
            prev_line = line
    print()

def print_network(network):
    result = ""
    for line in network:
        result += "\n\nLine " + str(line) + ": "
        i = 0
        for st in network[line]:
            if i == 0: result += st.name
            else: result += ", " + st.name
            i = 1
    print(result)

def get_neighbors(network, st_name):
    st = get_station_obj(network, st_name)
    return st if st == False else [x.name for x in st.neighbors]

def main():
    network = generate_network_from_file("stations.txt")
    route_interface(network)

if __name__ == "__main__":
    main()
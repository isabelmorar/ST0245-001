import pandas as pd
import heapq
from collections import deque

def data_structure(data):
    data["harassmentRisk"] = data["harassmentRisk"].fillna(data["harassmentRisk"].mean())
    total, nodes = list(data["origin"]), list(data["origin"].unique())
    adj_list = {k: {} for k in nodes}

    #{(origin): {destination: (length, risk)}}
    for i in range(len(total)):
        current = data.iloc[i]
        k = current["origin"]
        adj_list[k][current["destination"]] = (current["length"], current["harassmentRisk"])
        if current["oneway"]:
            y = current["destination"]
            try: 
                adj_list[y][current["origin"]] = (current["length"], current["harassmentRisk"])
            except KeyError:
                adj_list[y] = {}
                adj_list[y][current["origin"]] = (current["length"], current["harassmentRisk"])

    return adj_list


def shortest_distance(graph, starting_vertex, destination):
    distances = {v: float('infinity') for v in graph}
    prev_vertex = {v: None for v in graph}
    distances[starting_vertex], prev_vertex[starting_vertex] = 0, -1 

    priority = [(0, starting_vertex)]
    while len(priority) > 0:
        current_distance, current_vertex = heapq.heappop(priority)
        if current_vertex is destination:
           break
        for neighbor, values in graph[current_vertex].items():
            weight, risk = values
            distance = current_distance + weight
            if distance < distances[neighbor]:
                prev_vertex[neighbor], distances[neighbor] = current_vertex, distance
                heapq.heappush(priority, (distance, neighbor))

    return distances[destination], prev_vertex


def algorithm1(graph, starting_vertex, destination, max_risk):
    distances = {v: float('infinity') for v in graph}
    prev_vertex = {v: None for v in graph}
    risks = {v: None for v in graph}
    distances[starting_vertex], risks[starting_vertex] = 0, 0
    prev_vertex[starting_vertex] = -1
    
    priority = [(0, starting_vertex, 0)]
    while len(priority) > 0:
        current_distance, current_vertex, current_sum1 = heapq.heappop(priority)
        if current_vertex is destination:
            break
        for neighbor, values in graph[current_vertex].items():
            weight, risk = values
            distance = current_distance + weight
                
            if distance < distances[neighbor]:
                sum1 = current_sum1 + (weight*risk)
                av_risk = sum1/distance 
                if av_risk <= max_risk: 
                    prev_vertex[neighbor] = current_vertex
                    distances[neighbor], risks[neighbor] = distance, av_risk
                    heapq.heappush(priority, (distance, neighbor, sum1))
                    
    return distances[destination], prev_vertex, risks[destination]


def lowest_risk(graph, starting_vertex, destination):
    risks = {v: float('infinity') for v in graph}
    prev_vertex = {v: None for v in graph}
    risks[starting_vertex], prev_vertex[starting_vertex] = 0, -1
    
    visited = deque([starting_vertex])
    priority = [(0, starting_vertex, 0)]
    while len(priority) > 0:
        current_distance, current_vertex, current_sum1 = heapq.heappop(priority)
        if current_vertex is destination:
           break
        for neighbor, values in graph[current_vertex].items():
            if neighbor not in visited:
                weight, risk = values
                distance = current_distance + weight
                sum1 = current_sum1 + (weight*risk)
                av_risk = sum1/distance 
                
                if av_risk < risks[neighbor]: 
                    prev_vertex[neighbor], risks[neighbor] = current_vertex, av_risk
                    heapq.heappush(priority, (distance, neighbor, sum1))
                    visited.append(neighbor)
                    
    return risks[destination], prev_vertex


def algorithm2(graph, starting_vertex, destination, max_distance):
    distances = {v: None for v in graph}
    prev_vertex = {v: None for v in graph}
    risks = {v: 1 for v in graph}
    distances[starting_vertex], risks[starting_vertex] = 0, 0
    prev_vertex[starting_vertex] = -1

    visited = deque([starting_vertex])
    priority = [(0, starting_vertex, 0)]
    while len(priority) > 0:
        current_distance, current_vertex, current_sum1 = heapq.heappop(priority)
        if current_vertex is destination:
            break
        for neighbor, values in graph[current_vertex].items():
            if neighbor not in visited: 
                weight, risk = values
                distance = current_distance + weight
                sum1 = current_sum1 + (weight*risk)
                av_risk = sum1/distance
                
                if av_risk < risks[neighbor]:
                    if distance <= max_distance:
                        prev_vertex[neighbor] = current_vertex
                        distances[neighbor], risks[neighbor] = distance, av_risk
                        heapq.heappush(priority, (distance, neighbor, sum1))
                        visited.append(neighbor)
                   
    return distances[destination], prev_vertex, risks[destination]
    

def path(previous, i, result):
    if previous[i] == -1:
        return result
    result.append(previous[i])
    return path(previous, previous[i], result)


def main():
    data = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=";")
    adj_list = data_structure(data)
    origin = input("Enter origin coordinates: ")
    destination = input("Enter destination coordinates: ")
    max_risk = float(input("Enter maximum risk wanted on path: "))
    max_distance = float(input("Enter maximum distance wanted on path: "))
    print("\n-----")
    
    #Execution algorithm1 + shortest path 
    distance_shortest, prev_shortest = shortest_distance(adj_list, origin, destination)
    distance_algorithm1, prev_algorithm1, risk_algorithm1 = algorithm1(adj_list, origin, destination, max_risk)
    
    print("\nShortest path from {} to {}: ".format(origin, destination), "\n")
    path1 = path(prev_shortest, destination, deque([destination]))
    while len(path1) != 0:
        print(path1.pop(),"->", end=" ")
    print("\n\nTotal Distance:", round(distance_shortest,3))
  
    print("\n\nShortest path from {} to {} without exceeding risk of {}: ".format(origin, destination, max_risk), "\n")
    try: 
        path2 = path(prev_algorithm1, destination, deque([destination]))
        while len(path2) != 0:
            print(path2.pop(),"->", end=" ")
        print("\n\nTotal Distance:", round(distance_algorithm1,3))
        print("Average Weighted Risk:", round(risk_algorithm1,3))
    except KeyError:
        print("No path with given conditions")
    print("\n-----")
    
    #Execution algorithm2 + path with lowest risk
    risk_lowest, prev_lowest = lowest_risk(adj_list, origin, destination)
    distance_algorithm2, prev_algorithm2, risk_algorithm2 = algorithm2(adj_list, origin, destination, max_distance)
    
    print("\nPath with lowest risk from {} to {}: ".format(origin, destination), "\n")
    path3 = path(prev_lowest, destination, deque([destination]))
    while len(path3) != 0:
        print(path3.pop(),"->", end=" ")
    print("\n\nAverage Weighted Risk:", round(risk_lowest,3))

    print("\n\nPath with lowest risk from {} to {} without exceeding distance of {} meters: ".format(origin, destination, max_distance), "\n")
    try: 
        path4 = path(prev_algorithm2, destination, deque([destination]))
        while len(path4) != 0:
            print(path4.pop(),"->", end=" ")
        print("\n\nTotal Distance:", round(distance_algorithm2,3))
        print("Average Weighted Risk:", round(risk_algorithm2,3))
    except KeyError:
        print("No path with given conditions")

main()
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
    distances[starting_vertex] = 0
    prev_vertex[starting_vertex] = -1

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
    distances[starting_vertex] = 0
    prev_vertex[starting_vertex] = -1
    risks[starting_vertex] = 0

    priority = [(0, starting_vertex, 0)]
    while len(priority) > 0:
        current_distance, current_vertex, current_risk = heapq.heappop(priority)
        if current_vertex is destination:
           break
       
        for neighbor, values in graph[current_vertex].items():
            weight, risk = values
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                temp = prev_vertex[neighbor]
                prev_vertex[neighbor] = current_vertex
                current_path = path(prev_vertex, neighbor, deque([neighbor]))
                sum1, sum2 = 0, 0
                while len(current_path) > 1:
                    if len(current_path) == 3:
                        one, two, three = current_path.pop(), current_path.pop(), current_path.pop()
                        dist1, risk1 = graph[one][two]
                        dist2, risk2 = graph[two][three]
                        sum1 += (risk1*dist1 + risk2*dist2)
                        sum2 += (dist1 + dist2)
                    else:
                        dist, riesgo = graph[current_path.pop()][current_path.pop()]
                        sum1 += riesgo*dist
                        sum2 += dist
                    
                av_risk = sum1/sum2
                if av_risk <= max_risk:
                    distances[neighbor], risks[neighbor] = distance, av_risk
                    heapq.heappush(priority, (distance, neighbor, av_risk))
                else:
                    prev_vertex[neighbor] = temp 

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
    max_risk = float(input("Enter maximum risk desired along path: "))
    print("\n")
    computed_distance, prev_vertex, computed_risk = algorithm1(adj_list, origin, destination, max_risk)
    min_distance, prev_vertex2 = shortest_distance(adj_list, origin, destination)
    
    print("\nShortest path from {} to {} without exceeding risk of {}: ".format(origin, destination, max_risk), "\n")
    try: 
        path1 = path(prev_vertex, destination, deque([destination]))
        while len(path1) != 0:
            print(path1.pop(),"->", end=" ")
        print("\n\nTotal Distance:", computed_distance)
        print("Average Weighted Risk:", computed_risk)
    except KeyError:
        print("No path with given conditions")
    
    path2 = path(prev_vertex2, destination, deque([destination]))
    print("Shortest path from {} to {}: ".format(origin, destination), "\n")
    while len(path2) != 0:
        print(path2.pop(),"->", end=" ")
    print("\n\nTotal Distance:", min_distance)
    print("")
    

main()








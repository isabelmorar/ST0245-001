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
        current_distance, current_vertex, current_sum1 = heapq.heappop(priority)

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
    risks[starting_vertex] = 0
    prev_vertex[starting_vertex] = -1
    
    priority = [(0, starting_vertex, 0)]
    while len(priority) > 0:
        current_distance, current_vertex, current_sum1 = heapq.heappop(priority)
        if current_vertex is destination:
           break
        for neighbor, values in graph[current_vertex].items():
            weight, risk = values
            distance = current_distance + weight
            sum1 = current_sum1 + (weight*risk)
            av_risk = sum1/distance 
            
            if av_risk < risks[neighbor]: 
                prev_vertex[neighbor] = current_vertex
                risks[neighbor] = av_risk
                heapq.heappush(priority, (distance, neighbor, sum1))
                    
    return risks[destination], prev_vertex


def path(previous, i, result):
    if previous[i] == -1:
        return result
    result.append(previous[i])
    return path(previous, previous[i], result)


def main():
    sample = {"A": {"C": (5, 0.2), "D": (11, 0.4)}, "B": {"C":(7,0.32), "E": (14,0.41)}, "C": {"B": (7,0.32), "A": (5,0.2)}, "D": {"A": (11,0.4), "E": (8,1.5)}, "E": {"B": (14,0.41), "D": (8,1.5)}}
    
    data = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=";")
    adj_list = data_structure(data)
    trial = sample
    
    origin = "A"
    destination = "E"
    max_risk = 0.8
    #computed_distance, prev_vertex, computed_risk = algorithm1(trial, origin, destination, max_risk)
    #computed_distance, prev_vertex = shortest_distance(trial, origin, destination)
    computed_risk, prev_vertex = lowest_risk(trial, origin, destination)


    try: 
        camino = path(prev_vertex, destination, deque([destination]))
        print("Shortest path from {} to {}: ".format(origin, destination), "\n")
        while len(camino) != 0:
            print(camino.pop(),"->", end=" ")
        #print("\n\nTotal Distance: {} meters".format(round(computed_distance,3)))
        print("Average Risk:", round(computed_risk,3))
    
    except KeyError:
        print("No path with given conditions")

main()
import pandas as pd
import heapq

def data_structure(data):
    data["harassmentRisk"] = data["harassmentRisk"].fillna(0)
    total = list(data["origin"])
    nodes = list(data["origin"].unique())

    adj_list = {k: {} for k in nodes}

    #{(origin): {destination: (lenght, risk)}}
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
    anteriores = {v: None for v in graph}
    distances[starting_vertex] = 0
    anteriores[starting_vertex] = -1

    priority = [(0, starting_vertex)]
    while len(priority) > 0:
        current_distance, current_vertex = heapq.heappop(priority)
        if current_vertex is destination:
           break
       
        for neighbor, values in graph[current_vertex].items():
            weight, risk = values
            distance = current_distance + weight
            previous = current_vertex
            
            if distance < distances[neighbor]:
                anteriores[neighbor] = previous
                distances[neighbor] = distance
                heapq.heappush(priority, (distance, neighbor))

    return distances, anteriores


def lowest_risk(graph, starting_vertex, destination):
    anteriores = {v: None for v in graph}
    risks = {v: float('infinity') for v in graph}
    anteriores[starting_vertex] = -1
    risks[starting_vertex] = 0

    priority = [(starting_vertex, 0)]
    while len(priority) > 0:
        current_vertex, avg_risk = heapq.heappop(priority)
        if current_vertex is destination:
           break
       
        for neighbor, values in graph[current_vertex].items():
            weight, risk = values
            previous = current_vertex
            temp = anteriores[neighbor]
            
            if anteriores[current_vertex] is not neighbor:
                anteriores[neighbor] = previous
                current_path = path(anteriores, neighbor,[neighbor])   
                
                sum1, sum2 = 0, 0
                for i in range(len(current_path)-1):
                    dist, riesgo = graph[current_path[i]][current_path[i+1]]
                    sum1 += riesgo*dist
                    sum2 += dist
                    
                av_risk = sum1/sum2
                if av_risk < risks[neighbor]:
                    risks[neighbor] = av_risk
                    heapq.heappush(priority, (neighbor, risk))
                else:
                    anteriores[neighbor] = temp 

    return anteriores, risks


def algorithm1(graph, starting_vertex, destination, max_risk):
    distances = {v: float('infinity') for v in graph}
    anteriores = {v: None for v in graph}
    risks = {v: None for v in graph}
    distances[starting_vertex] = 0
    anteriores[starting_vertex] = -1
    risks[starting_vertex] = 0

    priority = [(0, starting_vertex, 0)]
    while len(priority) > 0:
        current_distance, current_vertex, avg_risk = heapq.heappop(priority)
        if current_vertex is destination:
           break
       
        for neighbor, values in graph[current_vertex].items():
            weight, risk = values
            distance = current_distance + weight
            previous = current_vertex
            
            if distance < distances[neighbor]:
                temp = anteriores[neighbor]
                anteriores[neighbor] = previous
                current_path = path(anteriores, neighbor,[neighbor])
                
                sum1, sum2 = 0, 0
                for i in range(len(current_path)-1):
                    dist, riesgo = graph[current_path[i]][current_path[i+1]]
                    sum1 += riesgo*dist
                    sum2 += dist
                
                av_risk = sum1/sum2
                if av_risk <= max_risk:
                    distances[neighbor] = distance
                    risks[neighbor] = av_risk
                    heapq.heappush(priority, (distance, neighbor, risk))
                else:
                    anteriores[neighbor] = temp 

    return distances, anteriores, risks


def path(previous, i, result):
   if previous[i] == -1:
       return result
   result.append(previous[i])
   return path(previous, previous[i], result)


def main():
    sample = {"A": {"C": (5, 0.2), "D": (11, 0.4)}, "B": {"C":(7,0.32), "E": (14,0.41)}, "C": {"B": (7,0.32), "A": (5,0.2)}, "D": {"A": (11,0.4), "E": (8,1.5)}, "E": {"B": (14,0.41), "D": (8,1.5)}}

    data = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=";")
    adj_list = data_structure(data)
                         
    origin = "A"
    destination = "B"
    distances, anteriores, risks = algorithm1(sample, origin, destination, 0.5)
    #distances, anteriores = shortest_distance(adj_list, origin, destination)
    #anteriores, risks = lowest_risk(adj_list, origin, destination)
    
    try: 
        camino = path(anteriores, destination, [destination])
        print("Shortest path from {} to {}: ".format(destination, origin))
        for i in range(len(camino)-1, -1,-1):
            print(camino[i], "->", end=" ")
        print(" ")
        #print("Total Distance:", distances[destination])
        print("Average Risk:", risks[destination])
    except KeyError:
        print("No path with given conditions")

main()








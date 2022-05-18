import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely import wkt
from collections import deque
from ConstrainedShortestPath import data_structure, path, algorithm2, algorithm1, shortest_distance, lowest_risk

#Load area and edges
area = pd.read_csv('poligono_de_medellin.csv',sep=';')
area['geometry'] = area['geometry'].apply(wkt.loads)
area = gpd.GeoDataFrame(area)

data = pd.read_csv("calles_de_medellin_con_acoso.csv",sep=';')
data['geometry'] = data['geometry'].apply(wkt.loads)
edges = gpd.GeoDataFrame(data)

#Algortihm Execution
adj_list = data_structure(data)
origin = input("Enter origin coordinates: ")
destination = input("Enter destination coordinates: ")
max_risk = float(input("Enter max risk wanted on path: "))
max_distance = float(input("Enter max distance wanted on path: "))

#Plot Origin and Destination
latitude1, longitude1 = origin[1:-1].split(", ")
latitude2, longitude2 = destination[1:-1].split(", ")
origin_coordinates = gpd.points_from_xy([float(latitude1)], [float(longitude1)])
destination_coordinates = gpd.points_from_xy([float(latitude2)], [float(longitude2)])
new1, new2 = gpd.GeoSeries(origin_coordinates), gpd.GeoSeries(destination_coordinates)    

#Compute the first 2 paths 
distance_algorithm1, prev_algorithm1, risk_algorithm1 = algorithm1(adj_list, origin, destination, max_risk)
distance_shortest, prev_shortest, risk_shortest = algorithm1(adj_list, origin, destination,1)

print("\n\n** Origin shown in red and destination shown in yellow **\n")
print("Shortest path (red) - ")
print("Total Distance: {} meters".format(round(distance_shortest,3)))
print("Average Risk:", round(risk_shortest,3))
path1 = path(prev_shortest, destination, deque([destination]))
path1.reverse()
path1_origins, path1_destinations = list(path1), list(path1)
path1_origins.pop()
path1_destinations.pop(0)

try: 
    print("\nShortest path without exceeding risk of {} (white) - ".format(max_risk))
    print("Total Distance: {} meters".format(round(distance_algorithm1,3)))
    print("Average Risk:", round(risk_algorithm1,3))
    path2 = path(prev_algorithm1, destination, deque([destination]))
    path2.reverse()
    path2_origins, path2_destinations = list(path2), list(path2)
    path2_origins.pop()
    path2_destinations.pop(0)
except KeyError:
    print("No path without exceeding risk of {}".format(max_risk))
    path2_origins = []

#Plot 1
fig, ax = plt.subplots(figsize=(12,8))
area.plot(ax=ax, facecolor='black')
edges.plot(ax=ax, linewidth=0.3, column='harassmentRisk', legend=True, missing_kwds={'color': 'dimgray'})
new1.plot(ax=ax, linewidth=5, color='red')
new2.plot(ax=ax, linewidth=5, color='yellow')

for i in range(len(path1_origins)):
    current = data[(data["origin"] == path1_origins[i]) & (data["destination"] == path1_destinations[i])]
    geometry = gpd.GeoSeries(current["geometry"])
    if geometry.empty:
        continue 
    geometry.plot(ax=ax, linewidth = 2, edgecolor='red')

for i in range(len(path2_origins)):
    current = data[(data["origin"] == path2_origins[i]) & (data["destination"] == path2_destinations[i])]
    geometry = gpd.GeoSeries(current["geometry"])
    if geometry.empty:
        continue 
    geometry.plot(ax=ax, linewidth = 2, edgecolor='white')         

plt.title("Riesgo de acoso en las calles de Medellín")
plt.tight_layout()
plt.savefig("mapa-riesgo-de-acoso.png")


#Compute the other 2 paths 
risk_lowest, prev_lowest, = lowest_risk(adj_list, origin, destination)
distance_algorithm2, prev_algorithm2, risk_algorithm2 = algorithm2(adj_list, origin, destination, max_distance)

print("\n\n** Origin shown in red and destination shown in yellow **\n")
print("Path with lowest risk (yellow) - ")
print("Average Risk:", round(risk_lowest,3))
path3 = path(prev_lowest, destination, deque([destination]))
path3.reverse()
path3_origins, path3_destinations = list(path3), list(path3)
path3_origins.pop()
path3_destinations.pop(0)

try: 
    print("\nPath with lowest risk without excedding distance of {} meters (white) - ".format(max_distance))
    print("Total Distance: {} meters".format(round(distance_algorithm2,3)))
    print("Average Risk:", round(risk_algorithm2,3))
    path4 = path(prev_algorithm2, destination, deque([destination]))
    path4.reverse()
    path4_origins, path4_destinations = list(path4), list(path4)
    path4_origins.pop()
    path4_destinations.pop(0)
except KeyError:
    print("No path without exceeding distance of {} meters".format(max_distance))
    path4_origins = []

#Plot 2
fig, ax = plt.subplots(figsize=(12,8))
area.plot(ax=ax, facecolor='black')
edges.plot(ax=ax, linewidth=0.3, column='length', legend=True, missing_kwds={'color': 'dimgray'})
new1.plot(ax=ax, linewidth=5, color='red')
new2.plot(ax=ax, linewidth=5, color='yellow')

for i in range(len(path3_origins)):
    current = data[(data["origin"] == path3_origins[i]) & (data["destination"] == path3_destinations[i])]
    geometry = gpd.GeoSeries(current["geometry"])
    if geometry.empty:
        continue 
    geometry.plot(ax=ax, linewidth = 2, edgecolor='yellow')

for i in range(len(path4_origins)):
    current = data[(data["origin"] == path4_origins[i]) & (data["destination"] == path4_destinations[i])]
    geometry = gpd.GeoSeries(current["geometry"])
    if geometry.empty:
        continue 
    geometry.plot(ax=ax, linewidth = 2, edgecolor='white')

plt.title("Longitud en metros de las calles de Medellín")
plt.tight_layout()
plt.savefig("mapa-de-called-con-longitud.png")
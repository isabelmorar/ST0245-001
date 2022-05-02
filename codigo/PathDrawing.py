import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely import wkt
from collections import deque
from ConstrainedShortestPath import data_structure, algorithm1, path

#Load area and edges
area = pd.read_csv('poligono_de_medellin.csv',sep=';')
area['geometry'] = area['geometry'].apply(wkt.loads)
area = gpd.GeoDataFrame(area)

data = pd.read_csv("calles_de_medellin_con_acoso.csv",sep=';')
data['geometry'] = data['geometry'].apply(wkt.loads)
edges = gpd.GeoDataFrame(data)


#Geometries for calculated path
total = list(data["origin"])
geometries = {}
for i in range(len(total)):
    current = data.iloc[i]
    k, m = (current["origin"], current["destination"]), (current["destination"],current["origin"])
    geometries[k], geometries[m] = current["geometry"], current["geometry"]

def computed_geometries(computed_path):
    path_geometries = deque()
    while len(computed_path) > 1:
        if len(computed_path) == 3:
            one, two, three = computed_path.pop(), computed_path.pop(), computed_path.pop()
            path_geometries.append(geometries[(one,two)])
            path_geometries.append(geometries[(two,three)])
        else:
            path_geometries.append(geometries[(computed_path.pop(), computed_path.pop())])
    return path_geometries 

adj_list = data_structure(data)
origin = input("Enter origin coordinates: ")
destination = input("Enter destination coordinates: ")
max_risk = float(input("Enter max risk wanted on path: "))
computed_distance, prev_vertex, computed_risk = algorithm1(adj_list, origin, destination, max_risk)
try: 
    computed_path = path(prev_vertex, destination, deque([destination]))
    path_geometries = computed_geometries(computed_path)
    print("\nShortest path from {} to {}: ".format(origin, destination), "\n")
    print("Total Distance: {} meters".format(round(computed_distance,3)))
    print("Average Risk:", round(computed_risk,3))
except KeyError:
    print("No path with given conditions")
    path_geometries = deque()

current_geometries = gpd.GeoSeries(list(path_geometries))


#Plot 1
fig, ax = plt.subplots(figsize=(12,8))
area.plot(ax=ax, facecolor='black')
edges.plot(ax=ax, linewidth=0.3, column='harassmentRisk', legend=True, missing_kwds={'color': 'dimgray'})
current_geometries.plot(ax = ax, linewidth=8, edgecolor='black')

plt.title("Riesgo de acoso en las calles de Medellín")
plt.tight_layout()
plt.savefig("mapa-riesgo-de-acoso.png")

#Plot 2
fig, ax = plt.subplots(figsize=(12,8))
area.plot(ax=ax, facecolor='black')
edges.plot(ax=ax, linewidth=0.3, column='length', legend=True, missing_kwds={'color': 'dimgray'})
current_geometries.plot(ax = ax, linewidth=8, edgecolor='black')

plt.title("Longitud en metros de las calles de Medellín")
plt.tight_layout()
plt.savefig("mapa-de-called-con-longitud.png")
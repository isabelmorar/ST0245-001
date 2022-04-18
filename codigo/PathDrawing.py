import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely import wkt

#Load area
area = pd.read_csv('poligono_de_medellin.csv',sep=';')
area['geometry'] = area['geometry'].apply(wkt.loads)
area = gpd.GeoDataFrame(area)

#Load streets
edges = pd.read_csv('calles_de_medellin_con_acoso.csv',sep=';')
edges['geometry'] = edges['geometry'].apply(wkt.loads)
edges = gpd.GeoDataFrame(edges)


#Plot 1
fig, ax = plt.subplots(figsize=(12,8))
area.plot(ax=ax, facecolor='black')
edges.plot(ax=ax, linewidth=0.3, column='harassmentRisk', legend=True, missing_kwds={'color': 'dimgray'})

plt.title("Riesgo de acoso en las calles de Medellín")
plt.tight_layout()
plt.savefig("mapa-riesgo-de-acoso.png")

#Plot 2
fig, ax = plt.subplots(figsize=(12,8))
area.plot(ax=ax, facecolor='black')
edges.plot(ax=ax, linewidth=0.3, column='length', legend=True, missing_kwds={'color': 'dimgray'})

plt.title("Longitud en metros de las calles de Medellín")
plt.tight_layout()
plt.savefig("mapa-de-called-con-longitud.png")
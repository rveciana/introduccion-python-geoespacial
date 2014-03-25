# -*- coding: utf-8 -*-
"""
8as Jornadas Sig Libre 
26 de Marzo de 2014
Introducción a Python para usos geoespaciales

Ejemplos para trabajar con archivos vectoriales usando fiona
"""

#Usando fiona para leer un fichero:

import fiona

c = fiona.open('data/llamps.shp')

print c
# <demo> --- stop ---


#Se puede saber el driver OGR usado con la propiedad:
print c.driver
# <demo> --- stop ---

#Y la proyección:
print c.crs

# <demo> --- stop ---

#El schema indica las otras propiedades del archivo:
print c.schema
# <demo> --- stop ---

#Para ver los registros, podemos usar el iterador:
print c.next()
# <demo> --- stop ---

#Podemos iterar todos los elementos usando
for record in c:
    print record['properties']['Data i hor']
# <demo> --- stop ---

#Podemos filtrar los datos para una bounding box de manera muy sencilla:

filtered_data = c.filter(bbox=(2.0, 40.8, 2.1, 40.9))
for record in filtered_data:
    print record
#El archivo se puede cerrar usando:
c.close()
# <demo> --- stop ---

#Escritura de archivos vectoriales:

#Para crear un archivo, 

crs = {u'no_defs': True, u'datum': u'WGS84', u'proj': u'longlat'}
driver = 'ESRI Shapefile'
schema = {'geometry': 'Point', 'properties': [('nombre', 'str'), ('valor', 'str')]}
of = fiona.open('test.shp','w', driver = driver, crs=crs, schema=schema)
# <demo> --- stop ---


#Se pueden añadir registros a los archivos existentes de la siguiente forma:
rec = {'geometry': {'type': 'Point', 'coordinates': (1.8890812, 40.889)}, 'type': 'Feature', 'id': '0', 'properties': {'nombre': 'punto1', 'valor': 'valor1'}}

of.write(rec)

# <demo> --- stop ---

#Operaciones con geometrías usando shapely

#Para transformar los datos leídos con fiona al objeto shapely, usamos shape:

from shapely.geometry import shape
import fiona
c = fiona.open('data/llamps.shp')
for point in c:
    print shape(point['geometry'])
# <demo> --- stop ---

#Una vez se tiene como objeto shape, se puede operar sobre las geometrías.

for point in c:
    print shape(point['geometry']).buffer(1)   

#La operación inversa, para guardar las geometrías con fiona, es mapping
# <demo> --- stop ---
#Distancia entre dos puntos
a = {'type': 'Point', 'coordinates': ((1, 40))}
b = {'type': 'Point', 'coordinates': ((0.5, 40))}
print shape(a).distance(shape(b))

# <demo> --- stop ---
#Intersección de dos LineString

a = {'type': 'LineString', 'coordinates': ((1, 40),(2,41))}
b = {'type': 'LineString', 'coordinates': ((0.5, 40),(2.5,41))}
print shape(a).crosses(shape(b))
print shape(a).intersection(shape(b))

# <demo> --- stop ---
#Un ejemplo un poco más complicado: Determinar cuantos rayos han caído en cada comarca

from shapely.geometry import shape
import fiona
comarcas = fiona.open('data/comarcas.shp')
rayos = fiona.open('data/llamps.shp')
informe = {}
for comarca in comarcas:
    nombre_comarca = comarca['properties']['nombre']
    codigo_comarca = comarca['properties']['codigo']
    informe[codigo_comarca] = {'nombre': nombre_comarca, 'numero_rayos': 0}
    shape_comarca = shape(comarca['geometry'])
    rayos_bbox = rayos.filter(bbox=shape_comarca.bounds)
    for rayo in rayos_bbox:
        if shape(rayo['geometry']).within(shape_comarca):
            informe[codigo_comarca]['numero_rayos'] += 1  

print informe
rayos.close()
comarcas.close()
# <demo> --- stop ---


#Representación de los datos

from osgeo import gdal
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import fiona
import numpy


m = Basemap(width = 272257.508, \
        height = 269254.668, \
        resolution = 'h', \
        projection = 'tmerc', \
        lon_0 = 1.727858333, \
        lat_0 = 41.715877778)
# <demo> --- stop ---

x = numpy.linspace(0, 272257.508, 272)
y = numpy.linspace(269254.668, 0, 269)

xx, yy = numpy.meshgrid(x, y)

m.drawmapboundary(fill_color=(0.8,0.8,1))
m.fillcontinents(color='beige', zorder=0)

c = fiona.open('data/llamps.shp')
for point in c:
    xp, yp = m(point['geometry']['coordinates'][0],point['geometry']['coordinates'][1])
    m.plot(xp, yp,'bo')

plt.show()

# <demo> --- stop ---

# -*- coding: utf-8 -*-
"""
8as Jornadas Sig Libre 
26 de Marzo de 2014
Introduction to Python for geospatial uses

Examples for using fiona to work with vectorial files
"""

#Using fiona to read a file:

import fiona

c = fiona.open('data/llamps.shp')

print c
# <demo> --- stop ---


#It's possible to get the OGR driver name with the property:
print c.driver
# <demo> --- stop ---

#And the projection:
print c.crs

# <demo> --- stop ---

#The schema indicates the other file properties:
print c.schema
# <demo> --- stop ---

#To see the record, it's possible to use the iterators:
print c.next()
# <demo> --- stop ---

#It's possible to iterate all the elements using
for record in c:
    print record['properties']['Data i hor']
# <demo> --- stop ---

#It's possible to filter the data for a bounding box in a very simple way:
filtered_data = c.filter(bbox=(2.0, 40.8, 2.1, 40.9))
for record in filtered_data:
    print record

#To close the file, use:
c.close()
# <demo> --- stop ---

#Vectorial files writting:

#To create a file:
crs = {u'no_defs': True, u'datum': u'WGS84', u'proj': u'longlat'}
driver = 'ESRI Shapefile'
schema = {'geometry': 'Point', 'properties': [('nombre', 'str'), ('valor', 'str')]}
of = fiona.open('test.shp','w', driver = driver, crs=crs, schema=schema)
# <demo> --- stop ---

#It's possible to add records to the existing files using:
rec = {'geometry': {'type': 'Point', 'coordinates': (1.8890812, 40.889)}, 'type': 'Feature', 'id': '0', 'properties': {'nombre': 'punto1', 'valor': 'valor1'}}

of.write(rec)

# <demo> --- stop ---

#Operations with geometries using shapely

#To transform the read data with fiona into a shapely object, we use shape:
from shapely.geometry import shape
import fiona
c = fiona.open('data/llamps.shp')
for point in c:
    print shape(point['geometry'])
# <demo> --- stop ---

#Once the object is a shape object, it's possible to operate on the geometries
for point in c:
    print shape(point['geometry']).buffer(1)   

#And the inverse operation, to save the geometries with fiona, is mapping
# <demo> --- stop ---
#Distance between two points
a = {'type': 'Point', 'coordinates': ((1, 40))}
b = {'type': 'Point', 'coordinates': ((0.5, 40))}
print shape(a).distance(shape(b))

# <demo> --- stop ---

#Two LineString intersection
a = {'type': 'LineString', 'coordinates': ((1, 40),(2,41))}
b = {'type': 'LineString', 'coordinates': ((0.5, 40),(2.5,41))}
print shape(a).crosses(shape(b))
print shape(a).intersection(shape(b))

# <demo> --- stop ---
#A more complicated example: Calculate how many lighnings have fallen in each comarca
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

#Data representation

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

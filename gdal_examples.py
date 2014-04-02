# -*- coding: utf-8 -*-
"""
8as Jornadas Sig Libre 
26 de Marzo de 2014
Introduction to Python for geospatial uses

Examples for using GDAL/python to work with vectorial files

"""


#To work with this example, we will need the modules:

from osgeo import gdal
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy

#How to open a dataset
ds = gdal.Open('data/XXX_RN1_20131117_0000_CMPAC1C_1h.tif')
# <demo> --- stop ---
# <demo> auto

#Get all the possible methods (quit using the q key):
help(ds)
# <demo> --- stop ---

"""
Reading the metadata:

"""
#Projection:
print ds.GetProjection()
# <demo> --- stop ---

#Geotransform
print ds.GetGeoTransform()
# <demo> --- stop ---


#To read the bands data:
#All at once

data = ds.ReadAsArray()

print data
# <demo> --- stop ---

#Only one band:
band = ds.GetRasterBand(1)
data = band.ReadAsArray()

print data

# <demo> --- stop ---

#Drawing the band using basemap
m = Basemap(width = 272257.508, \
        height = 269254.668, \
        resolution = 'h', \
        projection = 'tmerc', \
        lon_0 = 1.727858333, \
        lat_0 = 41.715877778)

#The equivalent to geotransform. Starting with 0 and finishing with 272257.508, we want 272 elements
x = numpy.linspace(0, 272257.508, 272)
y = numpy.linspace(269254.668, 0, 269)

#A matrix with the x and y values is created, to pass it to Basemap
xx, yy = numpy.meshgrid(x, y)

#contourf draws the colored isolines
cs = m.contourf(xx,yy,data)

plt.show()

# <demo> --- stop ---

#The map can be more complicated

#Starting from 0.1 and finishing with 25, paint a color each 3 acumulated liters.
m.contourf(xx,yy,data,numpy.arange(0.1,25,3))

#Drawing the land and sea zones as the map background
m.drawmapboundary(fill_color=(0.8,0.8,1))
m.fillcontinents(color='beige', zorder=0)

#Drawing the comarques
#The file comarcas.shp will be opened, but the file extension must be removed from the parameter
m.readshapefile('data/comarcas', 'comarcas')

#And finally, the title and legend
cbar = m.colorbar(cs,location='bottom',pad="5%")
cbar.set_label(u'precipitación (mm)')

plt.show()
# <demo> --- stop ---

#Raster calculations

#Opening another raster to play with the data
ds2 = gdal.Open('data/XXX_RN1_20131117_0100_CMPAC1C_1h.tif')
data2 = ds2.ReadAsArray()

#Summing two mateixes with numpy is easy
suma = data + data2

m.contourf(xx,yy,suma,numpy.arange(0.1,35,3))
m.drawmapboundary(fill_color=(0.8,0.8,1))
m.fillcontinents(color='beige', zorder=0)

m.readshapefile('data/comarcas', 'comarcas')

plt.show()

# <demo> --- stop ---

#Zones wih more than 6 liters of rain at 00 hours (the first opened file)
data_condicion = (data > 6)
cs = m.pcolormesh(xx,yy,data_condicion)
plt.show()

# <demo> --- stop ---

#Zones where it didn't rain at 00 and it did at 01 hours
data_condicion = (data < 0.1) * (data2 > 0.1)
cs = m.pcolormesh(xx,yy,data_condicion)
plt.show()

# <demo> --- stop ---

#Zones where it rained all the day

from osgeo import gdal
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy

m = Basemap(width = 272257.508, \
        height = 269254.668, \
        resolution = 'h', \
        projection = 'tmerc', \
        lon_0 = 1.727858333, \
        lat_0 = 41.715877778)

x = numpy.linspace(0, 272257.508, 272)
y = numpy.linspace(269254.668, 0, 269)

xx, yy = numpy.meshgrid(x, y)

# <demo> --- stop ---

#For each hour, the file is opened
horas_lluvia = None
for i in range(0,10):
    ds = gdal.Open('data/XXX_RN1_20131117_%02d00_CMPAC1C_1h.tif'%i)
    datos_hora = ds.ReadAsArray()
    #El valor del píxel será 1 si datos_hora tiene un valor > 0.1 (False * 1 = 0 y True * 1 = 1)
    zonas_lluvia = 1 * (datos_hora > 0.1)
    if horas_lluvia == None:
        horas_lluvia = zonas_lluvia
    else:
        horas_lluvia = horas_lluvia + zonas_lluvia

# <demo> --- stop ---

#Drawing the number of raining hours is very similar to the previous example
cs = m.pcolormesh(xx,yy,horas_lluvia)
m.drawmapboundary(fill_color=(0.8,0.8,1))
m.fillcontinents(color='beige', zorder=0)
m.readshapefile('data/comarcas', 'comarcas')
cbar = m.colorbar(cs,location='bottom',pad="5%")
cbar.set_label(u'horas de lluvia')

plt.figure()
# <demo> --- stop ---

#Drawing only the zones where the value is 10 (it rained in every image) is quite simple as well
cs = m.pcolormesh(xx,yy,horas_lluvia == 10)
m.drawmapboundary(fill_color=(0.8,0.8,1))
m.fillcontinents(color='beige', zorder=0)
m.readshapefile('data/comarcas', 'comarcas')
cbar = m.colorbar(cs,location='bottom',pad="5%")
cbar.set_label(u'horas de lluvia')
plt.show()
# <demo> --- stop ---

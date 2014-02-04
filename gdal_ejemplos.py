# -*- coding: utf-8 -*-
"""
8as Jornadas Sig Libre 
26 de Marzo de 2014
Introducción a Python para usos geoespaciales

Ejemplos para trabajar con GDAL/python
"""



#Para este ejemplo, necesitaremos los siguientes módulos:

from osgeo import gdal
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy


#Como abrir un dataset
ds = gdal.Open('data/XXX_RN1_20131117_0000_CMPAC1C_1h.tif')
# <demo> --- stop ---
# <demo> auto

#Todos los métodos posibles (salir usando la tecla q):
help(ds)
# <demo> --- stop ---

"""
Leer los metadatos:

"""
#Proyección:
print ds.GetProjection()
# <demo> --- stop ---

#Geotransform
print ds.GetGeoTransform()
# <demo> --- stop ---


#Para leer los datos de las bandas:
#Todas a la vez

data = ds.ReadAsArray()

print data
# <demo> --- stop ---

#Una sola banda (capa):
band = ds.GetRasterBand(1)
data = band.ReadAsArray()

print data

# <demo> --- stop ---


#Dibujar la banda usando basemap
m = Basemap(width = 272257.508, \
        height = 269254.668, \
        resolution = 'h', \
        projection = 'tmerc', \
        lon_0 = 1.727858333, \
        lat_0 = 41.715877778)

#El equivalente al geotransform. Empezando po 0 y acabando por 272257.508, de suma 272 a cada elemento
x = numpy.linspace(0, 272257.508, 272)
y = numpy.linspace(269254.668, 0, 269)

#Se crea la matriz con los valores de x e y, para poder pasarla a Basemap
xx, yy = numpy.meshgrid(x, y)

#contourf dibuja curvas de nivel coloreadas por dentro "isobandas"
cs = m.contourf(xx,yy,data)

plt.show()

# <demo> --- stop ---


#El mapa se puede complicar un poco más

#Empezando por 0.1 y acabando por 25, pintamos un color cada 3 litros acumulados.
m.contourf(xx,yy,data,numpy.arange(0.1,25,3))

#Dibujamos las zonas de tierra y mar como fondo del maps
m.drawmapboundary(fill_color=(0.8,0.8,1))
m.fillcontinents(color='beige', zorder=0)

#Dibujamos las comarcas
#Se abrirá el archivo comarcas.shp, pero se tiene que quitar la extensión
m.readshapefile('data/comarcas', 'comarcas')

#Y finalmente, la leyenda y el título
cbar = m.colorbar(cs,location='bottom',pad="5%")
cbar.set_label(u'precipitación (mm)')

plt.show()
# <demo> --- stop ---


#Cálculos entre rasters 

#Abrimos otro raster para poder jugar con los datos
ds2 = gdal.Open('data/XXX_RN1_20131117_0100_CMPAC1C_1h.tif')
data2 = ds2.ReadAsArray()

#Sumar dos matrices con numpy es inmediato
suma = data + data2

m.contourf(xx,yy,suma,numpy.arange(0.1,35,3))
m.drawmapboundary(fill_color=(0.8,0.8,1))
m.fillcontinents(color='beige', zorder=0)

m.readshapefile('data/comarcas', 'comarcas')

plt.show()

# <demo> --- stop ---


#Zonas con lluvia de más de 6 litros en la hora 00 (primer archivo abierto)
data_condicion = (data > 6)
cs = m.pcolormesh(xx,yy,data_condicion)
plt.show()

# <demo> --- stop ---

#Zonas donde no llovió a las 00 y si que llovió a las 01
data_condicion = (data < 0.1) * (data2 > 0.1)
cs = m.pcolormesh(xx,yy,data_condicion)
plt.show()

# <demo> --- stop ---

#Zonas en las que ha llovido todo el dia

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

#Para cada hora, se abre el archivo
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

#Dibujar el número de horas de lluvia es identico a los ejemplos anteriores
cs = m.pcolormesh(xx,yy,horas_lluvia)
m.drawmapboundary(fill_color=(0.8,0.8,1))
m.fillcontinents(color='beige', zorder=0)
m.readshapefile('data/comarcas', 'comarcas')
cbar = m.colorbar(cs,location='bottom',pad="5%")
cbar.set_label(u'horas de lluvia')

plt.figure()
# <demo> --- stop ---

#Dibujar solo las zonas donde el valor es 10 (ha llovido en cada imagen), también es sencillo
cs = m.pcolormesh(xx,yy,horas_lluvia == 10)
m.drawmapboundary(fill_color=(0.8,0.8,1))
m.fillcontinents(color='beige', zorder=0)
m.readshapefile('data/comarcas', 'comarcas')
cbar = m.colorbar(cs,location='bottom',pad="5%")
cbar.set_label(u'horas de lluvia')
plt.show()
# <demo> --- stop ---


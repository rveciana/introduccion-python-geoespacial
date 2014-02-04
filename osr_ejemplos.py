# -*- coding: utf-8 -*-
"""
8as Jornadas Sig Libre 
26 de Marzo de 2014
Introducción a Python para usos geoespaciales

Ejemplos para trabajar con las proyecciones (osr/python)
"""

from osgeo import gdal
from osgeo import osr

#Abrir un dataset
ds = gdal.Open('data/XXX_RN1_20131117_0000_CMPAC1C_1h.tif')
# <demo> --- stop ---

#Ver todos los métodos disponibles:
help(ds)
# <demo> --- stop ---


#Leer los metadatos de la proyección:
#Proyección:
proj_in = ds.GetProjection()

print proj_in
#Información sobre el formato: 
#http://www.geoapi.org/3.0/javadoc/org/opengis/referencing/doc-files/WKT.html

# <demo> --- stop ---
#Geotransform
gt = ds.GetGeoTransform()

"""
geotransform[0] = East/West location of Upper Left corner
geotransform[1] = X pixel size
geotransform[2] = X pixel rotation
geotransform[3] = North/South location of Upper Left corner
geotransform[4] = Y pixel rotation
geotransform[5] = Y pixel size

Xgeo = gt(0) + Xpixel*gt(1) + Yline*gt(2)
Ygeo = gt(3) + Xpixel*gt(4) + Yline*gt(5)
"""

print gt

# <demo> --- stop ---

#Cambio de proyección para un punto:

proj_out = osr.SpatialReference()
proj_out.ImportFromEPSG(4326)

#proj_in es texto por defecto, y hay que convertirlo en un objeto SpatialReference:
proj_in = osr.SpatialReference(proj_in)

transf = osr.CoordinateTransformation(proj_in, proj_out)

punto = transf.TransformPoint(gt[0], gt[3])

print punto

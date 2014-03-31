# -*- coding: utf-8 -*-
"""
8as Jornadas Sig Libre 
26 de Marzo de 2014
Introduction to Python for geospatial uses

Examples for using fiona to work with projections (osr/python)
"""

from osgeo import gdal
from osgeo import osr

#Open a dataset
ds = gdal.Open('data/XXX_RN1_20131117_0000_CMPAC1C_1h.tif')
# <demo> --- stop ---

#Reading the projection metadata:
#Projection:
proj_in = ds.GetProjection()

print proj_in
#Information about the used format: 
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

#Projection change for a point:

proj_out = osr.SpatialReference()
proj_out.ImportFromEPSG(4326)

#proj_in is a String, so it must be converted to a SpatialReference object:
proj_in = osr.SpatialReference(proj_in)

transf = osr.CoordinateTransformation(proj_in, proj_out)

punto = transf.TransformPoint(gt[0], gt[3])

print punto

# <demo> --- stop ---
#using the geotransform functions
#Pixel to coordinates:
gt = (1,1,0,1,0,1)
gdal.ApplyGeoTransform(gt,1,1)

#Coordinates to pixel
result, inv_gt = gdal.InvGeoTransform(gt)
gdal.ApplyGeoTransform(inv_gt,1,1)

# <demo> --- stop ---

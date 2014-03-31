# -*- coding: utf-8 -*-
"""
8as Jornadas Sig Libre 
26 de Marzo de 2014
Introduction to Python for geospatial uses

Examples for using mayavi to create 3d images
"""

#The libraries used are:
from osgeo import gdal
import numpy as np
from tvtk.api import tvtk
from mayavi import mlab
import Image

# <demo> --- stop ---
#The data is loaded as usual, but it has to be converted to float32
ds = gdal.Open('data/dem.tiff')
data = ds.ReadAsArray()

data = data.astype(np.float32)

# <demo> --- stop ---
#Creating a 3d representation is simple
mlab.figure(size=(640, 800), bgcolor=(0.16, 0.28, 0.46))

surf = mlab.surf(data, warp_scale=0.2) 
mlab.show()
# <demo> --- stop ---

#To draw a picture on the elevation, use the following steps:
#The image must be rotated 90 degrees:
im1 = Image.open("data/ortofoto.jpg")
im2 = im1.rotate(90)
im2.save("/tmp/ortofoto90.jpg")
#The image must be loaded with the tvtk library
bmp1 = tvtk.JPEGReader()
bmp1.file_name="/tmp/ortofoto90.jpg" #any jpeg file

my_texture=tvtk.Texture()
my_texture.interpolate=0
my_texture.set_input(0,bmp1.get_output())


mlab.figure(size=(640, 800), bgcolor=(0.16, 0.28, 0.46))
##A color must be defined
surf = mlab.surf(data, color=(1,1,1), warp_scale=0.2) 
surf.actor.actor.mapper.scalar_visibility = False
surf.actor.enable_texture = True
surf.actor.tcoord_generator_mode = 'plane'
surf.actor.actor.texture = my_texture
mlab.show()

#mlab.view(-5.9, 83, 570, [5.3, 20, 238])
#mlab.savefig('test.png')


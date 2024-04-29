import rasterio as rio
from rasterio import plot
import geopandas as gpd
from matplotlib import pyplot as plt
import os
import ee
import sys
import contextily as ctx
import geemap
from osgeo import ogr

# Authenticating and initializing Google Earth Engine (GEE) API
ee.Authenticate()
ee.Initialize()

# Setting up work directory and directories for storing data
wd = '/content/drive/MyDrive/CW1'
td = '/content/work'
download = os.path.join(td, 'download')
os.makedirs(td, exist_ok=True)
os.makedirs(download, exist_ok=True)

# Defining date ranges for imagery before and after the wildfire event
datefromb = '2018-10-20'  # Start date for imagery search before the wildfire
datetob = '2018-10-30'  # End date for imagery search before the wildfire
datefroma = '2018-09-01'  # Start date for imagery search after the wildfire
datetoa = '2018-09-05'  # End date for imagery search after the wildfire

# Importing and exploring the study area shapefile
shapefile1 = os.path.join(wd, 'dix.shp')
shap = gpd.read_file(shapefile1)
shap.crs = "EPSG:4326"

# Plotting the study area shapefile to visualize its size and location
fig, ax = plt.subplots(figsize=(15, 15))
shap_3857 = shap.to_crs(epsg=3857)
shap_3857.plot(ax=ax)
ctx.add_basemap(ax, source=ctx.providers.Stamen.TonerLite, zoom=10)

# Getting the extent of the study area
shape = shap.loc[shap.index == 3]
shapefileextent = shape.bounds
xmin, ymin, xmax, ymax = shapefileextent
geometry = ee.Geometry.Rectangle([xmin, ymin, xmax, ymax])

# NBR After fire October to November 2021
map = geemap.Map()
map.add_basemap('SATELLITE')  # Background satellite imagery layer
s2imagecol = ee.ImageCollection('COPERNICUS/S2').filterDate(datefromb, datetob).mean().divide(10000)
nbra = s2imagecol.normalizedDifference(['B8', 'B12'])
nbrviz = {'min': -0.2, 'max': 0.5, 'palette': ['#b30000', '#fd8d3c', '#ffeda0', '#74c476', '#00441b']}
map.addLayer(nbra, nbrviz, 'NBRa', False)
map.addLayer(s2imagecol.clip(geometry), {"min": 0, "max": 4000, "bands": ['B4', 'B3', 'B2']}, 'maskeNBRa', False)
imgRGBa = s2imagecol.visualize(**{'bands': ['B5', 'B4', 'B3'], 'min': 0.1, 'max': 0.5})
NBRa_RGBa = nbra.visualize(**{'min': -0.2, 'max': 0.5, 'palette': ['#b30000', '#fd8d3c', '#ffeda0', '#74c476', '#00441b']})
map.centerObject(geometry, 15)
map.addLayer(ee.ImageCollection([imgRGBa, NBRa_RGBa]).mosaic().clip(geometry), {}, 'Mosaic')
map.add_colorbar(nbrviz, label='NBR Severity', orientation='vertical', layer_name='Mosaic', position='bottomleft')
map

# Exporting Image to drive
filename3 = os.path.join(download, 'NBRAfter.tif')
feature = ee.Feature(geometry, {})
roi = feature.geometry()
NBRAfter = ee.ImageCollection([imgRGBa, NBRa_RGBa]).mosaic().clip(roi)
geemap.ee_export_image_to_drive(NBRAfter, description='NBRAft', folder='wd', region=roi, scale=30)

# NDVI Before burning (October to November 2020)
map = geemap.Map()
map.add_basemap('SATELLITE')
s2imagecol = ee.ImageCollection('COPERNICUS/S2').filterDate(datefromb, datetob).median().divide(10000)
ndvi = s2imagecol.normalizedDifference(['B3', 'B11'])
ndviviz = {"min": -1, "max": 1, "palette": ['white', 'blue']}
map.addLayer(ndvi, ndviviz, 'NDVI', False)
map.addLayer(s2imagecol.clip(geometry), {"bands": ['B5', 'B4', 'B3'], "min": 0.1, "max": 0.5}, 'maskeNDVI', False)
map.centerObject(geometry, 12)
map.addLayer(ee.ImageCollection([s2imagecol.visualize(**{'bands': ['B5', 'B4', 'B3'], 'min': 0.1, 'max': 0.5}), ndvi.visualize(**{'min': -0.04, 'max': 0.7, 'palette': ['#feb24c', '#c7e9c0', '#74c476', '#238b45', '#00441b']})]).mosaic().clip(geometry), {}, 'Mosaic')
map.add_colorbar(ndviviz, label='NDVI Density', orientation='vertical', layer_name='NDVI_cl_bar', position='bottomleft')
map.add_legend(legend_keys=['Sand', 'Thinly Vegetation', 'Mod.-Sparse Vegetation', 'Mod.-Dense Vegetation', 'Dense Vegetation'], legend_colors=['#feb24c', '#c7e9c0', '#74c476', '#238b45', '#00441b'])
map

# Exporting Image to drive
filename3 = os.path.join(download, 'NDVI_Before.tif')
feature = ee.Feature(geometry, {})
roi = feature.geometry()
NDVIBefore = ee.ImageCollection([s2imagecol.visualize(**{'bands': ['B5', 'B4', 'B3'], 'min': 0.1, 'max': 0.5}), ndvi.visualize(**{'min': -0.04, 'max': 0.7, 'palette': ['#feb24c', '#c7e9c0', '#74c476', '#238b45', '#00441b']}), ]).mosaic().clip(roi)
geemap.ee_export_image_to_drive(NDVIBefore, description='NDVI_Before', folder='wd', region=roi, scale=30)

# Difference between NDVI Before and after (One Year duration)
map = geemap.Map()
ndviviz = {'min': -1, 'max': 1, 'palette': ['#feb24c', '#c7e9c0', '#74c476', '#238b45', '#00441b']}
maskendvi = ndvi.updateMask(ndvi.gte(-3))
dndvi = maskendvi.subtract(maskendvi)
imgRGB = s2imagecol.visualize(**{'bands': ['B5', 'B4', 'B3'], 'min': 0.1, 'max': 0.5})
DNDVI_RGB = dndvi.visualize(**{'min': -1, 'max': 1, 'palette': ['#feb24c', '#c7e9c0', '#74c476', '#238b45', '#00441b']})
map.centerObject(geometry, 7)
map.addLayer(ee.ImageCollection([imgRGB, DNDVI_RGB]).mosaic().clip(geometry), {}, 'Mosaic')
map.add_colorbar(nbrviz, label='NDVI Density', orientation='vertical', layer_name='DNDVI_cl_bar', position='bottomleft')
map.add_legend(legend_keys=['Sand', 'Thinly Vegetation', 'Mod.-Sparse Vegetation', 'Mod.-Dense Vegetation', 'Dense Vegetation'], legend_colors=['#feb24c', '#c7e9c0', '#74c476', '#238b45', '#00441b'])
map

# Exporting Image to drive
filename3 = os.path.join(download, 'DNDVI.tif')
feature = ee.Feature(geometry, {})
roi = feature.geometry()
DNDVI = ee.ImageCollection([imgRGB, DNDVI_RGB]).mosaic().clip(roi)
geemap.ee_export_image_to_drive(DNDVI, description='DNDVI', folder='wd', region=roi, scale=30)

# Opening all raster files
NBR_before = rio.open(os.path.join(download, 'NBR_Before.tif'))
NBR_after = rio.open(os.path.join(download, 'NBR_After.tif'))
DNBR = rio.open(os.path.join(download, 'DNBR.tif'))
NDVI_before = rio.open(os.path.join(download, 'NDVI_Before.tif'))
NDVI_after = rio.open(os.path.join(download, 'NDVI_After.tif'))
DNDVI = rio.open(os.path.join(download, 'DNDVI.tif'))

# Plotting raster files for visualization
fig, axes = plt.subplots(1, 2, figsize=(40, 30))
plot.show(NBR_before, ax=axes[0])
axes[0].set_title('Normalized Burn Ration Before Fire', fontsize=50, color='#f03b20')
plot.show(NBR_after, ax=axes[1])
axes[1].set_title('Normalized Burn Ration Before Fire', fontsize=50, color='#f03b20')

fig, axes = plt.subplots(1, 2, figsize=(40, 30))
plot.show(NDVI_before, ax=axes[0])
axes[0].set_title('NDVI Burn Ration Before Fire', fontsize=50, color='#f03b20')
plot.show(NDVI_after, ax=axes[1])
axes[1].set_title('NDVI Burn Ration Before Fire', fontsize=50, color='#f03b20')

fig, axes = plt.subplots(1, 2, figsize=(40, 30))
plot.show(DNBR, ax=axes[0])
axes[0].set_title('Difference NBR', fontsize=50, color='#f03b20')
plot.show(DNDVI, ax=axes[1])
axes[1].set_title('Difference NDVI', fontsize=50, color='#f03b20')

# Displaying metadata
print("The information about DNBR raster file:")
print(DNBR.meta)
print("The information about DNDVI raster file:")
print(DNDVI.meta)
print("The information about NBR_after raster file:")
print(NBR_after.meta)
print("The information about NBR_before raster file:")
print(NBR_before.meta)
print("The information about NDVI_after raster file:")
print(NDVI_after.meta)
print("The information about NDVI_before raster file:")
print(NDVI_before.meta)

# Converting shapefile to GeoJSON format
roi2 = gpd.read_file(os.path.join(wd," files (2)/New_Shapefile.shp"))
roi2.crs = "EPSG:4326"
geoms = roi2.geometry.values
geometry = geoms[0]
from shapely.geometry import mapping
geoms = [mapping(geoms[0])]

# Extracting raster values within the polygon
with rio.open(os.path.join(download, 'NDVI_Before.tif')) as src:
    out_image, out_transform = mask(src, geoms, crop=True)

# Exporting to Google Drive
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

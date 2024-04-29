# Wildfire Severity Assessment using Remote Sensing Data

## Overview
This Git repository serves as a comprehensive resource for Dixie 2018 forest fire severity assessment using remote sensing indices such as Normalized Difference Vegetation Index (NDVI), Normalized Burn Ratio (NBR), and their respective differences (dNBR and dNDVI). The repository includes scripts, notebooks, and data visualization tools tailored for analyzing satellite imagery and assessing forest fire impacts on vegetation health and burn severity. It provides workflows for processing, visualizing, and interpreting NDVI and NBR data, enabling researchers, land managers, and stakeholders to conduct in-depth analyses of forest fire-affected areas. The repository aims to facilitate the understanding of the ecological impacts of forest fires and support decision-making processes related to post-fire recovery and management strategies.

## Study Area
The study area encompasses Butte Camp, California, which experienced a wildfire event during the specified time period. The shapefile delineating the study area boundary is provided in the repository.

## Date Ranges
The analysis covers two distinct time periods:

- Before Wildfire: October 20, 2018, to October 30, 2018
- After Wildfire: September 1, 2018, to September 5, 2018
These date ranges allow for the comparison of vegetation indices and wildfire severity before and after the wildfire event.

## Code Functionality
The Python scripts perform the following tasks:

- Importing Libraries: Necessary libraries for geospatial analysis, including rasterio, geopandas, matplotlib, and Google Earth Engine API (geemap), are imported.
- Mounting Google Drive: Google Drive is mounted to access and store files.
- Setting Up Work Directory: The working directory and folder structure are established to organize downloaded data and results.
- Defining Date Ranges: Date ranges are defined to specify the periods before and after the wildfire event.
- Importing and Exploring Shapefile: The shapefile representing the study area boundary is imported and explored using geopandas.
- Plotting Study Area Shapefile: The shapefile is plotted to visualize the study area boundary on a map.
- Exploring Area of Different Polygons: The script calculates and prints the area of each polygon in the shapefile.
- Exporting Images to Drive: Satellite imagery data, including Normalized Burn Ratio (NBR) and Normalized Difference Vegetation Index (NDVI), are retrieved from Google Earth Engine, visualized, and exported to Google Drive.
- Plotting Raster Files for Visualization: Raster files representing NDVI, NBR, Difference NDVI (dNDVI), and Difference NBR (dNBR) are plotted for visualization using matplotlib.
- Extracting Raster Values within Polygon: Raster values within a specified polygon are extracted using rasterio's mask function.
- Uploading Data to Google Drive: Extracted raster data or other files are uploaded to Google Drive using the Google Drive API.

## Prerequisites:
- Python 3.x
- Google Earth Engine (GEE) account
- Google Drive API credentials (for exporting data to Google Drive)
- Required Python packages:
  - rasterio
  - geopandas
  - matplotlib
  - earthengine-api
  - geemap
  - contextily
  - osgeo

## Usage
1. Clone this repository to your local machine.
2. Ensure that all required libraries are installed.
3. Authenticate and initialize Google Earth Engine (GEE) API by running the following command in the terminal:
4. Update the date ranges and study area boundary as needed.
5. Run the Python script (`wildfire_assessment.py`) to execute the analysis and visualization.

## Files:
- `wildfire_assessment.py`: Main Python script for conducting wildfire impact assessment.
- `dix.shp`: Sample shapefile representing the study area.
- `New_Shapefile.shp`: Alternative shapefile for extracting raster values within polygons.
- `README.md`: This file containing information about the repository.

## References:
- Google Earth Engine Python API: https://developers.google.com/earth-engine/guides/python_install
- GeoPandas documentation: https://geopandas.org/
- Contextily documentation: https://contextily.readthedocs.io/en/latest/
- Rasterio documentation: https://rasterio.readthedocs.io/en/latest/
- Earth Engine Python API documentation: https://developers.google.com/earth-engine/guides/python_install
- Google Drive API documentation: https://developers.google.com/drive/api/v3/about-sdk

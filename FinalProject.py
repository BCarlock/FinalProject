### Create an empty polygon and choose pour point

## Create file geodata base
""" This tool is used to create a file geodata base, mosaic raster set,and watershed layer at the same time"""
# CreateFileGDB_management (out_folder_path, out_name, {out_version})

import arcpy
from arcpy import env
from arcpy.sa import *

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Set local variables

out_folder_path = raw_input("Enter the file path for the geodatabase you would like to create: ")
out_name = raw_input("Enter the name of the geodatabase you would like to create: ")

# Execute CreateFileGDB

arcpy.CreateFileGDB_management(out_folder_path, out_name)

### Set as default database

## Create Mosaic Dataset
# CreateMosaicDataset_management (in_workspace, in_mosaicdataset_name, coordinate_system, {num_bands}, {pixel_type}, {product_definition}, {product_band_definitions}
# Set local variables

arcpy.env.workspace = out_folder_path


#Create Mosaic Dataset

gdbname = arcpy.env.workspace + '/' + out_name + '.gdb'
mdname = raw_input("Enter a file name for the raster set you would like to create: ")
prjfile = "PROJCS['NAD_1983_UTM_Zone_17N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-81.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]];-5120900 -9998100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision"
noband = ""
pixtype = "8_BIT_UNSIGNED"
pdef = "NONE"
wavelength = ""

arcpy.CreateMosaicDataset_management(gdbname, mdname, prjfile, noband,pixtype, pdef, wavelength)

## Add Rasters to Mosaic Dataset
# AddRastersToMosaicDataset_management (in_mosaic_dataset, raster_type, input_path, {update_cellsize_ranges}, {update_boundary}, {update_overviews}, {maximum_pyramid_levels}, {maximum_cell_size}, {minimum_dimension}, {spatial_reference}, {filter}, {sub_folder}, {duplicate_items_action}, {build_pyramids}, {calculate_statistics}, {build_thumbnails}, {operation_description}, {force_spatial_reference})
# Set local variables
mdname = (gdbname + "/" + mdname)
rastype = "Raster Dataset"
inpath = raw_input("Please enter the raster files you wish to mosaic (multiple files require a semi-colon between each file):  ")
updatecs = "UPDATE_CELL_SIZES"
updatebnd = "UPDATE_BOUNDARY"
updateovr = "UPDATE_OVERVIEWS"
maxlevel = "2"
maxcs = "#"
maxdim = "#"
spatialref = "#"
inputdatafilter = "*.tif"
subfolder = "NO_SUBFOLDERS"
duplicate = "EXCLUDE_DUPLICATES"
buildpy = "BUILD_PYRAMIDS"
calcstats = "CALCULATE_STATISTICS"
buildthumb = "NO_THUMBNAILS"
comments = "Add Raster Datasets"
forcesr = "#"
arcpy.AddRastersToMosaicDataset_management(mdname, "Raster Dataset", inpath, "UPDATE_CELL_SIZES", "UPDATE_BOUNDARY", "NO_OVERVIEWS", "", "0", "1500", "", "", "SUBFOLDERS", "ALLOW_DUPLICATES", "NO_PYRAMIDS", "NO_STATISTICS", "NO_THUMBNAILS", "", "NO_FORCE_SPATIAL_REFERENCE")

## Fill
# Fill_sa (in_surface_raster, z_limit, out_surface_raster)

# Set local variables
inSurfaceRaster = mdname
zLimit = 3.28

# Execute FlowDirection
outFill = Fill(inSurfaceRaster, zLimit)

# Save the output 
outFill.save(gdbname + "/fill_out")

## Flow Direction
# FlowDirection_sa (in_surface_raster, force_flow, out_drop_raster, out_flow_direction_raster) 

# Set local variables
inSurfaceRaster2 = outFill
outDropRaster = (gdbname + "/flow_drop")

# Execute FlowDirection
outFlowDirection = FlowDirection(inSurfaceRaster2, "FORCE", outDropRaster)

# Save the output 
outFlowDirection.save(gdbname + "/flow_dir")

## Flow Accumulation
# FlowAccumulation_sa (in_flow_direction_raster, in_weight_raster, data_type, out_accumulation_raster) 
# Set local variables

inFlowDirRaster = outFlowDirection
inWeightRaster = ""
dataType = "INTEGER"

# Execute FlowAccumulation
outFlowAccumulation = FlowAccumulation(inFlowDirRaster, inWeightRaster, dataType)

# Save the output 
outFlowAccumulation.save(gdbname + "/flow_acc")

## Watershed
# Watershed_sa (in_flow_direction_raster, in_pour_point_data, pour_point_field, out_raster) 

# Set local variables
inFlowDirection = outFlowDirection
inPourPointData = (raw_input("Enter the path and file name to your pour point shape file: "))

# Execute Watershed
outWatershed = arcpy.gp.Watershed_sa(inFlowDirection, inPourPointData, "watershedFlow")







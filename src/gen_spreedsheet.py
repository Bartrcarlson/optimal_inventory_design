import pandas as pd
import geopandas as gpd
import yaml
from osgeo import gdal, ogr
import numpy as np

gdal.UseExceptions()

with open("config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)


def var_by_strata():
    """
    takes a rasterfile of tree volumes and a shapefile of strata and returns a dataframe
    with the standard deviation of the volumes in each strata.
    the polygon can contain more than one occurrence of a strata,
    but they will be reported as one.
    also calculates the total area within each strata.
    """

    # Load
    raster = gdal.Open(cfg["paths"]["rasterfile"])
    rb = raster.GetRasterBand(cfg["raster_band"])
    shape = gpd.read_file(cfg["paths"]["shapefile"])

    # Dissolve/merge polygons by the Strata_Dat column
    merged_shape = shape.dissolve(by=cfg["shapefile_field_names"]["strata"])
    merged_shape = merged_shape.reset_index()
    merged_shape = merged_shape.rename(columns={"index": "Strata_Dat"})

    std_devs = []
    areas = []

    # Get spatial reference from shapefile
    srs = ogr.osr.SpatialReference()
    srs.ImportFromWkt(shape.crs.to_wkt())

    for geometry, data in zip(merged_shape.geometry, merged_shape.iterrows()):
        ogr_geom = ogr.CreateGeometryFromWkt(geometry.wkt)

        mem_ds = ogr.GetDriverByName("Memory").CreateDataSource("temp")
        layer = mem_ds.CreateLayer("temp", srs=srs, geom_type=ogr.wkbPolygon)

        featureDefn = layer.GetLayerDefn()
        feature = ogr.Feature(featureDefn)
        feature.SetGeometry(ogr_geom)
        layer.CreateFeature(feature)

        # Use GDAL's RasterizeLayer to get the raster values for this geometry
        mem_drv = gdal.GetDriverByName("MEM")
        target_ds = mem_drv.Create(
            "", raster.RasterXSize, raster.RasterYSize, 1, gdal.GDT_Byte
        )
        target_ds.SetProjection(raster.GetProjection())
        target_ds.SetGeoTransform(raster.GetGeoTransform())

        # Rasterize using the in-memory layer
        gdal.RasterizeLayer(target_ds, [1], layer, burn_values=[1])

        array = target_ds.ReadAsArray()

        # Use np.where to get the raster values for this polygon
        values = rb.ReadAsArray()[np.where(array == 1)]
        values = values.astype(np.float64)
        values = values[np.isfinite(values)]
        nodata_value = rb.GetNoDataValue()
        if nodata_value is not None:
            values = values[values != nodata_value]

        area = geometry.area
        areas.append([data[1]["Strata_Dat"], area])
        std_dev = np.std(values)
        std_devs.append([data[1]["Strata_Dat"], std_dev])

    df_area = pd.DataFrame(areas, columns=["Strata", "Area"])
    df_std = pd.DataFrame(std_devs, columns=["Strata", "StandardDev"])
    result_df = pd.merge(df_std, df_area, on="Strata")
    return result_df


def generate_spreedsheet():
    """
    creates a spreedsheet for data entry.
    one the first page is a field to list the total number of plots.

    on the second page is a table with all the strata in the first column.
    the second column will have the std dev of the strata from the rasterself.
        via the extract_raster_var_by_strata.py script.
    the third column is a field to hard set the number of plots in that strata default blank.
    the fourth column defaults to 1.0 and is a field to set the weight of that strata.
        effectivly allowing the user to under sample a strata. if the user wants to
    """
    df_page1 = pd.DataFrame()
    df_page1["Total_Plots"] = [0]

    df_page2 = var_by_strata()
    df_page2["hard_set_plot number"] = 0
    df_page2["weight"] = 1.0

    with pd.ExcelWriter(cfg["paths"]["spreedsheet"], engine="openpyxl") as writer:
        df_page1.to_excel(writer, sheet_name="page1", index=False)
        df_page2.to_excel(writer, sheet_name="page2", index=False)


if __name__ == "__main__":
    generate_spreedsheet()

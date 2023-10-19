import geopandas as gpd
import pandas as pd
from osgeo import gdal, ogr
import numpy as np

gdal.UseExceptions()


def var_by_strata():
    """
    takes a rasterfile of tree volumes and a shapefile of strata and returns a dataframe
    with the standard deviation of the volumes in each strata.
    the polygon can contain more than one occurrence of a strata, but they will be reported as one.
    """
    # Paths to files
    rasterfile = "../data/full_volume.tif"
    shapefile = "../data/SVR_TimberStrata.shp"

    # Load the raster file
    raster = gdal.Open(rasterfile)
    rb = raster.GetRasterBand(1)

    # Load the shapefile
    shape = gpd.read_file(shapefile)

    # Dissolve/merge polygons by the Strata_Dat column
    merged_shape = shape.dissolve(by="Strata_Dat")
    merged_shape = merged_shape.reset_index()
    merged_shape = merged_shape.rename(columns={"index": "Strata_Dat"})
    # Create an empty list to store standard deviations
    std_devs = []
    # Get spatial reference from shapefile
    srs = ogr.osr.SpatialReference()
    srs.ImportFromWkt(shape.crs.to_wkt())
    # Loop over each merged feature in shapefile
    for geometry, data in zip(merged_shape.geometry, merged_shape.iterrows()):
        # Convert shapely geometry to ogr geometry
        ogr_geom = ogr.CreateGeometryFromWkt(geometry.wkt)

        # Create an in-memory vector layer
        mem_ds = ogr.GetDriverByName("Memory").CreateDataSource("temp")
        layer = mem_ds.CreateLayer("temp", srs=srs, geom_type=ogr.wkbPolygon)

        # Add the ogr_geom geometry to this layer
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

        # Calculate standard deviation
        # if len(values) > 0:
        std_dev = np.std(values)
        std_devs.append([data[1]["Strata_Dat"], std_dev])

    # Convert list to DataFrame
    df = pd.DataFrame(std_devs, columns=["Strata", "StandardDev"])

    return df


if __name__ == "__main__":
    print(var_by_strata())

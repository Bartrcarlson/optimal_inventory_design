import pandas as pd
import geopandas as gpd
import extract_raster_var_by_strata as VarExtract


def generate_spreedsheet(rasterfile, shapefile, spreedsheetpath):
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

    df_page2 = VarExtract.var_by_strata(rasterfile, shapefile)
    df_page2["hard_set_plot number"] = 0
    df_page2["weight"] = 1.0

    with pd.ExcelWriter(spreedsheetpath, engine="openpyxl") as writer:
        df_page1.to_excel(writer, sheet_name="page1", index=False)
        df_page2.to_excel(writer, sheet_name="page2", index=False)


if __name__ == "__main__":
    # Paths to files
    rasterfile = "../data/full_volume.tif"
    shapefile = "../data/SVR_TimberStrata.shp"
    spreedsheetpath = "../user_input/strata.xlsx"
    generate_spreedsheet(rasterfile, shapefile, spreedsheetpath)

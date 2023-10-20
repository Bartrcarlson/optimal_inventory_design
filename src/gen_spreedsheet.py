import pandas as pd
import geopandas as gpd


def generate_spreedsheet():
    """
    creates a spreedsheet for data entry.
    one the first page is a field to list the total number of plots.

    on the second page is a table with all the strata in the first column.
    the second column is a field to hard set the number of plots in that strata default blank.
    the third column defaults to 1.0 and is a field to set the weight of that strata.
        effectivly allowing the user to under sample a strata. if the user wants to
    """
    strata_shapefile = "../data/SVR_TimberStrata.shp"
    strata = gpd.read_file(strata_shapefile)
    strata = strata[["Strata_Dat"]]
    strata = strata.drop_duplicates()

    df_page1 = pd.DataFrame()
    df_page1["Total_Plots"] = [0]

    df_page2 = pd.DataFrame()
    df_page2["Strata_Dat"] = strata["Strata_Dat"]
    df_page2["hard_set_plot number"] = ["" for i in range(len(strata))]
    df_page2["weight"] = [1.0 for i in range(len(strata))]

    with pd.ExcelWriter("../user_input/strata.xlsx", engine="openpyxl") as writer:
        df_page1.to_excel(writer, sheet_name="page1", index=False)
        df_page2.to_excel(writer, sheet_name="page2", index=False)


if __name__ == "__main__":
    generate_spreedsheet()

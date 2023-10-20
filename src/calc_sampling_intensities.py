import pandas as pd
import geopandas as gpd


def calc_sampling_intensities():
    """
    Calculate sampling intensities for each country based on the total number of plots
    the results of the optimal allocation and the hard set strata.
    """

    total_plots = pd.read_excel("../user_input/strata.xlsx", sheet_name="page1")
    print(total_plots)


if __name__ == "__main__":
    calc_sampling_intensities()

import pandas as pd
import geopandas as gpd
import yaml
import optimal_allocation as oa

with open("config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)


def calc_sampling_intensities():
    """
    Calculate sampling intensities for each country based on the total number of plots
    the results of the optimal allocation and the hard set strata.
    """

    total_plots = pd.read_excel(cfg["paths"]["spreedsheet"], sheet_name="page1")
    total_plots = total_plots["Total_Plots"].sum()

    df = pd.read_excel(cfg["paths"]["spreedsheet"], sheet_name="page2")

    # give the data a good cleaning after the user input.
    df["hard_set_plot_number"] = df["hard_set_plot_number"].fillna(0)
    df["hard_set_plot_number"] = df["hard_set_plot_number"].astype(int)
    df["StandardDev"] = df["StandardDev"].astype(float)
    df["Area"] = df["Area"].astype(float)
    df["weight"] = df["weight"].astype(float)
    df["StandardDev"] = df["StandardDev"].fillna(0.0)
    df["Area"] = df["Area"].fillna(0.0)
    df["weight"] = df["weight"].fillna(1.0)

    if total_plots == 0:
        raise ValueError("The user has not set the total number of plots.")
    if (df["weight"] > 1.0).any() or (df["weight"] < 0.0).any():
        raise ValueError("The user has set a weight outside of 0.0 to 1.0")

    df["plot_count"] = df["hard_set_plot_number"]
    reduced_total = total_plots - df["plot_count"].sum()
    calced_num = oa.neyman_alloc(
        reduced_total, df["Strata"], df["Area"], df["StandardDev"]
    )

    # if the hard set number is zero then use the calced_num. otherwise use the hard set number.
    # calced_num is a dictionary with the strata as the key and the number of plots as the value.

    for strata, value in calced_num.items():
        df.loc[df["Strata"] == strata, "plot_count"] = df.loc[
            df["Strata"] == strata, "plot_count"
        ].replace(0, value)

    print(df)


if __name__ == "__main__":
    calc_sampling_intensities()

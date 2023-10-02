import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_boxplots(df, observation_name):

    columns_to_plot = ["value", "value_std_dev", "latitude",
                    "year", "month", "time_decimal", 
                    "midpoint_time", "longitude", "altitude", 
                    "nvalue", "elevation", "intake_height"]

    fig, axs = plt.subplots(4, 3, figsize=(9, 8))
    axs = axs.ravel() 

    for i, col in enumerate(columns_to_plot):
        axs[i].boxplot(df[col].astype(float))
        axs[i].grid(True)
        axs[i].set_title(col)

    fig.suptitle(f"Boxplots of the variables of {observation_name} dataset", y=1.02)
    fig.tight_layout()
    plt.show()
    
def convert_to_datetime(df):
    df["datetime"] = pd.to_datetime(df[["year", "month", "day", "hour", "minute", "second"]])
    df["value"] = pd.to_numeric(df["value"])
    df["value_std_dev"] = pd.to_numeric(df["value_std_dev"])
    df.drop(["year", "month", "day", "hour", "minute", "second", "site_code"], axis=1, inplace=True)
    return df

def drop_missing_values(df):
    # Missing data will have a value of -999.99 for the mole fraction
    df = df[df["value"] != -999.99]
    return df

def correct_season(df):

    cycle_window = 7 * 12 # months
    
    df["corrected_value"] = df["value"].rolling(window=cycle_window, 
                                                min_periods=cycle_window // 2, 
                                                center=True).mean()
    return df

        
    return df

def plot_timeseries(df, observ_name):

    fig, axs = plt.subplots(1, 2, figsize=(15, 5))
    axs[0].plot(df["datetime"], df["value"], label="CO2 mole fraction", 
                color="blue", marker = "o", ms = 2)
    axs[0].errorbar(df["datetime"], df["corrected_value"], df["value_std_dev"], 
                    label="Average seasonal cycle correction", color="black")
    axs[0].set_xlabel("Time")
    axs[0].set_ylabel("CO2 mole fraction (ppm)")
    axs[0].set_title(f"CO2 Concentration Over Time at {observ_name}")
    axs[0].legend()
    axs[0].grid()

    mask = (df["datetime"].dt.year > 2010) & (df["datetime"].dt.year < 2017)
    axs[1].plot(df.loc[mask, "datetime"], df.loc[mask, "value"], 
                label="CO2 mole fraction", color="blue", marker = "o", ms = 5, mfc = "black")
    axs[1].errorbar(df.loc[mask, "datetime"], df.loc[mask, "corrected_value"], df.loc[mask, "value_std_dev"], 
                    label="Average seasonal cycle correction", color="black", marker="s", ms=3)
    axs[1].set_xlabel("Time")
    axs[1].set_ylabel("CO2 mole fraction (ppm)")
    axs[1].set_title(f"CO2 Concentration Over Time at {observ_name}")
    axs[1].legend()
    axs[1].grid()

    plt.tight_layout()
    plt.show()

import os
from time import sleep
import requests

import pandas as pd
import pypopulation

COUNTRIES_DATA_PATH = os.path.join("seeds", "countries.csv")
COVID_DATA_PATH = os.path.join("seeds", "covid_data.csv")
RAW_COLUMNS = ["Country", "Confirmed", "Deaths", "Active", "Date"]
COLUMNS_FOR_INCREMENT = ["confirmed", "deaths", "active"]


def add_population():
    countries_df = pd.read_csv(COUNTRIES_DATA_PATH)

    if "population" not in countries_df.columns:
        countries_df["population"] = countries_df["iso2"].apply(
            lambda code: pypopulation.get_population(code)
            if isinstance(code, str)
            else None
        )
        countries_df = countries_df.dropna(subset=["population"])
        countries_df.to_csv(COUNTRIES_DATA_PATH, index=False)


def prepare_template_file():
    columns = [col.lower() for col in RAW_COLUMNS]
    pd.DataFrame(columns=columns).to_csv(COVID_DATA_PATH, index=False)


def add_daily_increments(country_df):
    daily_increment_column_names = [f"new_{col}" for col in COLUMNS_FOR_INCREMENT]
    for col, increment_col in zip(COLUMNS_FOR_INCREMENT, daily_increment_column_names):
        country_df[increment_col] = country_df[col].diff()
        country_df[increment_col] = country_df[increment_col].apply(lambda x: max(x, 0))
    return country_df.dropna(subset=daily_increment_column_names, how="any")


def get_country_data(country):
    response = requests.get(f"https://api.covid19api.com/total/country/{country}")
    if response.status_code != 200:
        raise Exception(
            f"Failure in downloading data for {country}.\nReason: {response.reason}"
        )

    country_df = pd.DataFrame(response.json())[RAW_COLUMNS]
    country_df.columns = [col.lower() for col in country_df.columns]
    country_df = add_daily_increments(country_df)

    all_available_countries_df = pd.read_csv(COVID_DATA_PATH)
    all_available_countries_df = pd.concat(
        [country_df, all_available_countries_df], axis=0
    ).drop_duplicates()

    all_available_countries_df.to_csv(COVID_DATA_PATH, index=False)


if __name__ == "__main__":
    add_population()

    if not os.path.isfile(COVID_DATA_PATH):
        prepare_template_file()

    # download example countries
    example_countries = ("poland", "germany")
    for country in example_countries:
        get_country_data(country)
        sleep(10)

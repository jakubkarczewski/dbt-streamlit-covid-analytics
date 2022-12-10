import os
import time

import altair as alt
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

from get_data import COUNTRIES_DATA_PATH, COVID_DATA_PATH, prepare_template_file
from utils.app_utils import populate_db

engine = create_engine("postgresql://postgres:postgres@host.docker.internal:5432/postgres")
if not os.path.isfile(COVID_DATA_PATH):
    prepare_template_file()

st.write("# *DBT Visualisation App*")
countries = pd.read_csv(COUNTRIES_DATA_PATH, index_col=0)["slug"].to_dict()
selected_countries_for_display = st.multiselect("Select countries: ", list(countries.keys()))
selected_countries = [
    countries.get(country) for country in selected_countries_for_display if countries.get(country) is not None
]

(
    get_data_col,
    display_data_col,
    show_table_col,
    clear_col,
) = st.columns(4)

# TODO: learn how to do it properly in streamlit
with get_data_col:
    get_data = st.button("Get Data", 1, "Get data for the countries selected")

with display_data_col:
    display_data = st.button("Display Data", 2, "Display data for the countries selected in form of a chart")

with show_table_col:
    show_table = st.button("Show Table", 3)

with clear_col:
    clear = st.button("Clear", 4)

# TODO: learn how handle clicks properly in streamlit
if any((get_data, display_data, show_table)) and len(selected_countries) == 0:
    st.write("Select countries first!")

if get_data and len(selected_countries) > 0:
    populate_db(selected_countries)

if display_data and len(selected_countries) > 0:
    with st.spinner("Loading data ..."):
        covid_data = pd.read_sql_table("covid_data", con=engine, schema="public_source")
        covid_data = covid_data[covid_data["country"].isin(selected_countries_for_display)]
        time.sleep(1)

    if len(covid_data) > 0:
        st.success("Data Loaded!")
        chart = pd.read_sql_table("stg_deaths_per_month", con=engine)
        alt_chart = (
            alt.Chart(chart)
            .mark_line()
            .encode(
                x=alt.X("month_year", title="Month"),
                y=alt.Y("deaths", title="Number of Deaths"),
                color=alt.Color("country", title="Countries"),
            )
        )
        st.altair_chart(alt_chart, use_container_width=True)

if show_table and len(selected_countries) > 0:
    covid_data = pd.read_sql_table("covid_data", con=engine, schema="public_source")
    covid_data = covid_data[covid_data["country"].isin(selected_countries_for_display)]
    st.write(covid_data)

import os
import time

import altair as alt
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

from get_data import COUNTRIES_DATA_PATH, get_country_data, COVID_DATA_PATH, prepare_template_file

engine = create_engine("postgresql://postgres:postgres@host.docker.internal:5432/postgres")


def populate_db(countries):
    with st.spinner("Creating the seeds..."):
        for country in countries:
            get_country_data(country)
        time.sleep(1)
    st.success("Seeds successfully created!")

    with st.spinner("Installing dependencies..."):
        os.system("dbt deps")
        time.sleep(1)
    st.success("Dependencies successfully installed!")

    st.write("Populating db...")
    with st.spinner("Inserting seeds..."):
        os.system("dbt seed --profiles-dir ./profiles --target docker")
        time.sleep(1)
    st.success("Seeds successfully inserted!")

    with st.spinner("Building models..."):
        os.system("dbt run --full-refresh --profiles-dir ./profiles  --target docker")
        time.sleep(1)
    st.success("Models built!")

    with st.spinner("Creating tests..."):
        os.system("dbt test --profiles-dir ./profiles  --target docker")
        time.sleep(1)
    st.success("Tests created!")

    time.sleep(0.5)

    st.success("Db populated!")


if not os.path.isfile(COVID_DATA_PATH):
    prepare_template_file()
countries = pd.read_csv(COUNTRIES_DATA_PATH, index_col=0)["slug"].to_dict()

st.write("# *DBT Visualisation App*")
selected_countries = st.multiselect("Select countries: ", list(countries.keys()))
selected_slugs = [countries.get(country) for country in selected_countries if countries.get(country) is not None]

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    get_data = st.button("Get Data", 1, "Get data for the countries selected")
with col2:
    clear = st.button("Clear", 2)

if get_data:
    populate_db(selected_slugs)
    dataframe = pd.read_sql_table("covid_data", con=engine, schema="public_source")
    st.write(dataframe)
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

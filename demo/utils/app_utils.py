import os
import time

import streamlit as st

from get_data import get_country_data


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

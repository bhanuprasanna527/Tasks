import streamlit as st
import datetime
import pandas as pd
from utilities.py.ECG_App import ECG_App
from utilities.py.ECG_Sample import ECG_Sample
from utilities.py.streamlit_styling import streamlit_style
from utilities.py.data_view import data_view

ecg = ECG_App()
ecg.database.create_table()

streamlit_style()
st.markdown("#")

tab1, tab2, tab3, tab4 = st.tabs(["View Data", "Delete Data", "Search Data", "Add Data"])

health_conditions_unique = ecg.database.health_conditions_unique()

with tab1:
    df = data_view("Cologne")
    st.dataframe(df)
    st.divider()
    ecg.task_1()
with tab2:
    df = data_view("Cologne")
    st.dataframe(df)
    ecg.delete_sample()
with tab3:
    df = data_view("Cologne")
    filtered_df = ecg.filter_sample(df, health_conditions_unique)
    st.dataframe(filtered_df)
with tab4:
    df = data_view("Cologne")
    st.dataframe(df)
    ecg.create_sample()
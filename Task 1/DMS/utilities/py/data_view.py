import streamlit as st
import psycopg2 as pg
import pandas as pd


def data_view(dbname):
    """
    View the data in the database
    Parameters:
        :param dbname: database name - string
    """

    engine = pg.connect("dbname='Cologne'")
    df = pd.read_sql('select * from ecg', con=engine)

    df[['id', 'tk_id', 'sample_rate', 'duration', 'age']] = df[['id', 'tk_id', 'sample_rate', 'duration', 'age']].apply(pd.to_numeric)

    print(df.columns)
    return df

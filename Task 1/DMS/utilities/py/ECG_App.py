import streamlit as st
import psycopg2
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import os
from utilities.py.ECG_Database import ECG_Database
from utilities.py.ECG_Sample import ECG_Sample
from utilities.py.data_view import data_view


class ECG_App:
    def __init__(self, dbname="Cologne", host="localhost", port="5432"):
        """
        ECG App
        Parameters:
            :param dbname: database name - String
            :param host: database host - String
            :param port: database port - String
        """
        self.database = ECG_Database(dbname=dbname, host=host, port=port)

    def create_sample(self):
        with st.form(key='create_sample'):
            tk_id = st.text_input("Provide TK ID")
            date = st.date_input("Provide Date")
            unit = st.text_input("Provide Unit")
            hospital = st.text_input("Provide Hospital", "University Hospital Cologne")
            sample_rate = st.number_input("Provide Sample Rate")
            duration = st.number_input("Provide Duration")
            health_conditions = st.text_input("Provide Health Conditions")
            age = st.number_input("Provide Age")
            gender = st.selectbox('Provide Gender', ('Male', 'Female', 'Others'))
            image_file_upload = st.file_uploader("Choose the Heart Image File", type=["png", "jpg", "jpeg"])
            ecg_signal_file_upload = st.file_uploader("Choose ECG signal file upload", type=["csv"])
            submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            if image_file_upload is not None:
                file_details = {"FileName": image_file_upload.name, "FileType": image_file_upload.type}
                st.write(file_details)

                st.write(
                    os.path.join(os.getcwd(), "data", str(hospital), str(unit), str(tk_id), "heart image",
                                 image_file_upload.name))

                # Specify the directory where you want to save the uploaded image
                save_dir = os.path.join(os.getcwd(), "data", hospital, unit, tk_id, "heart image")

                # Create the directory if it doesn't exist
                os.makedirs(save_dir, exist_ok=True)

                # Save the uploaded image to a file
                file_path = os.path.join(save_dir, image_file_upload.name)
                with open(file_path, "wb") as f:
                    f.write(image_file_upload.getbuffer())

                st.success("Saved File")
            if ecg_signal_file_upload is not None:
                file_details = {"FileName": ecg_signal_file_upload.name, "FileType": ecg_signal_file_upload.type}
                st.write(file_details)

                st.write(
                    os.path.join(os.getcwd(), "data", str(hospital), str(unit), str(tk_id), "signal data",
                                 image_file_upload.name))

                # Specify the directory where you want to save the uploaded image
                save_dir = os.path.join(os.getcwd(), "data", str(hospital), str(unit), str(tk_id), "signal data")

                # Create the directory if it doesn't exist
                os.makedirs(save_dir, exist_ok=True)

                # Save the uploaded image to a file
                file_path = os.path.join(save_dir, ecg_signal_file_upload.name)
                with open(file_path, "wb") as f:
                    f.write(ecg_signal_file_upload.getbuffer())

                st.success("Saved File")

            heart_image_file_path = os.path.join(os.getcwd(), "data", hospital, unit, tk_id, image_file_upload.name)
            ecg_signal_data_file_path = os.path.join(os.getcwd(), "data", hospital, unit, tk_id, "signal data", ecg_signal_file_upload.name)
            ecg_sample = ECG_Sample(tk_id=tk_id, date=date, unit=unit,
                                    hospital=hospital, sample_rate=sample_rate, duration=duration,
                                    health_conditions=health_conditions, age=age, gender=gender,
                                    ecg_signal_data_file_path=ecg_signal_data_file_path,
                                    heart_image_file_path=heart_image_file_path)

            self.database.add_sample(ecg_sample)

    def delete_sample(self):
        with st.form(key='delete_sample'):
            start_id = st.number_input("Start ID")
            end_id = st.number_input("End ID")

            submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            self.database.delete_samples_in_a_range(start_id=start_id, end_id=end_id)

    def filter_sample(self, df, health_conditions_unique):
        """
        Filter ECG samples
        Parameters:
            :param df: ECG samples - Pandas Dataframe
        :return:
        """
        modify = st.checkbox("Add filters")

        if not modify:
            return df

        df = df.copy()

        # Try to convert datetimes into a standard format (datetime, no timezone)
        for col in df.columns:
            if is_object_dtype(df[col]):
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception:
                    pass

            if is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.tz_localize(None)

        modification_container = st.container()

        with modification_container:
            to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
            for column in to_filter_columns:
                left, right = st.columns((1, 20))

                if is_numeric_dtype(df[column]):
                    _min = float(df[column].min())
                    _max = float(df[column].max())
                    step = st.number_input("Step size", value=_min)
                    user_num_input = right.slider(
                        f"Values for {column}",
                        min_value=_min,
                        max_value=_max,
                        value=(_min, _max),
                        step=step,
                    )
                    df = df[df[column].between(*user_num_input)]
                elif is_datetime64_any_dtype(df[column]):
                    user_date_input = right.date_input(
                        f"Values for {column}",
                        value=(
                            df[column].min(),
                            df[column].max(),
                        ),
                    )
                    if len(user_date_input) == 2:
                        user_date_input = tuple(map(pd.to_datetime, user_date_input))
                        start_date, end_date = user_date_input
                        df = df.loc[df[column].between(start_date, end_date)]
                # Treat columns with < 10 unique values as categorical
                elif is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                    user_cat_input = right.multiselect(
                        f"Values for {column}",
                        df[column].unique(),
                        default=list(df[column].unique()),
                    )
                    df = df[df[column].isin(user_cat_input)]
                else:
                    user_text_input = right.text_input(
                        f"Substring or regex in {column}",
                    )
                    if user_text_input:
                        df = df[df[column].astype(str).str.contains(user_text_input)]

        return df

    def task_1(self):
        # Search for samples at least 10s seconds long
        st.markdown("<h3>Search by Duration of Samples:</h3>", unsafe_allow_html=True)
        dur = st.number_input("Enter at Least Duration", 10)
        long_samples = self.database.search_long_samples(dur)
        print(f"Samples with duration at least {dur} seconds:")
        st.dataframe(long_samples, column_config={1: 'id', 2: 'date', 3: 'tk_id', 4: 'unit', 5: 'hospital',
                                                  6: 'sample_rate', 7: 'duration', 8: 'health_conditions', 9: 'age',
                                                  10: 'gender', 11: 'ecg_signal_data_file_path',
                                                  12: 'heart_image_file_path'})
        st.write(f"\nNumber of samples with duration at least {dur} seconds: {len(long_samples)}.")

        # Count samples for patients at least 50 years old
        st.markdown("<h3>Search by Age of Patients:</h3>", unsafe_allow_html=True)
        age = st.number_input("Enter at Least Age", 50)
        older_than = self.database.count_samples_above_age(age)
        st.dataframe(older_than, column_config={1: 'id', 2: 'date', 3: 'tk_id', 4: 'unit', 5: 'hospital',
                                                  6: 'sample_rate', 7: 'duration', 8: 'health_conditions', 9: 'age',
                                                  10: 'gender', 11: 'ecg_signal_data_file_path',
                                                  12: 'heart_image_file_path'})
        st.write(f"\nNumber of samples for patients at least {age} years old: {len(older_than)}.")

        # Filter data by Health Conditions
        st.markdown("<h3>Filter data by Health Conditions:</h3>", unsafe_allow_html=True)
        health_conditions_unique = self.database.health_conditions_unique()
        df = data_view("Cologne")
        selected_conditions = st.multiselect("Select Health Conditions", health_conditions_unique)
        filtered_df = df[df['health_conditions'].str.contains('|'.join(selected_conditions))]
        st.dataframe(filtered_df)




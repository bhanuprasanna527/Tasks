import psycopg2
from psycopg2 import sql
import streamlit as st


class ECG_Database:
    def __init__(self, dbname, host='localhost', port=5432):
        """
        Class that manges the database of ECG data of patients.
        Parameters:
            :param dbname: database name - string
        """
        self.conn = psycopg2.connect(dbname=dbname, host=host, port=port)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS ecg (
            id serial PRIMARY KEY,
            date DATE,
            tk_id VARCHAR(10) NOT NULL,
            unit VARCHAR(255) NOT NULL,
            hospital VARCHAR(255) NOT NULL,
            sample_rate INT,
            duration INT,
            health_conditions VARCHAR(255),
            age INT,
            gender VARCHAR(255),
            ecg_signal_data_file_path VARCHAR(255),
            heart_image_file_path VARCHAR(255)
            );
            """
        )
        self.conn.commit()

    def health_conditions_unique(self):
        self.cur.execute("SELECT health_conditions FROM ecg;")
        temp_data = list(self.cur.fetchall())
        temp_data = [i[0].split(',') for i in temp_data]
        flattened_conditions = ','.join([condition for sublist in temp_data for condition in sublist])
        split_conditions = [condition.strip() for condition in flattened_conditions.split(',') if condition.strip()]
        unique_conditions = set(split_conditions)
        print(unique_conditions)
        return list(unique_conditions)

    def add_sample(self, ecg_sample):
        insert_query = sql.SQL(
            """
                INSERT INTO ecg (date, tk_id, unit, hospital, sample_rate, duration, health_conditions, age, gender, 
                ecg_signal_data_file_path, heart_image_file_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
        )

        self.cur.execute(insert_query, (ecg_sample.date, ecg_sample.tk_id, ecg_sample.unit, ecg_sample.hospital, ecg_sample.sample_rate,
                                        ecg_sample.duration, ecg_sample.health_conditions, ecg_sample.age,
                                        ecg_sample.gender, ecg_sample.ecg_signal_data_file_path,
                                        ecg_sample.heart_image_file_path))

        self.conn.commit()

    def delete_samples_in_a_range(self, start_id, end_id):
        delete_query = sql.SQL("DELETE FROM ecg WHERE id BETWEEN %s AND %s")
        self.cur.execute(delete_query, (start_id, end_id))
        self.conn.commit()

    def search_long_samples(self, threshold):
        self.cur.execute("SELECT * FROM ecg WHERE duration >= %s", (threshold,))
        return self.cur.fetchall()

    def count_samples_above_age(self, age):
        self.cur.execute("SELECT * FROM ecg WHERE age >= %s", (age,))
        return self.cur.fetchall()

import psycopg2
from psycopg2 import sql

class ECGSample:
    def __init__(self, tk_id, date, unit, hospital, sample_rate, duration, health_conditions, age, gender,
                 ecg_signal_data_file_path, heart_image_file_path):
        """
        Class that stores a sample of the patient's ECG data.
        Parameters:
            :param tk_id: Unique identifier for the patient.
            :param date: date of ecg sample - datetime object
            :param unit: Unit part of the Hospital - string
            :param hospital: Hospital name - string
            :param sample_rate: Sampling rate - integer
            :param duration: Duration of ecg sample in seconds - integer
            :param health_conditions: Health conditions - string
            :param age: Age of patient - integer
            :param gender: Gender of patient - string
            :param ecg_signal_data_file_path: ECG signal data file path - string
            :param heart_image_file_path: Heart image file path - string
        """
        self.date = date
        self.tk_id = tk_id
        self.unit = unit
        self.hospital = hospital
        self.sample_rate = sample_rate
        self.duration = duration
        self.health_conditions = health_conditions
        self.age = age
        self.gender = gender
        self.ecg_signal_data_file_path = ecg_signal_data_file_path
        self.heart_image_file_path = heart_image_file_path

        def is_long_enough(self, threshold):
            return self.duration >= threshold

        def is_older_than(self, age):
            return self.age >= age

class ECGDatabase:
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
        temp_data = [i[0].split(', ') for i in temp_data]
        set_temp_data = set()
        for i in temp_data:
            for j in i:
                set_temp_data.add(j)
        return list(set_temp_data)

    def add_sample(self, ecg_sample):
        insert_query = sql.SQL(
            """
                INSERT INTO ecg (tk_id, unit, hospital, sample_rate, duration, health_conditions, age, gender, 
                ecg_signal_data_file_path, heart_image_file_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
        )

        self.cur.execute(insert_query, (ecg_sample.tk_id, ecg_sample.unit, ecg_sample.hospital, ecg_sample.sample_rate,
                                        ecg_sample.duration, ecg_sample.health_conditions, ecg_sample.age,
                                        ecg_sample.gender, ecg_sample.ecg_signal_data_file_path,
                                        ecg_sample.heart_image_file_path))

        self.conn.commit()


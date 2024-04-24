class ECG_Sample:
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
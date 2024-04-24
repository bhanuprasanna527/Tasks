# Tasks

All the notebooks, files and data regarding the tasks are present in this git repository.
 
## Task 1

For the first task which is to store data in a smart way and get the required data quickly.

I have implemented a Streamlit website where filtering data to get the required reports immediately is just a click away.

The following operations have been implemented:

    1) Add new data with heart images and signal data. The heart images and signal data are organised and the file paths are stored in PostgreSQL database.
    
    2) Filter data on any column. Data can be filtered based on Age, Gender, Health Conditions, Hospital, and the respective unit of the hospital.

Here is a short video of demonstration:

[The video is on YouTube! Note - File size was large.](https://www.youtube.com/watch?v=MCI3USxwat0&ab_channel=Bhanuprasanna)


## Task 2

For Task 2, I have worked with the ECG Fragments dataset and have built a classifier using <b>CNN</b> for classifying between fragments that contain a Ventricular Flutter or Fibrillation and the ones that do not.

The notebook is available [here](https://github.com/bhanuprasanna527/Tasks/blob/main/Task%202/Task%202.ipynb).

The accuracy achieved by CNN on Test data is <b>94.48%</b>. This accuracy was achieved by saving the best model using training where I have early stopping method to save the best model. The training and validation graphs are shown below:

<img width="595" alt="Screenshot 2024-04-24 at 7 30 48 PM" src="https://github.com/bhanuprasanna527/Tasks/assets/63473951/dd7fb22b-3f64-4d0c-9644-6653551eb514">

The Classification report on the Test Data is as follows:

<img width="454" alt="Screenshot 2024-04-24 at 7 41 35 PM" src="https://github.com/bhanuprasanna527/Tasks/assets/63473951/82bdfb20-f068-4947-b0da-a2108f2c9256">

The below are the Accuracy, Precision, Recall, F1-score, and ROC-AUC results obtained from the model:

<img width="253" alt="Screenshot 2024-04-24 at 7 41 51 PM" src="https://github.com/bhanuprasanna527/Tasks/assets/63473951/7c301ab8-13fe-4dae-8641-ddb860466bb4">

___

I have also implemented the same model using K Fold Cross Validation technique which is used to find the best performing model by iteratively working on a portion of the data. This helps to overcome the problem of Overfitting and also assess and identify the best performing model.

The results are as follows:

Number of times K-Fold is done: 5
Number of Best Models saved: 5

The accuracy of the 5 models using Test data: [0.86614, 0.94488, 0.89763, 0.91338, 0.92125]

The mean accuracy of the 5 models is: <b>0.90866<b>

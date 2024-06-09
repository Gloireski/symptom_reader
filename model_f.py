from statistics import mode

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# from scipy.stats import mode
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.metrics import accuracy_score, confusion_matrix

DATA_PATH = "Training.csv"
data = pd.read_csv(DATA_PATH).dropna(axis=1)

# # Encoding the target value into numerical
# # value using LabelEncoder
encoder = LabelEncoder()
data["prognosis"] = encoder.fit_transform(data["prognosis"])
X = data.iloc[:, :-1]
y = data.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=24)

# Training the models on whole data
final_svm_model = SVC()
final_nb_model = GaussianNB()
final_rf_model = RandomForestClassifier(random_state=18)
final_svm_model.fit(X.values, y)
final_nb_model.fit(X.values, y)
final_rf_model.fit(X.values, y)

# Reading the test data
test_data = pd.read_csv("Testing.csv").dropna(axis=1)

test_X = test_data.iloc[:, :-1]
test_Y = encoder.transform(test_data.iloc[:, -1])

symptoms = X.columns.values
# Creating a symptom index dictionary to encode the
# input symptoms into numerical form
symptom_index = {}
for index, value in enumerate(symptoms):
    symptom = " ".join([i.capitalize() for i in value.split("_")])
    symptom_index[symptom] = index
# print(symptoms)
data_dict = {
    "symptom_index": symptom_index,
    "predictions_classes": encoder.classes_
}

# print(data_dict)


# Defining the Function
# Input: string containing symptoms separated by commas
# Output: Generated predictions by models
def predict_disease(in_symptoms):
    in_symptoms = in_symptoms.split(",")
    # creating input data for the models
    input_data = [0] * len(data_dict["symptom_index"])
    for in_symptom in in_symptoms:
        in_index = data_dict["symptom_index"][in_symptom]
        input_data[in_index] = 1

    # reshaping the input data and converting it
    # into suitable format for model predictions
    input_data = np.array(input_data).reshape(1, -1)

    # generating individual outputs
    rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[0]]
    nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[0]]
    svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_data)[0]]

    # making final prediction by taking mode of all predictions
    final_prediction = mode([rf_prediction, nb_prediction, svm_prediction])
    # r = mode(['Fungal infection', 'nb_prediction', 'nb_prediction'])
    # print(r)
    predictions = {
        "rf_model_prediction": rf_prediction,
        "naive_bayes_prediction": nb_prediction,
        "svm_model_prediction": svm_prediction,
        "final_prediction": final_prediction
    }
    # print(predictions)
    return final_prediction
    # return predictions

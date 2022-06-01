import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from sklearn.compose import ColumnTransformer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer
from tensorflow.keras.layers import Dense
import numpy as np
import csv
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers import Adam
from PIL import Image


data_file = pd.read_csv("./dataset/pieces_train.csv", encoding="utf-8", sep=";",header=None)
df = pd.DataFrame(data_file)

labels = df.iloc[:,0]
features = df.iloc[:, 1:]
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.2, random_state=23)
numerical_features = features.select_dtypes(include=['float64'])

def get_my_model():
    my_model = Sequential()
    input = InputLayer(input_shape=(1200, ))
    my_model.add(input)
    my_model.add(Dense(1, activation='relu'))
    opt = Adam(learning_rate=0.01)
    my_model.compile(loss='mse', metrics=['mae'], optimizer=opt)
    my_model.fit(np.asarray(features_train).astype('float64'), np.asarray(labels_train).astype('float64'), epochs=20, batch_size=1)
    return my_model

def decoding(num):
    pieces = ["pw","pb","tw","tb","cw","cb","fw","fb","dw", "db",
        "rw","rb","sw","sb"]
    return pieces[num]

def get_matrix_nn(img, n):
    matrix = []
    for i in range(0, 400, 50):
        inner_list = []
        for j in range(0, 400, 50):
            pos = (j, i, j+50, i+50)
            crop = img.crop(pos)
            resized = crop.resize((20, 20))
            data = np.array(resized).flatten()
            normalize_func = np.vectorize(lambda t: t ** 1/255)
            all_values = normalize_func(data)
            input = (np.asfarray(all_values)) + 0.01
            formated_input = [[x for x in input]]
            outputs = n.predict(formated_input)
            final_output = round(max(outputs[0]))
            inner_list.append(decoding(final_output))
        matrix.append(inner_list)
    return matrix

def get_score(mat, correct):
    cor = correct
    score = 0
    for i in range(len(mat)):
        for j in range(len(mat)):
            if mat[i][j] == cor[i][j]:
                score += 1
    return score

def get_value(n, value):
    img = Image.open(f"./created_boards/new_board{value}.png")
    resize_img = img.resize((400, 400))
    csv_data = pd.read_csv("./dataset/created_boards.csv", encoding="utf-8", sep=";", header=None)
    correct_mat = []
    correct_mat = np.split(np.array(csv_data.iloc[value]), 8)
    matrix = get_matrix_nn(resize_img, n)
    result = get_score(matrix, correct_mat)
    print(matrix)
    print(correct_mat)
    print("Result: " + str(result))
    return result

model = get_my_model()
result = get_value(model, 0)

# results = []
# for i in range(10):
#     result = get_value(model, i)
#     results.append(result)
#     print("new_game")
# print(results)
# mean = sum(results) / len(results)
# print(mean)
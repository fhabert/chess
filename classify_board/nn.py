import matplotlib.pyplot as plt
import numpy
import scipy.special
from PIL import Image
import pandas as pd
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import numpy as np

class neuralNetwork:

    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        self.inodes = input_nodes
        self.onodes = output_nodes
        self.hnodes = hidden_nodes
        self.lr = learning_rate
        self.wih = numpy.random.normal(0.0, pow(self.hnodes, - 0.5), (self.hnodes, self.inodes))
        self.who = numpy.random.normal(0.0, pow(self.onodes, - 0.5), (self.onodes, self.hnodes))
        self.activation_function = lambda x: scipy.special.expit(x)
        pass

    def train(self, inputs_list, targets_list):
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T
        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        output_errors = targets - final_outputs
        hidden_errors = numpy.dot(self.who.T, output_errors)
        self.who += self.lr * numpy.dot(output_errors * final_outputs * (1 - final_outputs), numpy.transpose(hidden_outputs))
        self.wih += self.lr * numpy.dot(hidden_errors * hidden_outputs * (1 - hidden_outputs), numpy.transpose(inputs))
        pass

    def query(self, inputs_list):
        inputs = numpy.array(inputs_list, ndmin = 2).T
        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        return final_outputs

# input_nodes = 1200
# hidden_nodes = 140
# output_nodes = 14
# learning_rate = 0.3
# trials_scores = []
# images = []

# n = neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

# data_file = pd.read_csv("./dataset/pieces_train.csv", encoding="utf-8", sep=";",header=None)
# train_file = pd.DataFrame(data_file)

# epochs = 50

# for _ in range(epochs):
#     for i in range(len(train_file)):
#         all_values = train_file.iloc[i]
#         inputs = (numpy.asfarray(all_values[1:])) + 0.01
#         targets = numpy.zeros(output_nodes) + 0.01
#         targets[int(float(all_values[0]))-1] = 0.99
#         n.train(inputs, targets)

# def test():
#     test_data = pd.read_csv('./dataset/pieces_test.csv',encoding="utf-8", sep=";",header=None)
#     test_list = pd.DataFrame(test_data)

#     score_card = []
#     for i in range(len(test_list)):
#         all_values = list(test_list.iloc[i])
#         correct_label = int(all_values[0])
#         inputs = (numpy.asfarray(all_values[1:])) + 0.01
#         outputs = n.query(inputs)
#         label = numpy.argmax(outputs)
#         if (label == correct_label):
#             score_card.append(1)
#         else:
#             score_card.append(0)

    # scored_array = numpy.asarray(score_card)
    # print("performance: ", scored_array.sum()/scored_array.size)

def decoding(num):
    pieces = ["pw","pb","tw","tb","cw","cb","fw","fb","dw", "db",
        "rw","rb","sw","sb"]
    return pieces[num]
    
    
def get_matrix(img, n):
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
            inputs = (numpy.asfarray(all_values)) + 0.01
            outputs = n.query(inputs)
            label = numpy.argmax(outputs)
            inner_list.append(decoding(label))
        matrix.append(inner_list)
    return matrix

def get_score(mat, correct):
    cor = correct
    score = 0
    for i in range(len(mat)):
        for j in range(len(mat)):
            if mat[i][j] == cor[i][j]:
                score += 1
    result = int(score / (len(mat) * len(mat))*100)
    return result

def get_value(n, value):
    img = Image.open(f"./created_boards/new_board{value}.png")
    csv_data = pd.read_csv("./dataset/created_boards.csv", encoding="utf-8", sep=";")
    correct_mat = []
    correct_mat = np.split(np.array(csv_data.iloc[value-1]), 8)
    scores = []
    matrix = get_matrix(img, n)
    result = get_score(matrix, correct_mat)
    scores.append(result)
    print("Result: " + str(result))
    mid_score = round(sum(scores) / len(scores))
    return mid_score, scores

# print(get_value(1))

def obtain_best_lr():
    results = {"0.1": [], "0.3": [], "0.5": []}
    inp_nodes = 1200
    hid_nodes = 400
    out_nodes = 14
    data_file = pd.read_csv("./dataset/pieces_train.csv", encoding="utf-8", sep=";",header=None)
    train_file = pd.DataFrame(data_file)
    learning_rates = [0.1, 0.3, 0.5]
    epochs = [x for x in range(15, 35, 5)]
    for lr in learning_rates:
        for ep in epochs:
            n = neuralNetwork(inp_nodes, hid_nodes, out_nodes, lr)
            for _ in range(ep):
                for i in range(len(train_file)):
                    all_values = train_file.iloc[i]
                    inputs = (numpy.asfarray(all_values[1:])) + 0.01
                    targets = numpy.zeros(out_nodes) + 0.01
                    targets[int(float(all_values[0]))-1] = 0.99
                    n.train(inputs, targets)
            result = get_value(n, 1)
            results[str(lr)].append(result)
        print(f"{lr} Learning Rate")
    return results

def get_graphs(graph, title):
    fig = plt.figure(figsize=(8, 6))
    fig.suptitle(title)
    axes = []
    epochs = [x for x in range(15, 35, 5)]
    axes_val = [x for x in range(231, 234, 1)]
    for item in axes_val:
        axes.append(fig.add_subplot(item))
    learning_rates = ["0.1", "0.3", "0.5"]
    colors = ['b', 'g', 'r']
    for i in range(len(axes)):
        axes[i].plot(epochs, graph[learning_rates[i]], color=colors[i])
        axes[i].set_title(f"{learning_rates[i]} Learning Rate")
        axes[i].set_ylim([0, 100])
        axes[i].set_ylabel("Correct Values")
        axes[i].set_xlabel("Number of epochs")
    plt.tight_layout()
    plt.savefig("./graphs/learning_rates.png")

# graph = {'0.1': [3, 15, 14, 23], 
#         '0.3': [25, 3, 28, 26], 
#         '0.5': [1, 1, 3, 1]}

# title = "Assessing the lr on different epochs (75 bo/ 400 hn)"
# graph = obtain_best_lr()
# get_graphs(graph, title)

inp_nodes = 1200
hid_nodes = 300
out_nodes = 14
data_file = pd.read_csv("./dataset/pieces_train.csv", encoding="utf-8", sep=";",header=None)
train_file = pd.DataFrame(data_file)
epochs = 25
n = neuralNetwork(inp_nodes, hid_nodes, out_nodes, 0.3)
for _ in range(epochs):
    for i in range(len(train_file)):
        all_values = train_file.iloc[i]
        inputs = (numpy.asfarray(all_values[1:])) + 0.01
        targets = numpy.zeros(out_nodes) + 0.01
        targets[int(float(all_values[0]))-1] = 0.99
        n.train(inputs, targets)
    print("new epochs")
result, scores = get_value(n, 1)
print(result, scores)
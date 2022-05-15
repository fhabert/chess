### PAS UTILISE

# import matplotlib.pyplot as plt
# import numpy
# import scipy.special
# import pandas as pd
# import numpy as np

# class neuralNetwork:

#     def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
#         self.inodes = input_nodes
#         self.onodes = output_nodes
#         self.hnodes = hidden_nodes
#         self.lr = learning_rate
#         self.wih = numpy.random.normal(0.0, pow(self.hnodes, - 0.5), (self.hnodes, self.inodes))
#         self.who = numpy.random.normal(0.0, pow(self.onodes, - 0.5), (self.onodes, self.hnodes))
#         self.activation_function = lambda x: scipy.special.expit(x)
#         pass

#     def train(self, inputs_list, targets_list):
#         inputs = numpy.array(inputs_list, ndmin=2).T
#         targets = numpy.array(targets_list, ndmin=2).T
#         hidden_inputs = numpy.dot(self.wih, inputs)
#         hidden_outputs = self.activation_function(hidden_inputs)
#         final_inputs = numpy.dot(self.who, hidden_outputs)
#         final_outputs = self.activation_function(final_inputs)
#         output_errors = targets - final_outputs
#         hidden_errors = numpy.dot(self.who.T, output_errors)
#         self.who += self.lr * numpy.dot(output_errors * final_outputs * (1 - final_outputs), numpy.transpose(hidden_outputs))
#         self.wih += self.lr * numpy.dot(hidden_errors * hidden_outputs * (1 - hidden_outputs), numpy.transpose(inputs))
#         pass

#     def query(self, inputs_list):
#         inputs = numpy.array(inputs_list, ndmin = 2).T
#         hidden_inputs = numpy.dot(self.wih, inputs)
#         hidden_outputs = self.activation_function(hidden_inputs)
#         final_inputs = numpy.dot(self.who, hidden_outputs)
#         final_outputs = self.activation_function(final_inputs)
#         return final_outputs

# input_nodes = 1200
# hidden_nodes = 150
# output_nodes = 14
# lr = 0.3
# learning_rates = np.arange(0.1, 1, 0.1, dtype=float)
# scores = []
# best_rate = 0
# best_score = 0

# for learning_rate in learning_rates:
#     n = neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

#     data_file = pd.read_csv("./dataset/pieces_train.csv", encoding="utf-8", sep=";",header=None)
#     train_file = pd.DataFrame(data_file)

#     epochs = 20

#     for e in range(epochs):
#         for i in range(len(train_file)):
#             all_values = train_file.iloc[i]
#             inputs = (numpy.asfarray(all_values[1:])) + 0.01
#             targets = numpy.zeros(output_nodes) + 0.01
#             targets[int(float(all_values[0]))-1] = 0.99
#             n.train(inputs, targets)

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
    
#     scored_array = numpy.asarray(score_card)
#     actual_score = scored_array.sum()/scored_array.size
#     scores.append(actual_score)
#     print("Learning rate: " + str(learning_rate) + " " + "-" + " " + str(actual_score))
#     if actual_score > best_score:
#         best_score =  actual_score
#         best_rate = learning_rate

# # print("performance: ", scored_array.sum()/scored_array.size)
# print("Best score: " + str(best_score))
# print("Best rate: " + str(best_rate))

# # learning rate to use: 0.3
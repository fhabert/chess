import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import matplotlib.image as mpimg
from PIL import Image
import pandas as pd
import csv
from sklearn.utils import shuffle
import chess_piece

batch_size = 32
img_height = 20
img_width = 20

train_ds = tf.keras.utils.image_dataset_from_directory(
  "./chess_pieces",
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

encoding = {}
class_names = list(chess_piece.pieces.keys())
for i in range(len(class_names)):
  encoding[class_names[i]] = i

decoding = {}
class_names = list(chess_piece.pieces.keys())
for i in range(len(class_names)):
  encoding[i] = class_names[i]

def create_diagram():
  fig = plt.figure(figsize=(8, 8))
  columns = 2
  rows = 6
  count = 1
  for keys, values in chess_piece.pieces.items():
    resize_img = values[0].resize((80, 80))
    fig.add_subplot(rows, columns, count)
    plt.imshow(resize_img)
    plt.title(keys)
    plt.axis("off")
    count += 1
  plt.show()


def get_board_diagram():
  fig = plt.figure(figsize=(8, 8))
  rows = 1
  columns = 2
  fig.add_subplot(rows, columns, 1)
  img = Image.open("./created_boards/new_board1.png")
  csv_data = pd.read_csv("./dataset/created_boards.csv", encoding="utf-8", sep=";",header=None)
  matrix = np.split(np.array(csv_data.iloc[0]), 8)
  table = plt.table(cellText=matrix, loc='right', colWidths=[0.18 for _ in matrix], cellLoc='center')
  table.set_fontsize(15)
  table.scale(1, 4)
  plt.imshow(img)
  plt.title("Image and matrix of the board", pad=20)
  plt.axis("off")
  plt.show()


def get_excel_pieces():
  temp = []
  for key, _ in chess_piece.pieces.items():
    for i in range(len(chess_piece.pieces[key])):
      img = load_img(f"./chess_pieces/{key}/{key}{i}.png")
      data = img_to_array(img)
      temp.append((key, data))
  # mixt_images = temp
  mixt_images = shuffle(temp, random_state=0)
  num = round(len(temp)*0.8)
  with open('./dataset/pieces_train.csv', 'w', newline='') as f:
    for item in mixt_images[:num]:
      row = np.array(item[1]).flatten()
      normalize_func = np.vectorize(lambda t: t ** 1/255)
      new_row = normalize_func(row)
      top_row = np.insert(new_row, 0, encoding[item[0]])
      writer = csv.writer(f)
      writer.writerow(top_row)
    f.close()
  with open('./dataset/pieces_test.csv', 'w', newline='') as f:
    for item in mixt_images[num:]:
      row = np.array(item[1]).flatten()
      normalize_func = np.vectorize(lambda t: t ** 1/255)
      new_row = normalize_func(row)
      top_row = np.insert(new_row, 0, encoding[item[0]])
      writer = csv.writer(f)
      writer.writerow(top_row)
    f.close()
  pass

def get_excel_boards():
  temp = []
  for i in range(1, 100, 1):
    img = load_img(f"./resized_boards/new_board{i}.png")
    data = img_to_array(img)
    temp.append(data)
  num = round(len(temp)*0.8)
  with open('./dataset/created_boards_train.csv', 'w', newline='') as f:
    for item in temp[:num]:
      row = np.array(item).flatten()
      normalize_func = np.vectorize(lambda t: t ** 1/255)
      new_row = normalize_func(row)
      writer = csv.writer(f)
      writer.writerow(new_row)
    f.close()
  with open('./dataset/created_boards_test.csv', 'w', newline='') as f:
    for item in temp[num:]:
      row = np.array(item).flatten()
      normalize_func = np.vectorize(lambda t: t ** 1/255)
      new_row = normalize_func(row)
      writer = csv.writer(f)
      writer.writerow(new_row)
    f.close()
  pass
    
get_excel_pieces()
# get_excel_boards()
# create_diagram()
# get_board_diagram()


  # temp = []
  # for key, _ in chess_piece.pieces.items():
  #   count = 0
  #   for _ in chess_piece.pieces[key]:
  #     img = load_img(f"../chess_pieces/{key}/{key}{count}.png")
  #     data = img_to_array(img)
  #     temp.append((key, data))
  #     count += 1
  # # mixt_images = shuffle(temp, random_state=0)
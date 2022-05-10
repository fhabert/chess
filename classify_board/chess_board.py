import numpy as np
import random
from sklearn.utils import shuffle
import csv
from PIL import Image

COLUMNS = 8
LINES = 8
COUNT = 1

images = [[0]*LINES for _ in range(LINES)]

def get_board():
    board = []
    for i in range(LINES):
        inner_board = []
        for j in range(COLUMNS):
            inner_board.append(0)
        board.append(inner_board)
    for i in range(LINES):
        board[1][i] = "pb"
        board[6][i] = "pw"
    black_s = ["tb", "cb", 0, "db", "rb", 0, "cb", "tb"]
    white_s = ["tw", "cw", 0, "dw", "rw", 0, "cw", "tw"]
    for i in range(LINES):
        board[0][i] = black_s[i] 
        board[7][i] = white_s[i]
    return board

def images_board(board):
    b = board
    array_images = []
    images_pos = []
    for i in range(0, 400, 50):
        inner_list = []
        for j in range(0, 400, 50):
            pos = (j, i, j+50, i+50)
            inner_list.append(pos)
        images_pos.append(inner_list)
    for i in range(len(b)):
        inner_images = []
        for j in range(len(b[i])):
            if b[i][j] != "sw" and b[i][j] != "sb":
                url = f"./unique_pieces/{b[i][j]}.png"
                img = Image.open(url)
                resize_img = img.resize((50, 50))
                inner_images.append(resize_img)
            else:
                inner_images.append(0)
        array_images.append(inner_images)
    new_list = [[(array_images[i][j], images_pos[i][j]) for i in range(len(images_pos))] for j in range(len(images_pos))]
    reconstruct_image(new_list)

def pos_fou():
    fb = []
    fw = []
    for i in range(LINES):
        for j in range(COLUMNS):
            if i + j % 2 == 0:
                fw.append((i, j))
            elif i + j % 2 != 0:
                fb.append((i, j))
    return random.choices(fb, k=2), random.choices(fw, k=2)

def shuffle_board():
    fb, fw = pos_fou()
    actual_board = []
    board = get_board()
    valid = True
    for item in fb:
        temp = board[item[0]][item[1]]
        board[item[0]][item[1]] = "fb"
        for i in range(LINES):
            for j in range(COLUMNS):
                if valid and (board[i][j] == 0) :
                    index = (i, j)
                    valid = False
        board[index[0]][index[1]] = temp
    valid = True
    for item in fw:
        temp = board[item[0]][item[1]]
        board[item[0]][item[1]] = "fw"
        for i in range(LINES):
            for j in range(COLUMNS):
                if valid and (board[i][j] == 0):
                    index = (i, j)
                    valid = False
        board[index[0]][index[1]] = temp
    for item in board:
        for piece in item:
            actual_board.append(piece)
    shuffle_board = shuffle(actual_board)
    for i in range(len(shuffle_board)):
        if shuffle_board[i] == 0 and i % 2 == 0:
            shuffle_board[i] = "sw"
        elif shuffle_board[i] == 0 and i % 2 == 1:
            shuffle_board[i] = "sb"
    outer_li = []
    inner_li = []
    counter = 0
    for i in range(len(shuffle_board)):
        inner_li.append(shuffle_board[i])
        if len(inner_li) == 8:
            outer_li.append(inner_li)
            inner_li = []
            counter += 1
    return outer_li

def reconstruct_image(images):
    set_img = images
    new_image = Image.open("./full_game/empty_board.png")
    for i in range(len(set_img)):
        for j in range(len(set_img)):
            if set_img[i][j][0] != 0:
                new_image.paste(set_img[i][j][0], set_img[i][j][1], set_img[i][j][0])
    new_image.save(f"./created_boards/new_board{COUNT}.png")
    # resized_img = new_image.resize((20, 20))
    # resized_img.save(f"./resized_boards/new_board{COUNT}.png")
    # new_image.show()
    pass

def create_csv(b):
    board = np.array(b).flatten()
    with open('./dataset/created_boards.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(board)
    f.close()

for i in range(100):
    board = shuffle_board()
    img = images_board(board)
    create_csv(board)
    COUNT += 1

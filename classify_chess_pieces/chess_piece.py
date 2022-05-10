from PIL import Image
import pandas as pd

created_images = []
created_boards_img = []
pieces = {
    "pw": [],
    "pb": [],
    "tw": [],
    "tb": [],
    "cw": [],
    "cb": [],
    "fw": [],
    "fb": [],
    "dw": [],
    "db": [],
    "rw": [],
    "rb": [],
    "sw": [],
    "sb": []
}

black_positions = [("tb", (0, 0, 50, 50)), ("cb", (50, 0, 100, 50)), ("fb", (100, 0, 150, 50)),
                ("db", (150, 0, 200, 50)), ("rb", (200, 0, 250, 50)), ("pb", (0, 50, 50, 100)), ("sb", (50, 100, 100, 150))]

white_positions = [("tw", (0, 350, 50, 400)), ("cw", (50, 350, 100, 400)), ("fw", (100, 350, 150, 400)),
                ("dw", (150, 350, 200, 400)), ("rw", (200, 350, 250, 400)), ("pw", (0, 300, 50, 350)), ("sw", (0, 100, 50, 150))]

for i in range(1,14,1):
    target = f"./full_game/game{i}.png"
    image = Image.open(target)
    resize = image.resize((400, 400))
    created_images.append(resize)

for i in range(1, 61, 1):
    target = f"./created_boards/new_board{i}.png"
    image = Image.open(target)
    resize = image.resize((400, 400))
    created_boards_img.append(resize)

data = pd.read_csv("./dataset/created_boards.csv", encoding="utf-8", sep=";", header=None)
games = data.iloc[:60]
count = 0
images_pos = []

for i in range(0, 400, 50):
    inner_list = []
    for j in range(0, 400, 50):
        pos = (j, i, j+50, i+50)
        inner_list.append(pos)
    images_pos.append(inner_list)

count = 0
for k in range(len(created_boards_img)):
    for i in range(len(images_pos)):
        for j in range(len(images_pos)):
            img = created_boards_img[k].crop(images_pos[i][j])
            resize_item = img.resize((20, 20))
            index = list(games.iloc[k])[count]
            pieces[index].append(resize_item)
            count += 1
    count = 0

for item in created_images:
    for b_piece in black_positions:
        img = item.crop(b_piece[1])
        resize_item = img.resize((20, 20))
        pieces[b_piece[0]].append(resize_item)
    for w_piece in white_positions:
        img = item.crop(w_piece[1])
        resize_item = img.resize((20, 20))
        pieces[w_piece[0]].append(resize_item)

for key, _ in pieces.items():
    count = 0
    for item in pieces[key]:
        item.save(f"./chess_pieces/{key}/{key}{count}.png")
        count += 1

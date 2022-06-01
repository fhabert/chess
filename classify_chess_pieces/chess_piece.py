from PIL import Image
import pandas as pd
import os

COLUMNS = 8
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


names = []
images = []
for key,  _ in pieces.items():
    names.append(key)
big_img = Image.open("./full_game/game4.png")
resize = big_img.resize((400, 400))
for _ in range(30):
    for i in range(12):
        img_w = resize.crop((0, 100, 50, 150))
        img_b = resize.crop((50, 100, 100, 150))
        resize_item_w = img_w.resize((20, 20))
        resize_item_b = img_b.resize((20, 20))
        img = Image.open(f"./unique_pieces/{names[i]}.png")
        img_res = img.resize((50, 50))
        img_w.paste(img_res,img_res)
        img_w_res = img_w.resize((20, 20))
        img_b.paste(img_res,img_res)
        img_b_res = img_b.resize((20, 20))
        pieces[names[i]].append(img_w_res)
        pieces[names[i]].append(img_b_res)

    img_w = resize.crop((0, 100, 50, 150))
    img_b = resize.crop((50, 100, 100, 150))
    pieces["sw"].append(img_w.resize((20, 20)))
    pieces["sb"].append(img_b.resize((20, 20)))
    pieces["sw"].append(img_w.resize((20, 20)))
    pieces["sb"].append(img_b.resize((20, 20)))


for key, _ in pieces.items():
    dir = f'./chess_pieces/{key}'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

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
        if count < 100:
            item.save(f"./chess_pieces/{key}/{key}{count}.png")
        count += 1





import gc

COLUMNS = 8
LINES = 8

class Game(object):
    def __init__(self):        
        self.board = [[0]*LINES for i in range(LINES)]
        self.initiate_board()
        self.turn = "white"
        self.pieceTaken = []
        self.posDir = self.checkDir()
        pass

    def checkDir(self):
        posDir = []
        for i in range(COLUMNS):
            for j in range(LINES):
                if self.board[i][j] == 0:
                    posDir.append((i, j))
        return posDir


    def initiate_board(self):
        for i in range(LINES):
            self.board[1][i] = "pb"
            self.board[6][i] = "pw"
        black_s = ["tb", "cb", "fb", "db", "rb", "fb", "cb", "tb"]
        white_s = ["tw", "cw", "fw", "dw", "rw", "fw", "cw", "tw"]
        for i in range(LINES):
            self.board[0][i] = black_s[i] 
            self.board[7][i] = white_s[i]
        pass

    def makeMove(self, piecePos, nextPos):
        name = self.board[piecePos[0]][piecePos[1]]
        if "p" in name:
            piece = Pion(piecePos)
        elif "t" in name:
            piece = Tour(piecePos)
        elif "f" in name:
            piece = Fou(piecePos)
        elif "d" in name:
            piece = Dame(piecePos)
        elif "r" in name:
            piece = Roi(piecePos)
        elif "c" in name:
            piece = Cheval(piecePos)
        posDir = piece.posDir
        if nextPos in posDir:
            temp = self.board[nextPos[0]][nextPos[1]]
            if temp != 0:
                self.pieceTaken.append(temp)
            self.board[nextPos[0]][nextPos[1]] = name
            self.board[piecePos[0]][piecePos[1]] = 0
            self.posDir
            del piece
            gc.collect()
            return True
        else:
            return False
        

game = Game()

def draw_game():
    for i in range(COLUMNS):
        for j in range(19):
            if j == 0:
                print("\n", "--", end="")
            print("--", end="")
        for j in range(LINES):
            if j == 0:
                print("\n", end="")
            print("| ", end="")
            if game.board[i][j] == 0:
                print(" 0", end="")
            else:
                print(game.board[i][j], end="")
            print(" ", end="")
        print("|", end="")
    pass

class Pion():
    def __init__(self, pos):
        self.pos = pos
        self.posDir = self.checkDir()
    
    def checkDir(self):
        posDir = []
        i = self.pos[0]
        j = self.pos[1]
        if i > 0 and j < 7:
            if game.turn == "black":
                if i == 6 and game.board[i-2][j] == 0:
                    posDir.append((i-2, j))
                if game.board[i-1][j] == 0:
                    posDir.append((i-1, j))
                if j > 0 and j < 7:
                    if game.board[i-1][j-1] != 0 and "w" in game.board[i-1][j-1]:
                        posDir.append((i-1, j-1))
                    if game.board[i-1][j+1] != 0 and "w" in game.board[i-1][j+1]:
                        posDir.append((i-1, j+1))
                if j == 0 and (game.board[i-1][j+1] != 0 and "w" in game.board[i-1][j+1]):
                    posDir.append((i-1, j+1))
                if j == 7 and (game.board[i-1][j-1] != 0 and "w" in game.board[i-1][j-1]):
                    posDir.append((i-1, j-1))
            else:
                if i == 1 and game.board[i+2][j] == 0:
                    posDir.append((i+2, j))
                if game.board[i+1][j] == 0:
                    posDir.append((i+1, j))
                if j > 0 and j < 7:
                    if game.board[i+1][j-1] != 0 and "b" in game.board[i+1][j-1]:
                        posDir.append((i+1, j-1))
                    if game.board[i+1][j+1] != 0 and "b" in game.board[i+1][j+1]:
                        posDir.append((i+1, j+1))
                if j == 0 and (game.board[i+1][j+1] != 0 and "b" in game.board[i+1][j+1]):
                    posDir.append((i+1, j+1))
                if j == 7 and (game.board[i+1][j-1] != 0 and "b" in game.board[i+1][j-1]):
                    posDir.append((i+1, j-1))
        return posDir

class Tour():
    def __init__(self, pos):
        self.pos = pos
        self.posDir = self.checkDir()
    
    def checkDir(self):
        posDir = []
        i = self.pos[0]
        j = self.pos[1]
        if game.turn == "black":
            while (i < 7 and game.board[i+1][j] == 0) or (game.board[i+1][j] != 0 and "w" in game.board[i+1][j]):
                i += 1
                posDir.append((i, j))
                if i < 7 and game.board[i+1][j] != 0 and "w" in game.board[i+1][j]:
                    posDir.append((i, j))
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (i > 0 and game.board[i-1][j] == 0) or (game.board[i-1][j] != 0 and "w" in game.board[i-1][j]):
                i -= 1
                posDir.append((i, j))
                if i > 0 and game.board[i-1][j] != 0 and "w" in game.board[i-1][j]:
                    posDir.append((i, j))
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (j > 0 and game.board[i][j-1] == 0) or (game.board[i][j-1] != 0 and "w" in game.board[i][j-1]):
                j -= 1
                posDir.append((i, j))
                if j > 0 and game.board[i][j-1] != 0 and "w" in game.board[i][j-1]:
                    posDir.append((i, j))
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (j < 7 and game.board[i][j+1] == 0) or (game.board[i][j+1] != 0 and "w" in game.board[i][j+1]):
                j += 1
                posDir.append((i, j))
                if j < 0 and game.board[i][j+1] != 0 and "w" in game.board[i][j+1]:
                    posDir.append((i, j))
                    break
            i = self.pos[0]
            j = self.pos[1]
        else:
            while (i < 7 and game.board[i+1][j] == 0) or (game.board[i+1][j] != 0 and "b" in game.board[i+1][j]):
                i += 1
                posDir.append((i, j))
                if i < 7 and game.board[i+1][j] != 0 and "b" in game.board[i+1][j]:
                    posDir.append((i, j))
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (i > 0 and game.board[i-1][j] == 0) or (game.board[i-1][j] != 0 and "b" in game.board[i-1][j]):
                i -= 1
                posDir.append((i, j))
                if i > 0 and game.board[i-1][j] != 0 and "b" in game.board[i-1][j]:
                    posDir.append((i, j))
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (j > 0 and game.board[i][j-1] == 0) or (game.board[i][j-1] != 0 and "b" in game.board[i][j-1]):
                j -= 1
                posDir.append((i, j))
                if j > 0 and game.board[i][j-1] != 0 and "b" in game.board[i][j-1]:
                    posDir.append((i, j))
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (j < 0 and game.board[i][j+1] == 0) or (game.board[i][j+1] != 0 and "b" in game.board[i][j+1]):
                j += 1
                posDir.append((i, j))
                if j < 0 and game.board[i][j+1] != 0 and "b" in game.board[i][j+1]:
                    posDir.append((i, j))
                    break
        return posDir


class Fou:
    def __init__(self, pos):
        self.pos = pos
        self.posDir = self.checkDir()

    def checkDir(self):
        posDir = []
        i = self.pos[0]
        j = self.pos[1]
        if game.turn == "black":
            while (i < 7 and j < 7 and game.board[i+1][j+1] == 0) or (game.board[i+1][j+1] != 0 and "w" in game.board[i+1][j+1]):
                i += 1
                j += 1
                posDir.append((i, j))
                if i < 7 and j < 7 and game.board[i+1][j+1] != 0 and "w" in game.board[i+1][j+1]:
                    posDir.append((i, j))
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (i > 0 and j < 7 and game.board[i-1][j+1] == 0) or (game.board[i-1][j+1] != 0 and "w" in game.board[i-1][j+1]):
                j += 1
                i -= 1
                posDir.append((i, j))
                if i > 0 and j < 7 and game.board[i-1][j+1] != 0 and "w" in game.board[i-1][j+1]:
                    posDir.append((i, j))
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (j > 0 and i < 7 and game.board[i+1][j-1] == 0) or (game.board[i+1][j-1] != 0 and "w" in game.board[i+1][j-1]):
                print(j, i)
                i += 1
                j -= 1
                posDir.append((i, j))
                if j > 0 and i < 7 and game.board[i+1][j-1] != 0 and "w" in game.board[i+1][j-1]:
                    posDir.append((i, j))
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (j > 0 and i > 0 and game.board[i-1][j-1] == 0) or (game.board[i-1][j-1] != 0 and "w" in game.board[i-1][j-1]):
                i -= 1
                j -= 1
                posDir.append((i, j))
                if j > 0 and i > 0 and game.board[i-1][j-1] != 0 and "w" in game.board[i-1][j-1]:
                    posDir.append((i, j))
                    break
            i = self.pos[0]
            j = self.pos[1]
        else:
            while (i < 7 and j < 7 and game.board[i+1][j+1] == 0) or (game.board[i+1][j+1] != 0 and "b" in game.board[i+1][j+1]):
                i += 1
                j += 1
                posDir.append((i, j))
                if i < 7 and j < 7 and game.board[i+1][j+1] != 0 and "b" in game.board[i+1][j+1]:
                    posDir.append((i, j))
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (i > 0 and j < 7 and game.board[i-1][j+1] == 0) or (game.board[i-1][j+1] != 0 and "b" in game.board[i-1][j+1]):
                i -= 1
                j += 1
                posDir.append((i, j))
                if i > 0 and j < 7 and game.board[i-1][j+1] != 0 and "b" in game.board[i-1][j+1]:
                    posDir.append((i, j))
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (j > 0 and i < 7 and game.board[i+1][j-1] == 0) or (game.board[i+1][j-1] != 0 and "b" in game.board[i+1][j-1]):
                j -= 1
                i += 1
                posDir.append((i, j))
                if j > 0 and i < 7 and game.board[i+1][j-1] != 0 and "b" in game.board[i+1][j-1]:
                    posDir.append((i, j))
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (j > 0 and i < 7 and game.board[i-1][j+1] == 0) or (game.board[i-1][j+1] != 0 and "b" in game.board[i-1][j+1]):
                j += 1
                i -= 1
                posDir.append((i, j))
                if j > 0 and i < 7 and game.board[i-1][j+1] != 0 and "b" in game.board[i-1][j+1]:
                    posDir.append((i, j))
                    break
        return posDir

class Dame:
    def __init__(self, pos):
        self.pos = pos
        self.posDir = self.checkDir()
    
    def checkDir(self):
        posDir = []
        tourDir = Tour(self.pos)
        fouDir = Fou(self.pos)
        for item in tourDir.posDir:
            posDir.append(item)
        for item in fouDir.posDir:
            posDir.append(item)
        del fouDir
        del tourDir
        gc.collect()
        return posDir

class Roi:
    def __init__(self, pos):
        self.pos = pos
        self.posDir = self.checkDir()
    
    def checkDir(self):
        posDir = []
        dame = Dame(self.pos)
        posDame = dame.posDir
        # print(posDame)
        for item in posDame:
            if (item[0] >= (self.pos[0] - 1) and (item[0] <= self.pos[0] +1)) and (item[1] >= (self.pos[1] - 1) and (item[1] <= self.pos[1] +1)):
                print("hye")
                posDir.append(item)
        del dame
        gc.collect()
        return posDir

    def isMate(self):
        pass

class Cheval:
    def __init__(self, pos):
        self.pos = pos
        self.posDir = self.checkDir()

    def checkDir(self):
        i = self.pos[0]
        j = self.pos[1]
        posDir = []
        if (i > 1 and i < 6) and (j > 1 and j < 6):
            chevalDir = [(i-2, j-1), (i-1, j-2), (i+1, j-2), (i+2, j-1), (i+2, j+1), (i+1, j+2), (i-1, j+2), (i-2, j+1)]
        elif (j > 1 and j < 6) and (i >= 0 and i < 2):
            chevalDir = [(i+1, j-2), (i+2, j-1), (i+2, j+1), (i+1, j+2)]
            if i == 1:
                chevalDir = [(i+1, j-2), (i+2, j-1), (i+2, j+1), (i+1, j+2), (i-1, j-2), (i-1, j+2)]
        elif (j > 1 and j < 6) and (i <= 7 and i > 5):
            chevalDir = [(i-1, j-2), (i-1, j+2), (i-2, j-1), (i-2, j+1)]
            if i == 6:
                chevalDir = [(i+1, j-2), (i+1, j+2), (i-1, j-2), (i-1, j+2), (i+1, j-2), (i+1, j+2)]
        elif (i > 1 and i < 6) and (j == 0):
            chevalDir = [(i-2, j+1), (i-1, j+2), (i+1, j+2), (i+2, j+1)]
        elif (i > 1 and i < 6) and (j == 7):
            chevalDir = [(i-2, j-1), (i-1, j-2), (i+1, j-2), (i+2, j-1)]
        elif (i > 1 and i < 6) and (j == 1):
            chevalDir = [(i-2, j-1), (i+2, j-1), (i+2, j+1), (i+1, j+2), (i-1, j+2), (i-2, j+1)]
        elif (i > 1 and i < 6) and (j == 6):
            chevalDir = [(i-2, j-1), (i-1, j-2), (i+1, j-2), (i+2, j-1), (i+2, j+1), (i-2, j+1)]
        
        elif i == 0 and j == 0:
            chevalDir = [(i+2, j+1), (i+1, j+2)]
        elif i == 7 and j == 0:
            chevalDir = [(i-2, j+1), (i-1, j+2)]
        elif i == 0 and j == 7:
            chevalDir = [(i+2, j-1), (i+1, j-2)]
        elif i == 7 and j == 7:
            chevalDir = [(i-2, j-1), (i-1, j-2)]

        elif i == 0 and j == 1:
            chevalDir = [(i+2, j+1), (i+1, j+2), (i+2, j-1)]
        elif i == 0 and j == 6:
            chevalDir = [(i+2, j+1), (i-1, j+2), (i-2, j+1)]
        elif i == 7 and j == 1:
            chevalDir = [(i-2, j-1), (i-2, j+1), (i-1, j+2)]
        elif i == 7 and j == 6:
            chevalDir = [(i-2, j-1), (i-2, j+1), (i-1, j-2)]
        
        elif i == 1 and j == 0:
            chevalDir = [(i-1, j+2), (i+1, j+2), (i+2, j+1)]
        elif i == 6 and j == 0:
            chevalDir = [(i-2, j+1), (i-1, j+2), (i+1, j+2)]
        elif i == 1 and j == 7:
            chevalDir = [(i+2, j-1), (i+1, j-2), (i-1, j-2)]
        elif i == 6 and j == 7:
            chevalDir = [(i-2, j-1), (i-1, j-2), (i+1, j-2)]

        elif i == 1 and j == 1:
            chevalDir = [(i-1, j+2), (i+1, j+2), (i+2, j+1), (i+2, j-1)]
        elif i == 1 and j == 6:
            chevalDir = [(i+1, j-2), (i-1, j-2), (i+2, j-1), (i+2, j+1)]
        elif i == 6 and j == 1:
            chevalDir = [(i-2, j-1), (i-2, j+1), (i-1, j+2), (i+1, j+2)]
        elif i == 6 and j == 6:
            chevalDir = [(i-2, j+1), (i-2, j-1), (i-1, j-2), (i+1, j-2)]


        for item in chevalDir:
                if game.board[item[0]][item[1]] == 0:
                    posDir.append(item)
                else:
                    if game.turn == "black":
                        if "w" in game.board[item[0]][item[1]]:
                            posDir.append(item)
                    else:
                        if "b" in game.board[item[0]][item[1]]:
                            posDir.append(item)
            
        return posDir

playing = True

while playing:
    print("C'est au {}".format(game.turn))
    selectPiece = input("Quel piece prenez vous ?")
    nextPos = input("Ou allez vous ?")
    if game.makeMove(selectPiece, nextPos):
        draw_game()
    else:
        print("Ceci n'est pas une case valide..")
    
# game.makeMove((6,4), (5,4))
# pion = Pion((6, 3))
# print(pion.posDir)
# game.makeMove((6, 1), (5, 1))
# print("\n")
# game.makeMove((0, 0), (5, 3))
# draw_game()
# draw_game()
# game.makeMove((7, 3), (6, 3))
# draw_game()
# tour = Tour((5, 3))
# cheval = Cheval((3, 1))
# print(cheval.posDir)
# tour = Tour((7, 0))
# draw_game()
# print(tour.posDir)
# print(game.posDir)
import gc

COLUMNS = 8
LINES = 8

def getOpponentPiece():
    wp = []
    bp = []
    for i in range(0, COLUMNS):
        for j in range(0, LINES):
            if game.board[i][j] != 0 and "w" in game.board[i][j]:
                wp.append((i, j))
            elif game.board[i][j] != 0 and "b" in game.board[i][j]:
                bp.append((i, j))
    return wp, bp

def draw_game(board):
    for i in range(COLUMNS):
        for j in range(19):
            if j == 0:
                print("\n", "--", end="")
            print("--", end="")
        for j in range(LINES):
            if j == 0:
                print("\n", end="")
            print("| ", end="")
            if board[i][j] == 0:
                print(" 0", end="")
            else:
                print(board[i][j], end="")
            print(" ", end="")
        print("|", end="")
    print("\n")
    print("Black: {}".format(game.pieceTaken["black"]))
    print("White: {}".format(game.pieceTaken["white"]))
    pass

def getKingsPos():
    for i in range(COLUMNS):
        for j in range(LINES):
            if game.board[i][j] == "rb":
                blackKingPos = (i, j)
            elif game.board[i][j] == "rw":
                whiteKingPos = (i, j)
    return blackKingPos, whiteKingPos

def getPiecesPos(pw, pb, check=True):
    opposentPos = []
    ownPos = []
    if game.turn == "black":
        game.turn = "white"
        for item in pw:
            piece, name = game.getPiece(item)
            if "p" in name:
                posDir = piece.checkDir(kingCheck=check)
            else:
                posDir = piece.posDir
            for pos in posDir:
                opposentPos.append([name, item, pos])
        game.turn = "black"
        for item in pb:
            piece, name = game.getPiece(item)
            if "p" in name:
                posDir = piece.checkDir(kingCheck=check)
            else:
                posDir = piece.posDir
            for pos in posDir:
                ownPos.append([name, item, pos])
    else:
        game.turn = "black"
        for item in pb:
            piece, name = game.getPiece(item)
            if "p" in name:
                posDir = piece.checkDir(kingCheck=check)
            else:
                posDir = piece.posDir
            for pos in posDir:
                opposentPos.append([name, item, pos])
        game.turn = "white"
        for item in pw:
            piece, name = game.getPiece(item)
            if "p" in name:
                posDir = piece.checkDir(kingCheck=check )
            else:
                posDir = piece.posDir
            for pos in posDir:
                ownPos.append([name, item, pos])
    return opposentPos, ownPos
    

class Game(object):
    def __init__(self):        
        self.board = [[0]*LINES for _ in range(LINES)]
        self.initiate_board()
        self.turn = "white"
        self.pieceTaken = { "black": [], "white": [] }
        self.posDir = self.checkDir()
        self.playing = True
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

    def getPiece(self, piecePos, isMate=False):
        name = self.board[piecePos[0]][piecePos[1]]
        if name == 0:
            return None, None
        if "p" in name:
            piece = Pion(piecePos)
        elif "t" in name:
            piece = Tour(piecePos)
        elif "f" in name:
            piece = Fou(piecePos)
        elif "d" in name:
            piece = Dame(piecePos)
        elif "r" in name:
            piece = Roi(piecePos, isMate)
        else:
            piece = Cheval(piecePos)
        return piece, name

    def makeMove(self, piecePos, nextPos, piece, name, piece_pos):
        if self.board[nextPos[0]][nextPos[1]] != 0 and "r" in name:
            return False
        temporary = [[game.board[i][j] for i in range(COLUMNS)] for j in range(LINES)]
        if nextPos in piece.posDir:
            temp = self.board[nextPos[0]][nextPos[1]]
            if self.board[piecePos[0]][piecePos[1]] != 0 and "r" in name:
                if nextPos == (0, 6):
                    self.board[0][7] = 0
                    self.board[0][5] = "tb"
                elif nextPos == (0, 2):
                    self.board[0][0] = 0
                    self.board[0][3] = "tb"
                elif nextPos == (7, 6):
                    self.board[7][7] = 0
                    self.board[7][5] = "tw"
                elif nextPos == (7, 2):
                    self.board[7][0] = 0
                    self.board[7][3] = "tw"
            elif temp != 0:
                if "w" in name:
                    self.pieceTaken["white"].append(temp)
                else:
                    self.pieceTaken["black"].append(temp)
            if "p" in name and self.turn == "white" and nextPos[0] == 0:
                name = self.getNewPiece("w")
            elif "p" in name and self.turn == "black" and nextPos[0] == 7:
                name = self.getNewPiece("b")
            self.board[nextPos[0]][nextPos[1]] = name
            self.board[piecePos[0]][piecePos[1]] = 0
            roi_piece = Roi(piece_pos)
            if "r" in name:
                roi_piece.pos = nextPos
            if roi_piece.isMate():
                print("can't play this move.. You are mate")
                game.board = temporary
                return False
            else:
                return True
        else:
            return False
        
    def getNewPiece(self, color):
        pieces = ["t", "c", "f", "d"]
        print(pieces)
        pieceSelect = input("Quelle piece choisissez-vous ?")
        name = f"{pieceSelect}{color}"
        return name
        

game = Game()


class Pion():
    def __init__(self, pos):
        self.pos = pos
        self.posDir = self.checkDir()
    
    def checkDir(self, kingCheck=False):
        posDir = []
        i = self.pos[0]
        j = self.pos[1]
        if game.turn == "white":
            if i > 0:
                if not kingCheck:
                    if i == 6 and game.board[i-1][j] == 0 and game.board[i-2][j] == 0:
                        posDir.append((i-2, j))
                    if game.board[i-1][j] == 0:
                        posDir.append((i-1, j))
                if j > 0 and j < 7:
                    if game.board[i-1][j-1] != 0 and "b" in game.board[i-1][j-1]:
                        posDir.append((i-1, j-1))
                    if game.board[i-1][j+1] != 0 and "b" in game.board[i-1][j+1]:
                        posDir.append((i-1, j+1))
                if j == 0 and (game.board[i-1][j+1] != 0 and "b" in game.board[i-1][j+1]):
                    posDir.append((i-1, j+1))
                if j == 7 and (game.board[i-1][j-1] != 0 and "b" in game.board[i-1][j-1]):
                    posDir.append((i-1, j-1))
        else:
            if i < 7:
                if not kingCheck:
                    if i == 1 and game.board[i+1][j] == 0 and game.board[i+2][j] == 0:
                        posDir.append((i+2, j))
                    if game.board[i+1][j] == 0:
                        posDir.append((i+1, j))
                if j > 0 and j < 7:
                    if game.board[i+1][j-1] != 0 and "w" in game.board[i+1][j-1]:
                        posDir.append((i+1, j-1))
                    if game.board[i+1][j+1] != 0 and "w" in game.board[i+1][j+1]:
                        posDir.append((i+1, j+1))
                if j == 0 and (game.board[i+1][j+1] != 0 and "w" in game.board[i+1][j+1]):
                    posDir.append((i+1, j+1))
                if j == 7 and (game.board[i+1][j-1] != 0 and "w" in game.board[i+1][j-1]):
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
            while (i < 7 and game.board[i+1][j] == 0) or (i < 7 and game.board[i+1][j] != 0 and "w" in game.board[i+1][j]):
                i += 1
                posDir.append((i, j))
                if game.board[i][j] != 0:
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (i > 0 and game.board[i-1][j] == 0) or (i > 0 and game.board[i-1][j] != 0 and "w" in game.board[i-1][j]):
                i -= 1
                posDir.append((i, j))
                if game.board[i][j] != 0:
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (j > 0 and game.board[i][j-1] == 0) or (j > 0 and game.board[i][j-1] != 0 and "w" in game.board[i][j-1]):
                j -= 1
                posDir.append((i, j))
                if game.board[i][j] != 0:
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (j < 7 and game.board[i][j+1] == 0) or (j < 7 and game.board[i][j+1] != 0 and "w" in game.board[i][j+1]):
                j += 1
                posDir.append((i, j))
                if game.board[i][j] != 0:
                    break
            i = self.pos[0]
            j = self.pos[1]
        else:
            while (i < 7 and game.board[i+1][j] == 0) or (i < 7 and game.board[i+1][j] != 0 and "b" in game.board[i+1][j]):
                i += 1
                posDir.append((i, j))
                if game.board[i][j] != 0:
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (i > 0 and game.board[i-1][j] == 0) or (i > 0 and game.board[i-1][j] != 0 and "b" in game.board[i-1][j]):
                i -= 1
                posDir.append((i, j))
                if game.board[i][j] != 0:
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (j > 0 and game.board[i][j-1] == 0) or (j > 0 and game.board[i][j-1] != 0 and "b" in game.board[i][j-1]):
                j -= 1
                posDir.append((i, j))
                if game.board[i][j] != 0:
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (j < 7 and game.board[i][j+1] == 0) or (j < 0 and game.board[i][j+1] != 0 and "b" in game.board[i][j+1]):
                j += 1
                posDir.append((i, j))
                if game.board[i][j] != 0:
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
            while (i < 7 and j < 7 and game.board[i+1][j+1] == 0) or (i < 7 and j < 7 and game.board[i+1][j+1] != 0 and "w" in game.board[i+1][j+1]):
                i += 1
                j += 1
                posDir.append((i, j))
                if game.board[i][j] != 0:
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (i > 0 and j < 7 and game.board[i-1][j+1] == 0) or (i > 0 and j < 7 and game.board[i-1][j+1] != 0 and "w" in game.board[i-1][j+1]):
                j += 1
                i -= 1
                posDir.append((i, j))
                if game.board[i][j] != 0:
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (j > 0 and i < 7 and game.board[i+1][j-1] == 0) or (j > 0 and i < 7 and game.board[i+1][j-1] != 0 and "w" in game.board[i+1][j-1]):
                i += 1
                j -= 1
                posDir.append((i, j))
                if game.board[i][j] != 0:
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (j > 0 and i > 0 and game.board[i-1][j-1] == 0) or (j > 0 and i > 0 and game.board[i-1][j-1] != 0 and "w" in game.board[i-1][j-1]):
                i -= 1
                j -= 1
                posDir.append((i, j))
                if game.board[i][j] != 0:
                    break
            i = self.pos[0]
            j = self.pos[1]
        else:
            while (i < 7 and j < 7 and game.board[i+1][j+1] == 0) or (i < 7 and j < 7 and game.board[i+1][j+1] != 0 and "b" in game.board[i+1][j+1]):
                i += 1
                j += 1
                posDir.append((i, j))
                if game.board[i][j] != 0:
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (i > 0 and j < 7 and game.board[i-1][j+1] == 0) or (i > 0 and j < 7 and game.board[i-1][j+1] != 0 and "b" in game.board[i-1][j+1]):
                i -= 1
                j += 1
                posDir.append((i, j))
                if game.board[i][j] != 0:
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (j > 0 and i < 7 and game.board[i+1][j-1] == 0) or (j > 0 and i < 7 and game.board[i+1][j-1] != 0 and "b" in game.board[i+1][j-1]):
                j -= 1
                i += 1
                posDir.append((i, j))
                if game.board[i][j] != 0:
                    break
            i = self.pos[0]
            j = self.pos[1]
            while (j > 0 and i > 0 and game.board[i-1][j-1] == 0) or (j > 0 and i > 0 and game.board[i-1][j-1] != 0 and "b" in game.board[i-1][j-1]):
                j -= 1
                i -= 1
                posDir.append((i, j))
                if game.board[i][j] != 0:
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
    def __init__(self, pos, kingMate=False):
        self.pos = pos
        self.mate = kingMate
        self.checkMate = False
        self.posDir = self.checkDir()
    
    def checkDir(self):
        posDir = []
        dame = Dame(self.pos)
        posDame = dame.posDir
        for item in posDame:
            if (item[0] >= (self.pos[0] - 1) and (item[0] <= self.pos[0] + 1)) and (item[1] >= (self.pos[1] - 1) and (item[1] <= self.pos[1] +1)):
                posDir.append(item)
        if game.turn == "black" and not self.mate:
            if game.board[0][5] == 0 and game.board[0][6] == 0 and game.board[0][7] == "tb":
                posDir.append((0, 6))
            if game.board[0][1] == 0 and game.board[0][2] == 0 and game.board[0][3] == 0 and game.board[0][0] == "tb":
                posDir.append((0, 2))
        elif game.turn == "white" and not self.mate:
            if game.board[7][5] == 0 and game.board[7][6] == 0 and game.board[7][7] == "tw":
                posDir.append((7, 6))
            if game.board[7][1] == 0 and game.board[7][2] == 0 and game.board[7][3] == 0 and game.board[7][0] == "tw":
                posDir.append((7, 2))
        del dame
        gc.collect()
        return posDir

    def isMate(self):
        posWhite, posBlack = getOpponentPiece()
        oppoPos, ownPos = getPiecesPos(posWhite, posBlack, False)
        opposentPos = [item[2] for item in oppoPos]
        opposentFiltered = list(dict.fromkeys(opposentPos))
        if (self.pos in opposentFiltered):
            print("echec au roi")
            for item in opposentFiltered:
                if item in self.posDir:
                    self.posDir.remove(item)
            tempo = [[game.board[i][j] for i in range(COLUMNS)] for j in range(LINES)]
            for item in self.posDir:
                game.board[self.pos[0]][self.pos[1]] = 0
                if game.turn == "black":
                    game.board[item[0]][item[1]] = "rb"
                else:
                    game.board[item[0]][item[1]] = "rw"
                temp = self.pos
                self.pos = (item[0], item[1])
                posWhite, posBlack = getOpponentPiece()
                oppoPos, _ = getPiecesPos(posWhite, posBlack, False)
                opposentPos = [item[2] for item in oppoPos]
                opposentFiltered = list(dict.fromkeys(opposentPos))
                if (self.pos in opposentFiltered):
                    self.posDir.remove((item[0], item[1]))
                self.pos = temp
                game.board = [[tempo[i][j] for i in range(COLUMNS)] for j in range(LINES)]
            if len(self.posDir) == 0:
                print("no possible pos..")
                self.posDir = []
                tempo = [[game.board[i][j] for i in range(COLUMNS)] for j in range(LINES)]
                for item in ownPos:
                    nextPosition = item[2]
                    game.board[item[1][0]][item[1][1]] = 0
                    game.board[nextPosition[0]][nextPosition[1]] = item[0]
                    posWhite, posBlack = getOpponentPiece()
                    oppoPos, _ = getPiecesPos(posWhite, posBlack, False)
                    opposentPos = [item[2] for item in oppoPos]
                    opposentFiltered = list(dict.fromkeys(opposentPos))
                    if item in opposentFiltered:
                        game.board = tempo
                        self.checkMate = False
                        return False
                    game.board = [[tempo[i][j] for i in range(COLUMNS)] for j in range(LINES)]
                self.checkMate = True
                return True
            self.mate = True
            self.checkMate = False
            return True
        self.checkMate = False
        self.mate = False
        return False
    

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
            chevalDir = [(i+2, j+1), (i+1, j-2), (i+2, j-1)]
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


count = 0
turns = ["white", "black"]

# while game.playing:
#     draw_game(game.board)
#     print("\n")
#     print("C'est au {}".format(game.turn))
#     blackKingPos, whiteKingPos = getKingsPos()
#     if game.turn == "black":
#         roi = Roi(blackKingPos)
#     else:
#         roi = Roi(whiteKingPos)
#     if roi.isMate():
#         if roi.checkMate:
#             print("checkmate..")
#             game.playing = False
#             break
#     selectPiece = input("Quel piece prenez vous ?")
#     formatPiece = tuple(map(int, selectPiece.split(',')))
#     if roi.mate:
#         piece, name = game.getPiece(formatPiece, True)
#     else:
#         piece, name = game.getPiece(formatPiece)
#     print(piece.posDir)
#     nextPos = input("Ou allez vous ?")
#     formatNext = tuple(map(int, nextPos.split(',')))
#     if roi.pos == piece.pos:
#         roi = piece
#     while not game.makeMove(formatPiece, formatNext, piece, name, roi.pos) and game.playing:
#         selectPiece = input("Quel piece prenez vous ?")
#         formatPiece = tuple(map(int, selectPiece.split(',')))
#         piece, name = game.getPiece(formatPiece)
#         print(piece.posDir)
#         nextPos = input("Ou allez vous ?")
#         formatNext = tuple(map(int, nextPos.split(',')))
#     if count == 0:
#         count = 1
#     else:
#         count = 0
#     game.turn = turns[count]

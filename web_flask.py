from flask import Flask, redirect, url_for, render_template, request, session, jsonify, make_response
from flask_cors import CORS
import main

app = Flask(__name__)
app.secret_key = "PaRiS"
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("base.html", board=main.game.board)

@app.route('/api/v1/board', methods=['GET'])
def api_all():
    return jsonify(main.game.board)

@app.route("/api/v1/board/update", defaults='', methods=['GET', 'POST'])
def api_post():
    posString = str(request.args.get('position'))
    nextString = str(request.args.get('nextPos'))
    formPos = tuple(map(int, posString.split(',')))
    formNext = tuple(map(int, nextString.split(',')))
    blackKingPos, whiteKingPos = main.getKingsPos()
    if main.game.turn == "black":
        roi = main.Roi(blackKingPos)
    else:
        roi = main.Roi(whiteKingPos)
    if roi.mate:
        piece, name = main.game.getPiece(formPos, True)
    else:
        piece, name = main.game.getPiece(formPos)
    if roi.isMate():
        if roi.checkMate:
            print("checkmate..")
            main.game.playing = False
    if main.game.playing:
        if main.game.makeMove(formPos, formNext, piece, name, roi.pos):
            if main.count == 0:
                main.count = 1
            else:
                main.count = 0
            main.game.turn = main.turns[main.count]
    return jsonify(main.game.board)

if __name__ == '__main__':
    app.run(debug=True)
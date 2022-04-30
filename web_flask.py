from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import main
import requests

app = Flask(__name__)
app.secret_key = "PaRiS"
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    response = requests.get("http://localhost:5000/api/v1/board")
    res_json = response.json()
    turn = res_json["turn"]
    game_board = res_json["board"]
    check = res_json["check"]
    checkmate = res_json["checkmate"]
    return render_template("base.html", board=game_board, turn=turn, check=check, checkmate=checkmate)


@app.route('/api/v1/board', methods=['GET'])
def api_all():
    blackKingPos, whiteKingPos = main.getKingsPos()
    if main.game.turn == "black":
        roi = main.Roi(blackKingPos)
    else:
        roi = main.Roi(whiteKingPos)
    if roi.isMate():
        if roi.checkMate:
            print("checkmate..")
            main.game.playing = False
            game = { "board": main.game.board, "turn": main.game.turn, "check": "true", "checkmate": "true" }
        else:
            game = { "board": main.game.board, "turn": main.game.turn, "check": "true", "checkmate": "false" }
        return jsonify(game)
    else:
        game = { "board": main.game.board, "turn": main.game.turn, "check": "false", "checkmate": "false" }
    return jsonify(game)


@app.route("/api/v1/board/update", defaults='', methods=['GET', 'POST'])
def api_post():
    if main.game.playing:
        if request.args.get('position'):
            posString = str(request.args.get('position'))
            formPos = tuple(map(int, posString.split(',')))
            if request.args.get('nextPos'):
                nextString = str(request.args.get('nextPos'))
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
            if request.args.get('nextPos'):
                if main.game.makeMove(formPos, formNext, piece, name, roi.pos):
                    if main.count == 0:
                        main.count = 1
                    else:
                        main.count = 0
                    main.game.turn = main.turns[main.count]
                game = { "board": main.game.board, "turn": main.game.turn, "check": "false", "checkmate": "false" }
                return jsonify(game)
            else:
                game = { "board": main.game.board, "posDir": piece.posDir,"turn": main.game.turn, "check": "false", "checkmate": "false" }
                return jsonify(game)
        else:
            game = { "board": main.game.board, "turn": main.game.turn, "check": "false", "checkmate": "false" }
            return jsonify(game)
    return jsonify(game)

if __name__ == '__main__':
    app.run(debug=True)
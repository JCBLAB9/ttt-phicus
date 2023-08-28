from tictactoe import TicTacToe
from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)
game = TicTacToe()


@app.route('/start', methods=['GET'])
def start_game():
    game.reset()
    return jsonify(
        {
            "board": game.display_board(),
            "status": game.status,
            "current_player": game.current_player
        })


@app.route('/move', methods=['POST'])
def make_move():
    data = request.get_json()
    row, col = data['row'], data['col']
    result = game.make_move(row, col)
    return jsonify(
        {
            "result": result,
            "board": game.display_board(),
            "status": game.status,
            "current_player": game.current_player
        })


@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(
        {"board": game.display_board(),
         "status": game.status,
         "current_player": game.current_player
         })


if __name__ == '__main__':
    app.run()

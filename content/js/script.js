let currentPlayer = 'X';

function startGame() {
    fetch('http://127.0.0.1:5000/start')
        .then(response => response.json())
        .then(data => {
            updateBoard(data.board);
            document.getElementById("status").textContent = "Game started!";
        });
}

function makeMove(row, col) {
    fetch('http://127.0.0.1:5000/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({row: row, col: col})
    })
    .then(response => response.json())
    .then(data => {
        if (data.result !== "invalid move") {
            updateBoard(data.board);
            if (data.status !== "in progress") {
                document.getElementById("status").textContent = data.status;
            } else {
                currentPlayer = data.current_player;
            }
        } else {
            alert("Invalid move!");
        }
    });
}

function updateBoard(board) {
    const table = document.getElementById("board");
    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            table.rows[i].cells[j].textContent = board[i][j];
        }
    }
}

window.onload = startGame;


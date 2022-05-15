const board = document.querySelector(".board");
const center = document.querySelector(".sub-title");
let eatPiece = 0;
let turn;
let pos_color;
let posPiece = "";
let nextPos = "";

const differentArray = (array1, array2) => {
    for (let i = 0; i < array1.length; i++) {
        for (let j = 0; j < array1.length; j++) {
            if (array1[i][j] !== array2[i][j]) {
                return true;
            }
        }
    };
    return false;
}
  
if (board) {
    const executeGame = async () => {
        const fetchResponse = await fetch(`/api/v1/board`);
        const data = await fetchResponse.json();
        turn = data["turn"];
        posPiece = "";
        nextPos = "";
        if (data["checkmate"] == "true") {
            center.innerHTML = `<h3 class="sub-title">${turn} are checkmate!</h3>`;
        } else if (data["check"] == "true") {
            center.innerHTML = `<h3 class="sub-title">${turn} are check!</h3>`;
        } else {
            center.innerHTML = "";
        }
        const lines = board.children;
        for (let line of lines) {
            const squares = line.children;
            for (let square of squares) {
                square.addEventListener("click", async (e) => {
                    e.preventDefault();
                    const posHTML = e.currentTarget.id.slice(8,12);
                    if (e.currentTarget.children.length > 0) {
                        const innerLines = board.children;
                        for (let inLine of innerLines) {
                            const innerSquares = inLine.children;
                            for (let innerSquare of innerSquares) {
                                const innerPosHTML = innerSquare.id.slice(8,12);
                                let leftNum = Number.parseInt(innerPosHTML[0], 10);
                                let rightNum = Number.parseInt(innerPosHTML[3], 10);
                                let idNum = leftNum + rightNum;
                                if (innerSquare.children.length > 0 && innerSquare.children[0].classList.contains("gray_posDir")) {
                                    innerSquare.innerHTML = "";
                                }
                                if (innerSquare.classList.contains("select_square") & idNum % 2 == 0) {
                                    innerSquare.classList.remove("select_square");
                                    innerSquare.classList.add("beige_square");
                                } else if (innerSquare.classList.contains("select_square") & idNum % 2 == 1) {
                                    innerSquare.classList.remove("select_square");
                                    innerSquare.classList.add("green_square");
                                }
                            }
                        }
                        if (e.currentTarget.classList.contains('beige_square')) {
                            e.currentTarget.classList.remove("beige_square");
                            e.currentTarget.classList.add("select_square");
                        } else if (e.currentTarget.classList.contains('green_square')) {
                            e.currentTarget.classList.remove("green_square");
                            e.currentTarget.classList.add("select_square");
                        }
                    }
                    if (e.currentTarget.children.length > 0) {
                        let pos_id = e.currentTarget.children[0].src;
                        pos_color = pos_id[37];
                        if (pos_color === turn[0]) {
                            posPiece = posHTML.replace(/\s/g, '');
                        } else if (pos_color !== turn[0]) { 
                            nextPos = posHTML.replace(/\s/g, '');
                        } 
                    } else if (square.children.length === 0 & posPiece !== "") {
                        nextPos = posHTML.replace(/\s/g, '');
                    }
                    const headers = {
                        method:"POST",
                        headers: {
                            "Content-type": "application/json; charset=UTF-8"
                        }
                    };
                    if (nextPos === "") {
                        const fetchResponse = await fetch(`/api/v1/board/update?position=${posPiece}`, headers);
                        const data = await fetchResponse.json();
                        const possibleDir = [];
                        if (data["posDir"] !== undefined) {
                            for(let item of data["posDir"]) {
                                let squareString = "square_(";
                                squareString += String(item[0]);
                                squareString += ", ";
                                squareString += String(item[1]);
                                squareString += ")";
                                possibleDir.push(squareString);
                            }
                            for (let name of possibleDir) {
                                const element = document.getElementById(name);
                                if (element.children.length == 0) {
                                    element.insertAdjacentHTML("beforeend", "<div class='gray_posDir'></div>")
                                }
                            }
                        }
                    }
                    if (posPiece !== "" & nextPos !== "") {
                        const init_board = await fetch('/api/v1/board/update');
                        const init_info = await init_board.text();
                        const init_json = JSON.parse(init_info);
                        fetch(`/api/v1/board/update?position=${posPiece}&nextPos=${nextPos}`, headers);
                        const update_board = await fetch('/api/v1/board/update');
                        const update_info = await update_board.text();
                        const updated_json = JSON.parse(update_info);
                        let html = "";
                        const updated_json_board = updated_json["board"];
                        const init_json_board = init_json["board"];
                        const turnData = await fetch('/api/v1/board/update');
                        const turnData_info = await turnData.text();
                        const turnData_json = JSON.parse(turnData_info);
                        turn = turnData_json["turn"]
                        if (differentArray(updated_json_board, init_json_board)) {
                            board.innerHTML = "";
                            if (turn == "white") {
                                for (let i = 0; i < 8; i++) {
                                    html += `<div class="line_squares">`;
                                    for (let j = 0; j < 8; j++) {
                                        const position = `(${i}, ${j})`;
                                        if ((i + j) % 2 == 0) {
                                            html += `<div id='square_${position}' class="squares beige_square">`;
                                            if (updated_json_board[i][j] != 0) {
                                                html += `<img src="../static/images/${updated_json_board[i][j]}.png" id="img_${position}" \
                                                width="70px" height="80px" alt="img_${updated_json_board[i][j]}"/>`;
                                            }
                                            html += "</div>";
                                        } else {
                                            html += `<div id='square_${position}' class="squares green_square">`;
                                            if(updated_json_board[i][j] != 0) {
                                                html += `<img src="../static/images/${updated_json_board[i][j]}.png" id="img_${position}"\
                                                width="70px" height="80px" alt="img_${updated_json_board[i][j]}"/>`;
                                            }
                                            html += "</div>";
                                        }
                                    }
                                    html += "</div>"
                                }
                            } else if (turn == "black") {
                                for (let i = 7; i >= 0; i--) {
                                    html += `<div class="line_squares">`;
                                    for (let j = 7; j >= 0; j--) {
                                        const position = `(${i}, ${j})`;
                                        if ((i + j) % 2 == 0) {
                                            html += `<div id='square_${position}' class="squares beige_square">`;
                                            if (updated_json_board[i][j] != 0) {
                                                html += `<img src="../static/images/${updated_json_board[i][j]}.png" id="img_${position}" \
                                                width="70px" height="80px" alt="img_${updated_json_board[i][j]}"/>`;
                                            }
                                            html += "</div>";
                                        } else {
                                            html += `<div id='square_${position}' class="squares green_square">`;
                                            if(updated_json_board[i][j] != 0) {
                                                html += `<img src="../static/images/${updated_json_board[i][j]}.png" id="img_${position}"\
                                                 width="70px" height="80px" alt="img_${updated_json_board[i][j]}"/>`;
                                            }
                                            html += "</div>";
                                        }
                                    }
                                    html += "</div>"
                                }
                            }
                            board.insertAdjacentHTML("beforeend", html);
                        }
                        executeGame();
                    }
                })
            }
        }
    }
    executeGame();
}


// innerSquare.classList.remove("select_square");
// innerSquare.classList.add("green_square");

// } else if (innerSquare.classList.contains("select_square") & idNum % 2 == 0) {
//     innerSquare.innerHTML = "";
//     innerSquare.classList.remove("select_square");
//     innerSquare.classList.add("beige_square");
// }
// if (innerSquare.classList.contains("yellow_posDir") & idNum % 2 == 1) {
//     innerSquare.innerHTML = "";
//     innerSquare.classList.remove("yellow_posDir");
//     innerSquare.classList.add("green_square");
// } else if (innerSquare.classList.contains("yellow_posDir") & idNum % 2 == 0) {
//     innerSquare.innerHTML = "";
//     innerSquare.classList.remove("yellow_posDir");
//     innerSquare.classList.add("beige_square");
// }
// if (element.classList.contains('beige_square')) {
// element.classList.remove("beige_square");
// element.classList.add("yellow_posDir");
// } else if (element.classList.contains('green_square')) {
    // element.classList.remove("green_square");
    // element.insertAdjacentHTML("beforeend", "<div class='gray_posDir'></div>")
    // element.classList.add("yellow_posDir");
// }


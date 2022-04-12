const board = document.querySelector(".board");
let posPiece = "";
let nextPos = "";
let eatPiece = 0;
let turn;

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
    const executeGame = () => {
        const lines = board.children;
        for (let line of lines) {
            const squares = line.children;
            for (let square of squares) {
                square.addEventListener("click", async (e) => {
                    e.preventDefault();
                    const posHTML = square.id.slice(8,12);
                    if (e.currentTarget.children.length > 0) {
                        if (e.currentTarget.classList.contains('beige_square')) {
                            e.currentTarget.classList.remove("beige_square");
                            e.currentTarget.classList.add("select_square");
                        } else if (e.currentTarget.classList.contains('green_square')) {
                            e.currentTarget.classList.remove("green_square");
                            e.currentTarget.classList.add("select_square");
                        }
                    }
                    if (square.children.length > 0 & eatPiece == 0) { 
                        posPiece = posHTML.replace(/\s/g, '');
                        eatPiece = 1; 
                    } else if (square.children.length > 0 & eatPiece == 1) { 
                        nextPos = posHTML.replace(/\s/g, '');
                        eatPiece = 0;
                    } else {
                        nextPos = posHTML.replace(/\s/g, '');
                    }
                    console.log(posPiece);
                    const headers = {
                        method:"POST",
                        headers: {
                            "Content-type": "application/json; charset=UTF-8"
                        }
                    };
                    const fetchResponse = await fetch(`/api/v1/board/update?position=${posPiece}`, headers);
                    const data = await fetchResponse.json();
                    console.log(data);
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
                            if (element.classList.contains('beige_square')) {
                                element.classList.remove("beige_square");
                                element.classList.add("yellow_posDir");
                            } else if (element.classList.contains('green_square')) {
                                element.classList.remove("green_square");
                                element.classList.add("yellow_posDir");
                            }
                        }
                    };
                    console.log(possibleDir);
                    if (posPiece !== "" & nextPos !== "") {
                        const init_board = await fetch('/api/v1/board/update');
                        const init_info = await init_board.text();
                        const init_json = JSON.parse(init_info);
                        fetch(`/api/v1/board/update?position=${posPiece}&nextPos=${nextPos}`, {
                            method:"POST",
                            headers: {
                                "Content-type": "application/json; charset=UTF-8"
                            }
                        });
                        const update_board = await fetch('/api/v1/board/update');
                        const update_info = await update_board.text();
                        const updated_json = JSON.parse(update_info);
                        let html = "";
                        const info = await fetch('/api/v1/board');
                        const info_text = await info.text();
                        const info_json = JSON.parse(info_text);
                        turn = info_json["turn"];
                        if (differentArray(updated_json, init_json)) {
                            board.innerHTML = "";
                            if (turn == "white") {
                                for (let i = 0; i < 8; i++) {
                                    html += `<div class="line_squares">`;
                                    for (let j = 0; j < 8; j++) {
                                        const position = `(${i}, ${j})`;
                                        if ((i + j) % 2 == 0) {
                                            html += `<div id='square_${position}' class="squares beige_square">`;
                                            if (updated_json[i][j] != 0) {
                                                html += `<img src="../static/images/${updated_json[i][j]}.png" id="img_${position}" \
                                                width="70px" height="80px" alt="img_${updated_json[i][j]}"/>`;
                                            }
                                            html += "</div>";
                                        } else {
                                            html += `<div id='square_${position}' class="squares green_square">`;
                                            if(updated_json[i][j] != 0) {
                                                html += `<img src="../static/images/${updated_json[i][j]}.png" id="img_${position}"\
                                                 width="70px" height="80px" alt="img_${updated_json[i][j]}"/>`;
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
                                            if (updated_json[i][j] != 0) {
                                                html += `<img src="../static/images/${updated_json[i][j]}.png" id="img_${position}" \
                                                width="70px" height="80px" alt="img_${updated_json[i][j]}"/>`;
                                            }
                                            html += "</div>";
                                        } else {
                                            html += `<div id='square_${position}' class="squares green_square">`;
                                            if(updated_json[i][j] != 0) {
                                                html += `<img src="../static/images/${updated_json[i][j]}.png" id="img_${position}"\
                                                 width="70px" height="80px" alt="img_${updated_json[i][j]}"/>`;
                                            }
                                            html += "</div>";
                                        }
                                    }
                                    html += "</div>"
                                }
                            }
                            board.insertAdjacentHTML("beforeend", html);
                        }
                        posPiece = "";
                        nextPos = "";
                        eatPiece = 0;
                        executeGame();
                    }
                })
            }
        }
    }
    executeGame();
}



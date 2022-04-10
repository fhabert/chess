const board = document.querySelector(".board");
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
    const lines = board.children;
    for (let line of lines) {
        const squares = line.children;
        for (let square of squares) {
            square.addEventListener("click", async () => {
                console.log(square.id);
                const posHTML = square.id.slice(8,12);
                if (square.children.length > 0) { 
                    posPiece = posHTML.replace(/\s/g, '');
                } else {
                    nextPos = posHTML.replace(/\s/g, '');
                }
                if (posPiece !== "" & nextPos !== "") {
                    const dataPos = {position: posPiece, nextP: nextPos};
                    const init_board = await fetch('/api/v1/board');
                    const init_info = await init_board.text();
                    const init_json = JSON.parse(init_info);
                    fetch(`/api/v1/board/update?position=${posPiece}&nextPos=${nextPos}`, {
                        method:"POST",
                        body: JSON.stringify(dataPos),
                        headers: {
                            "Content-type": "application/json; charset=UTF-8"
                        }
                    })
                        .then(response => response.json())
                        .then(json => console.log(json));
                    const update_board = await fetch('/api/v1/board');
                    const update_info = await update_board.text();
                    const updated_json = JSON.parse(update_info);
                    let html = "";
                    if (differentArray(updated_json, init_json)) {
                        console.log("yeahhh");
                        board.innerHTML = "";
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
                        board.insertAdjacentHTML("beforeend", html);
                    }
                    posPiece = "";
                    nextPos = "";
                }
            })
        }
    }
}




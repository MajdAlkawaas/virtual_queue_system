document.addEventListener("DOMContentLoaded", function () {
    console.log("Game script loaded ");

    // Add event listeners to game buttons
    document.querySelectorAll(".game-btn").forEach(button => {
        button.addEventListener("click", function () {
            loadGame(this.dataset.game);
        });
    });
});

/*  Game Selection Logic */
function loadGame(gameName) {
    const gameContainer = document.getElementById("game-content");
    gameContainer.innerHTML = ""; /

    switch (gameName) {
        case "rock-paper-scissors":
            startRockPaperScissors();
            break;
        case "memory-match":
            startMemoryMatch();
            break;
        case "number-guess":
            startNumberGuess();
            break;
        default:
            gameContainer.innerHTML = "<p class='text-center text-danger'>⚠️ Game not found.</p>";
    }
}

/* Rock-Paper-Scissors */
function startRockPaperScissors() {
    document.getElementById("game-content").innerHTML = `
        <h3>Rock-Paper-Scissors</h3>
        <p>Choose one:</p>
        <button class="btn btn-dark" onclick="playRPS('rock')">🪨 Rock</button>
        <button class="btn btn-info" onclick="playRPS('paper')">📄 Paper</button>
        <button class="btn btn-warning" onclick="playRPS('scissors')">✂ Scissors</button>
        <p id="rps-result" class="mt-3 text-center"></p>
        <button class="btn btn-secondary mt-3" onclick="startRockPaperScissors()">🔄 Restart</button>
    `;
}

function playRPS(playerChoice) {
    const choices = ["rock", "paper", "scissors"];
    const aiChoice = choices[Math.floor(Math.random() * choices.length)];
    let result = "It's a tie!";
    
    if (
        (playerChoice === "rock" && aiChoice === "scissors") ||
        (playerChoice === "paper" && aiChoice === "rock") ||
        (playerChoice === "scissors" && aiChoice === "paper")
    ) {
        result = "🎉 You win!";
    } else if (playerChoice !== aiChoice) {
        result = "💻 AI wins!";
    }

    document.getElementById("rps-result").innerHTML = `AI chose <b>${aiChoice.toUpperCase()}</b>. ${result}`;
}

/* Memory Match (5x5 Grid) */
function startMemoryMatch() {
    document.getElementById("game-content").innerHTML = `
        <h3>Memory Match</h3>
        <p>Find matching pairs before time runs out!</p>
        <div id="memory-grid"></div>
        <button class="btn btn-secondary mt-3" onclick="startMemoryMatch()">🔄 Restart</button>
    `;
    generateMemoryCards();
}

let flippedCards = [];
let matchedPairs = 0;

function generateMemoryCards() {
    const memoryGrid = document.getElementById("memory-grid");
    memoryGrid.innerHTML = "";
    memoryGrid.style.display = "grid";
    memoryGrid.style.gridTemplateColumns = "repeat(5, 1fr)";
    memoryGrid.style.gap = "10px";
    memoryGrid.style.justifyContent = "center";

    const icons = ["🍎", "🍌", "🍉", "🍇", "🍒", "🍓", "🥑", "🍍", "🥕", "🍆"];
    let cards = [...icons, ...icons, ...icons, ...icons, ...icons]; // 5x5 Grid
    cards.sort(() => Math.random() - 0.5);

    cards.forEach((card, index) => {
        let cardElement = document.createElement("button");
        cardElement.classList.add("memory-card", "btn", "btn-light");
        cardElement.dataset.card = card;
        cardElement.dataset.index = index;
        cardElement.textContent = "❓";
        cardElement.onclick = () => flipCard(cardElement);
        memoryGrid.appendChild(cardElement);
    });
}

function flipCard(cardElement) {
    if (flippedCards.length < 2 && !flippedCards.includes(cardElement)) {
        cardElement.textContent = cardElement.dataset.card;
        flippedCards.push(cardElement);
        if (flippedCards.length === 2) setTimeout(checkMemoryMatch, 500);
    }
}

function checkMemoryMatch() {
    if (flippedCards[0].dataset.card === flippedCards[1].dataset.card) {
        flippedCards.forEach(card => card.style.visibility = "hidden");
        matchedPairs++;
    } else {
        flippedCards.forEach(card => card.textContent = "❓");
    }
    flippedCards = [];

    if (matchedPairs === 10) {
        document.getElementById("memory-grid").innerHTML = `<h4>🎉 You won! All pairs matched.</h4>`;
    }
}

/* Number Guess */
let numberToGuess;
function startNumberGuess() {
    numberToGuess = Math.floor(Math.random() * 10) + 1;
    document.getElementById("game-content").innerHTML = `
        <h3>Number Guessing Game</h3>
        <p>Guess a number between 1 and 10:</p>
        <input type="number" id="guess" min="1" max="10" class="form-control w-50 mx-auto">
        <button class="btn btn-primary mt-2" onclick="checkNumberGuess()">Submit</button>
        <p id="guess-result" class="text-center mt-2"></p>
        <button class="btn btn-secondary mt-3" onclick="startNumberGuess()">🔄 Restart</button>
    `;
}

function checkNumberGuess() {
    const guess = parseInt(document.getElementById("guess").value);
    const resultElement = document.getElementById("guess-result");

    if (isNaN(guess) || guess < 1 || guess > 10) {
        resultElement.innerHTML = "⚠️ Enter a number between 1-10.";
        return;
    }

    resultElement.innerHTML =
        guess === numberToGuess ? "🎉 Correct!" : guess < numberToGuess ? "🔼 Try higher!" : "🔽 Try lower!";
}

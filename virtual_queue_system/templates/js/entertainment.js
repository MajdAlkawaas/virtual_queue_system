function playMusic() {
    const music = new Audio("music/relaxing.mp3");
    music.play();
    alert("Playing relaxing music...");
}

function startGame() {
    window.location.href = "game.html"; // Redirect to game page
}

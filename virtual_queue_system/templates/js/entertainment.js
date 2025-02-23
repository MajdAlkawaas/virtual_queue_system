// Music Player with Toggle
let music = new Audio("music/relaxing.mp3");
let isPlaying = false;

function playMusic() {
    if (!isPlaying) {
        music.play();
        isPlaying = true;
        document.getElementById("music-status").textContent = "🎵 Music Playing...";
        document.getElementById("music-btn").textContent = "⏸ Pause Music";
    } else {
        music.pause();
        isPlaying = false;
        document.getElementById("music-status").textContent = "🎵 Music Paused.";
        document.getElementById("music-btn").textContent = "▶ Play Music";
    }
}

//Game Start - Redirect to Game Page
function startGame() {
    window.location.href = "game.html";  
}

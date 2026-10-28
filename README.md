import base64
import streamlit as st

st.set_page_config(page_title="Flappy Bird Chú Chim Đội Mũ", layout="centered")


def get_image_base64(path):
  try:
    with open(path, "rb") as f:
      return base64.b64encode(f.read()).decode()
  except:
    return ""


img_base64 = get_image_base64("bird.png")

st.title("🐦 Flappy Bird - Chú Chim Đội Mũ Siêu Ngầu")

game_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  body {{ display: flex; justify-content: center; align-items: center; height: 100vh; background: #111; margin: 0; }}
  canvas {{ border: 4px solid #fff; box-shadow: 0px 0px 15px rgba(0,0,0,0.8); background: #70c5ce; cursor: pointer; }}
</style>
</head>
<body>
<canvas id="gameCanvas" width="400" height="550"></canvas>
<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const birdImg = new Image();
birdImg.src = "data:image/png;base64,{img_base64}";

let bird = {{ x: 50, y: 150, width: 45, height: 35, gravity: 0.6, lift: -10, velocity: 0 }};
let pipes = [];
let pipeWidth = 60, pipeGap = 150, pipeSpeed = 3;
let frameCount = 0, score = 0;

// Trạng thái game: 'START', 'PLAYING', 'OVER'
let gameState = 'START';

function spawnPipe() {{
  let topHeight = Math.floor(Math.random() * (canvas.height - pipeGap - 100)) + 50;
  pipes.push({{ x: canvas.width, top: topHeight, bottom: canvas.height - topHeight - pipeGap, passed: false }});
}}

function handleInput() {{
  if (gameState === 'START') {{
    gameState = 'PLAYING';
    resetGameVars();
    loop();
  }} else if (gameState === 'PLAYING') {{
    bird.velocity = bird.lift;
  }} else if (gameState === 'OVER') {{
    gameState = 'PLAYING';
    resetGameVars();
    loop();
  }}
}}

document.addEventListener("keydown", e => {{ if (e.code === "Space") {{ handleInput(); e.preventDefault(); }}}});
canvas.addEventListener("click", handleInput);

function resetGameVars() {{
  bird.y = 150; bird.velocity = 0; pipes = []; score = 0; frameCount = 0;
}}

function drawStartScreen() {{
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  // Vẽ chú chim trang trí ở màn hình chờ
  ctx.drawImage(birdImg, canvas.width / 2 - 25, canvas.height / 2 - 60, 50, 40);
  
  ctx.fillStyle = "#FFF";
  ctx.font = "bold 32px Arial";
  ctx.textAlign = "center";
  ctx.fillText("FLAPPY BIRD", canvas.width / 2, canvas.height / 2 - 10);
  
  ctx.fillStyle = "#FFEB3B";
  ctx.font = "bold 20px Arial";
  ctx.fillText("👉 Nhấn để Bắt Đầu 👈", canvas.width / 2, canvas.height / 2 + 40);
  ctx.textAlign = "left";
}}

function loop() {{
  if (gameState !== 'PLAYING') return;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (frameCount % 90 === 0) spawnPipe();

  for (let i = pipes.length - 1; i >= 0; i--) {{
    pipes[i].x -= pipeSpeed;
    ctx.fillStyle = "#73bf2e";
    ctx.fillRect(pipes[i].x, 0, pipeWidth, pipes[i].top);
    ctx.fillRect(pipes[i].x, canvas.height - pipes[i].bottom, pipeWidth, pipes[i].bottom);

    if (!pipes[i].passed && pipes[i].x + pipeWidth < bird.x) {{ score++; pipes[i].passed = true; }}

    if (bird.x < pipes[i].x + pipeWidth && bird.x + bird.width > pipes[i].x &&
        (bird.y < pipes[i].top || bird.y + bird.height > canvas.height - pipes[i].bottom)) {{
      gameState = 'OVER';
    }}

    if (pipes[i].x + pipeWidth < 0) pipes.splice(i, 1);
  }}

  bird.velocity += bird.gravity;
  bird.y += bird.velocity;
  ctx.drawImage(birdImg, bird.x, bird.y, bird.width, bird.height);

  if (bird.y + bird.height >= canvas.height || bird.y <= 0) gameState = 'OVER';

  ctx.fillStyle = "#FFF"; ctx.font = "bold 28px Arial";
  ctx.fillText("Điểm: " + score, 20, 40);

  if (gameState === 'OVER') {{
    ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#FF5722"; ctx.font = "bold 35px Arial"; ctx.textAlign = "center";
    ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 20);
    ctx.fillStyle = "#FFF"; ctx.font = "18px Arial";
    ctx.fillText("Click hoặc Space để chơi lại", canvas.width / 2, canvas.height / 2 + 25);
    ctx.textAlign = "left";
    return;
  }}

  frameCount++;
  requestAnimationFrame(loop);
}}

// Hiển thị màn hình chờ ban đầu khi vừa tải trang
birdImg.onload = () => {{
  drawStartScreen();
}};
</script>
</body>
</html>
"""

import streamlit.components.v1 as components

components.html(game_html, height=580, scrolling=False) scrolling=False)

import base64
import streamlit as st

st.set_page_config(page_title="Flappy Bird - 3D Custom", layout="centered")


def get_image_base64(path):
  try:
    with open(path, "rb") as f:
      return base64.b64encode(f.read()).decode()
  except:
    return ""


img_base64 = get_image_base64("bird.png")

st.title("🐦 Flappy Bird - Phiên Bản 3D Đỉnh Cao")

game_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  body {{ display: flex; justify-content: center; align-items: center; height: 100vh; background: #111; margin: 0; }}
  canvas {{ border: 4px solid #fff; box-shadow: 0px 0px 20px rgba(0,0,0,0.8); background: linear-gradient(#4ec0ca, #70c5ce); cursor: pointer; }}
</style>
</head>
<body>
<canvas id="gameCanvas" width="400" height="550"></canvas>
<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Xử lý tự động tách nền trắng của ảnh chú chim
const rawBirdImg = new Image();
let processedBirdImg = new Image();
let imageLoaded = false;
rawBirdImg.src = "data:image/png;base64,{img_base64}";

rawBirdImg.onload = function() {{
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = rawBirdImg.width;
    tempCanvas.height = rawBirdImg.height;
    const tempCtx = tempCanvas.getContext('2d');
    tempCtx.drawImage(rawBirdImg, 0, 0);
    
    const imgData = tempCtx.getImageData(0, 0, tempCanvas.width, tempCanvas.height);
    const data = imgData.data;
    // Tự động chuyển các pixel màu trắng hoặc gần trắng thành trong suốt (Transparent)
    for (let i = 0; i < data.length; i += 4) {{
        let r = data[i], g = data[i+1], b = data[i+2];
        if (r > 220 && g > 220 && b > 220) {{
            data[i+3] = 0; // Alpha = 0 (Trong suốt)
        }}
    }}
    tempCtx.putImageData(imgData, 0, 0);
    processedBirdImg.src = tempCanvas.toDataURL();
    imageLoaded = true;
    drawStartScreen();
}};

let bird = {{ x: 60, y: 200, width: 48, height: 36, gravity: 0.55, lift: -9, velocity: 0 }};
let pipes = [];
let pipeWidth = 65, pipeGap = 150, pipeSpeed = 3;
let frameCount = 0, score = 0;
let gameState = 'START';

function spawnPipe() {{
  let topHeight = Math.floor(Math.random() * (canvas.height - pipeGap - 120)) + 60;
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
  bird.y = 200; bird.velocity = 0; pipes = []; score = 0; frameCount = 0;
}}

function drawStartScreen() {{
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Vẽ nền trời 3D gradient
  let gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
  gradient.addColorStop(0, "#4ec0ca");
  gradient.addColorStop(1, "#2b8a95");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  if (imageLoaded) {{
      ctx.drawImage(processedBirdImg, canvas.width / 2 - 25, canvas.height / 2 - 70, 50, 40);
  }}

  ctx.fillStyle = "#FFF";
  ctx.font = "bold 34px Arial";
  ctx.textAlign = "center";
  ctx.shadowColor = "rgba(0, 0, 0, 0.5)";
  ctx.shadowBlur = 6;
  ctx.fillText("FLAPPY BIRD 3D", canvas.width / 2, canvas.height / 2 - 10);
  
  ctx.fillStyle = "#FFEB3B";
  ctx.font = "bold 22px Arial";
  ctx.fillText("👉 Nhấn để Bắt Đầu 👈", canvas.width / 2, canvas.height / 2 + 45);
  ctx.shadowBlur = 0;
  ctx.textAlign = "left";
}}

function loop() {{
  if (gameState !== 'PLAYING') return;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Vẽ nền trời
  let gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
  gradient.addColorStop(0, "#4ec0ca");
  gradient.addColorStop(1, "#3196a2");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  if (frameCount % 90 === 0) spawnPipe();

  // Vẽ ống nước kiểu 3D có viền bóng
  for (let i = pipes.length - 1; i >= 0; i--) {{
    pipes[i].x -= pipeSpeed;

    // Ống trên
    let pipeGradTop = ctx.createLinearGradient(pipes[i].x, 0, pipes[i].x + pipeWidth, 0);
    pipeGradTop.addColorStop(0, "#73bf2e");
    pipeGradTop.addColorStop(0.5, "#9de356");
    pipeGradTop.addColorStop(1, "#558022");
    ctx.fillStyle = pipeGradTop;
    ctx.fillRect(pipes[i].x, 0, pipeWidth, pipes[i].top);
    ctx.strokeStyle = "#335111";
    ctx.lineWidth = 3;
    ctx.strokeRect(pipes[i].x, 0, pipeWidth, pipes[i].top);

    // Ống dưới
    let pipeGradBot = ctx.createLinearGradient(pipes[i].x, 0, pipes[i].x + pipeWidth, 0);
    pipeGradBot.addColorStop(0, "#73bf2e");
    pipeGradBot.addColorStop(0.5, "#9de356");
    pipeGradBot.addColorStop(1, "#558022");
    ctx.fillStyle = pipeGradBot;
    ctx.fillRect(pipes[i].x, canvas.height - pipes[i].bottom, pipeWidth, pipes[i].bottom);
    ctx.strokeRect(pipes[i].x, canvas.height - pipes[i].bottom, pipeWidth, pipes[i].bottom);

    if (!pipes[i].passed && pipes[i].x + pipeWidth < bird.x) {{ score++; pipes[i].passed = true; }}

    if (bird.x < pipes[i].x + pipeWidth && bird.x + bird.width > pipes[i].x &&
        (bird.y < pipes[i].top || bird.y + bird.height > canvas.height - pipes[i].bottom)) {{
      gameState = 'OVER';
    }}

    if (pipes[i].x + pipeWidth < 0) pipes.splice(i, 1);
  }}

  // Cập nhật vật lý chim
  bird.velocity += bird.gravity;
  bird.y += bird.velocity;

  // Hiệu ứng xoay góc (chúc đầu xuống khi rơi, ngẩng lên khi bay) khi vẽ chim
  ctx.save();
  ctx.translate(bird.x + bird.width / 2, bird.y + bird.height / 2);
  let rotation = Math.min(Math.PI / 4, Math.max(-Math.PI / 4, bird.velocity * 0.08));
  ctx.rotate(rotation);

  if (imageLoaded) {{
      ctx.drawImage(processedBirdImg, -bird.width / 2, -bird.height / 2, bird.width, bird.height);
  }} else {{
      ctx.fillStyle = "#FFEB3B";
      ctx.beginPath();
      ctx.arc(0, 0, bird.width/2, 0, Math.PI * 2);
      ctx.fill();
  }}
  ctx.restore();

  // Kiểm tra chạm đất / chạm trần
  if (bird.y + bird.height >= canvas.height || bird.y <= 0) gameState = 'OVER';

  // Hiển thị điểm số 3D nổi bật
  ctx.fillStyle = "#FFF";
  ctx.font = "bold 32px Arial";
  ctx.shadowColor = "rgba(0, 0, 0, 0.6)";
  ctx.shadowBlur = 4;
  ctx.fillText("Điểm: " + score, 20, 45);
  ctx.shadowBlur = 0;

  if (gameState === 'OVER') {{
    ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = "#FF5722";
    ctx.font = "bold 40px Arial";
    ctx.textAlign = "center";
    ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 25);
    
    ctx.fillStyle = "#FFF";
    ctx.font = "20px Arial";
    ctx.fillText("Click hoặc Space để chơi lại", canvas.width / 2, canvas.height / 2 + 25);
    ctx.textAlign = "left";
    return;
  }}

  frameCount++;
  requestAnimationFrame(loop);
}}

setTimeout(() => {{
    if (!imageLoaded) drawStartScreen();
}, 600);
</script>
</body>
</html>
"""

import streamlit.components.v1 as components

components.html(game_html, height=580, scrolling=False)

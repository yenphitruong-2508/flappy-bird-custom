import base64
import streamlit as st

st.set_page_config(page_title="Flappy Bird - Retro Style", layout="centered")


def get_image_base64(path):
  try:
    with open(path, "rb") as f:
      return base64.b64encode(f.read()).decode()
  except:
    return ""


img_base64 = get_image_base64("bird.png")

st.title("🐦 Flappy Bird - Phiên Bản Cổ Điển Chuẩn Retro")

game_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  body {{ display: flex; justify-content: center; align-items: center; height: 100vh; background: #111; margin: 0; font-family: Arial, sans-serif; }}
  canvas {{ border: 4px solid #fff; box-shadow: 0px 0px 20px rgba(0,0,0,0.8); background: #4ec0ca; cursor: pointer; }}
</style>
</head>
<body>
<canvas id="gameCanvas" width="400" height="600"></canvas>
<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Tự động tách nền trắng của ảnh chú chim
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
    for (let i = 0; i < data.length; i += 4) {{
        let r = data[i], g = data[i+1], b = data[i+2];
        if (r > 220 && g > 220 && b > 220) {{
            data[i+3] = 0;
        }}
    }}
    tempCtx.putImageData(imgData, 0, 0);
    processedBirdImg.src = tempCanvas.toDataURL();
    imageLoaded = true;
    drawStartScreen();
}};

let bird = {{ x: 60, y: 220, width: 45, height: 35, gravity: 0.55, lift: -9, velocity: 0 }};
let pipes = [];
let pipeWidth = 65, pipeGap = 155, pipeSpeed = 3;
let frameCount = 0, score = 0;
let highScore = localStorage.getItem("flappy_highScore") || 0;
let gameState = 'START'; // 'START', 'PLAYING', 'OVER'

function spawnPipe() {{
  let topHeight = Math.floor(Math.random() * (canvas.height - pipeGap - 180)) + 60;
  pipes.push({{ x: canvas.width, top: topHeight, bottomHeight: canvas.height - topHeight - pipeGap, passed: false }});
}}

// Vẽ background phong cách retro (mây, thành phố, bụi cây)
function drawBackground() {{
  ctx.fillStyle = "#4ec0ca";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Mây
  ctx.fillStyle = "rgba(255, 255, 255, 0.8)";
  ctx.beginPath();
  ctx.arc(80, 120, 30, 0, Math.PI * 2);
  ctx.arc(110, 115, 40, 0, Math.PI * 2);
  ctx.arc(140, 125, 25, 0, Math.PI * 2);
  ctx.fill();

  ctx.beginPath();
  ctx.arc(300, 220, 35, 0, Math.PI * 2);
  ctx.arc(335, 210, 45, 0, Math.PI * 2);
  ctx.fill();

  // Tòa nhà thành phố phía sau[cite: 7]
  ctx.fillStyle = "#9cc6cb";
  ctx.fillRect(40, canvas.height - 220, 45, 220);
  ctx.fillRect(85, canvas.height - 180, 35, 180);
  ctx.fillRect(140, canvas.height - 250, 50, 250);
  ctx.fillRect(230, canvas.height - 200, 40, 200);
  ctx.fillRect(285, canvas.height - 240, 55, 240);

  // Bụi cây xanh[cite: 7]
  ctx.fillStyle = "#73bf2e";
  for (let i = 0; i < canvas.width; i += 40) {{
    ctx.beginPath();
    ctx.arc(i + 20, canvas.height - 120, 35, 0, Math.PI * 2);
    ctx.fill();
  }}
  ctx.fillStyle = "#558022";
  ctx.fillRect(0, canvas.height - 100, canvas.width, 100);
}}

function drawPipe(pipe) {{
  let pipeColor = "#73bf2e";
  let pipeBorder = "#558022";
  let capHeight = 26;
  let capOverflow = 4;

  // Ống trên
  ctx.fillStyle = pipeColor;
  ctx.fillRect(pipe.x, 0, pipeWidth, pipe.top);
  ctx.strokeStyle = pipeBorder;
  ctx.lineWidth = 3;
  ctx.strokeRect(pipe.x, 0, pipeWidth, pipe.top);
  
  ctx.fillRect(pipe.x - capOverflow, pipe.top - capHeight, pipeWidth + (capOverflow * 2), capHeight);
  ctx.strokeRect(pipe.x - capOverflow, pipe.top - capHeight, pipeWidth + (capOverflow * 2), capHeight);

  // Ống dưới
  let bottomY = canvas.height - pipe.bottomHeight;
  ctx.fillStyle = pipeColor;
  ctx.fillRect(pipe.x, bottomY, pipeWidth, pipe.bottomHeight);
  ctx.strokeRect(pipe.x, bottomY, pipeWidth, pipe.bottomHeight);

  ctx.fillRect(pipe.x - capOverflow, bottomY, pipeWidth + (capOverflow * 2), capHeight);
  ctx.strokeRect(pipe.x - capOverflow, bottomY, pipeWidth + (capOverflow * 2), capHeight);
}}

function drawBird(x, y, w, h, velocity) {{
  ctx.save();
  ctx.translate(x + w / 2, y + h / 2);
  let rotation = Math.min(Math.PI / 4, Math.max(-Math.PI / 4, velocity * 0.08));
  ctx.rotate(rotation);

  if (imageLoaded) {{
      ctx.drawImage(processedBirdImg, -w / 2, -h / 2, w, h);
  }} else {{
      ctx.fillStyle = "#FFEB3B";
      ctx.beginPath();
      ctx.arc(0, 0, w/2, 0, Math.PI * 2);
      ctx.fill();
  }}
  ctx.restore();
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

document.addEventListener("keydown", e => {{ 
  if (e.code === "Space") {{ 
    handleInput(); 
    e.preventDefault(); 
  }} 
}});

canvas.addEventListener("click", e => {{
  handleInput();
}});

function resetGameVars() {{
  bird.y = 220; 
  bird.velocity = 0; 
  pipes = []; 
  score = 0; 
  frameCount = 0;
}}

function drawStartScreen() {{
  drawBackground();
  drawBird(canvas.width / 2 - 25, canvas.height / 2 - 80, 50, 40, 0);

  ctx.fillStyle = "#FFF";
  ctx.font = "bold 38px Arial";
  ctx.textAlign = "center";
  ctx.shadowColor = "rgba(0, 0, 0, 0.6)";
  ctx.shadowBlur = 6;
  ctx.fillText("FLAPPY BIRD", canvas.width / 2, canvas.height / 2 - 15);
  
  ctx.fillStyle = "#FFEB3B";
  ctx.font = "bold 24px Arial";
  ctx.fillText("👉 Nhấn để Bắt Đầu 👈", canvas.width / 2, canvas.height / 2 + 45);
  ctx.shadowBlur = 0;
  ctx.textAlign = "left";
}}

function drawScorecard() {{
  ctx.fillStyle = "rgba(0, 0, 0, 0.6)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  let boxWidth = 300;
  let boxHeight = 220;
  let boxX = (canvas.width - boxWidth) / 2;
  let boxY = (canvas.height - boxHeight) / 2 - 20;

  // Bảng điểm retro vàng
  ctx.fillStyle = "#ded895";
  ctx.strokeStyle = "#55380c";
  ctx.lineWidth = 4;
  ctx.fillRect(boxX, boxY, boxWidth, boxHeight);
  ctx.strokeRect(boxX, boxY, boxWidth, boxHeight);

  ctx.fillStyle = "#d9381e";
  ctx.font = "bold 32px Arial";
  ctx.textAlign = "center";
  ctx.fillText("GAME OVER", canvas.width / 2, boxY + 40);

  // Điểm hiện tại
  ctx.fillStyle = "#55380c";
  ctx.font = "bold 20px Arial";
  ctx.textAlign = "left";
  ctx.fillText("Điểm hiện tại:", boxX + 30, boxY + 95);
  ctx.textAlign = "right";
  ctx.fillText(score, boxX + boxWidth - 30, boxY + 95);

  // Điểm kỷ lục cao nhất
  ctx.textAlign = "left";
  ctx.fillText("Cao nhất:", boxX + 30, boxY + 140);
  ctx.textAlign = "right";
  ctx.fillText(highScore, boxX + boxWidth - 30, boxY + 140);

  // Nút Thử Lại
  let btnWidth = 160;
  let btnHeight = 45;
  let btnX = (canvas.width - btnWidth) / 2;
  let btnY = boxY + boxHeight + 20;

  ctx.fillStyle = "#e06322";
  ctx.strokeStyle = "#fff";
  ctx.lineWidth = 3;
  ctx.fillRect(btnX, btnY, btnWidth, btnHeight);
  ctx.strokeRect(btnX, btnY, btnWidth, btnHeight);

  ctx.fillStyle = "#FFF";
  ctx.font = "bold 22px Arial";
  ctx.textAlign = "center";
  ctx.fillText("🔄 THỬ LẠI", canvas.width / 2, btnY + 30);
  ctx.textAlign = "left";
}}

function loop() {{
  if (gameState !== 'PLAYING') return;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  drawBackground();

  if (frameCount % 90 === 0) spawnPipe();

  for (let i = pipes.length - 1; i >= 0; i--) {{
    pipes[i].x -= pipeSpeed;
    drawPipe(pipes[i]);

    if (!pipes[i].passed && pipes[i].x + pipeWidth < bird.x) {{
      score++;
      pipes[i].passed = true;
      if (score > highScore) {{
        highScore = score;
        localStorage.setItem("flappy_highScore", highScore);
      }}
    }}

    let topCollision = bird.x < pipes[i].x + pipeWidth && bird.x + bird.width > pipes[i].x && bird.y < pipes[i].top;
    let bottomCollision = bird.x < pipes[i].x + pipeWidth && bird.x + bird.width > pipes[i].x && bird.y + bird.height > canvas.height - pipes[i].bottomHeight;

    if (topCollision || bottomCollision) {{
      gameState = 'OVER';
    }}

    if (pipes[i].x + pipeWidth < 0) {{
      pipes.splice(i, 1);
    }}
  }}

  bird.velocity += bird.gravity;
  bird.y += bird.velocity;
  drawBird(bird.x, bird.y, bird.width, bird.height, bird.velocity);

  if (bird.y + bird.height >= canvas.height - 100 || bird.y <= 0) {{
    gameState = 'OVER';
  }}

  // Hiển thị điểm số khi đang chơi
  ctx.fillStyle = "#FFF";
  ctx.font = "bold 40px Arial";
  ctx.textAlign = "center";
  ctx.shadowColor = "rgba(0, 0, 0, 0.5)";
  ctx.shadowBlur = 4;
  ctx.fillText(score, canvas.width / 2, 70);
  ctx.shadowBlur = 0;
  ctx.textAlign = "left";

  if (gameState === 'OVER') {{
    drawScorecard();
    return;
  }}

  frameCount++;
  requestAnimationFrame(loop);
}}

setTimeout(() => {{
    drawStartScreen();
}, 200);
</script>
</body>
</html>
"""

import streamlit.components.v1 as components

components.html(game_html, height=620, scrolling=False)

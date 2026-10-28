import base64
import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Flappy Bird - Chú Chim Đội Mũ", page_icon="🐦", layout="centered"
)


# Hàm chuyển đổi ảnh cục bộ sang base64 để nhúng trực tiếp vào mã HTML/JS
def get_image_base64(path):
  try:
    with open(path, "rb") as f:
      data = f.read()
    return base64.b64encode(data).decode()
  except Exception:
    return ""


img_base64 = get_image_base64("bird.png")

st.title("🐦 Flappy Bird: Phiên bản Chú Chim Đội Mũ")
st.markdown("Nhấn phím **Space** hoặc bấm vào màn hình game để chú chim bay lên!")

# Mã HTML, CSS và JavaScript hoàn chỉnh cho game Flappy Bird sử dụng ảnh custom
game_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  body {{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: #222;
    margin: 0;
    font-family: Arial, sans-serif;
  }}
  canvas {{
    border: 4px solid #fff;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.8);
    background: #70c5ce;
    cursor: pointer;
  }}
</style>
</head>
<body>

<canvas id="gameCanvas" width="400" height="600"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Tải hình ảnh chú chim từ base64
const birdImg = new Image();
birdImg.src = "data:image/png;base64,{img_base64}";

// Biến trạng thái game
let bird = {{
  x: 50,
  y: 150,
  width: 45,
  height: 35,
  gravity: 0.6,
  lift: -10,
  velocity: 0
}};

let pipes = [];
let pipeWidth = 60;
let pipeGap = 160;
let pipeSpeed = 3;
let frameCount = 0;
let score = 0;
let isGameOver = false;

// Khởi tạo ống nước đầu tiên
function spawnPipe() {{
  let minHeight = 50;
  let maxHeight = canvas.height - pipeGap - 50;
  let topHeight = Math.floor(Math.random() * (maxHeight - minHeight + 1)) + minHeight;
  
  pipes.push({{
    x: canvas.width,
    top: topHeight,
    bottom: canvas.height - topHeight - pipeGap,
    passed: false
  }});
}}

// Điều khiển bay lên khi nhấn phím Space hoặc click chuột
document.addEventListener("keydown", function(e) {{
  if (e.code === "Space") {{
    if (isGameOver) {{
      resetGame();
    }} else {{
      bird.velocity = bird.lift;
    }}
    e.preventDefault();
  }}
}});

canvas.addEventListener("click", function() {{
  if (isGameOver) {{
    resetGame();
  }} else {{
    bird.velocity = bird.lift;
  }}
}});

function resetGame() {{
  bird.y = 150;
  bird.velocity = 0;
  pipes = [];
  score = 0;
  frameCount = 0;
  isGameOver = false;
  loop();
}}

function loop() {{
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // 1. Cập nhật và vẽ ống nước
  if (frameCount % 90 === 0) {{
    spawnPipe();
  }}

  for (let i = pipes.length - 1; i >= 0; i--) {{
    pipes[i].x -= pipeSpeed;

    // Vẽ ống trên
    ctx.fillStyle = "#73bf2e";
    ctx.fillRect(pipes[i].x, 0, pipeWidth, pipes[i].top);
    ctx.strokeStyle = "#558022";
    ctx.lineWidth = 3;
    ctx.strokeRect(pipes[i].x, 0, pipeWidth, pipes[i].top);

    // Vẽ ống dưới
    ctx.fillRect(pipes[i].x, canvas.height - pipes[i].bottom, pipeWidth, pipes[i].bottom);
    ctx.strokeRect(pipes[i].x, canvas.height - pipes[i].bottom, pipeWidth, pipes[i].bottom);

    // Kiểm tra ghi điểm
    if (!pipes[i].passed && pipes[i].x + pipeWidth < bird.x) {{
      score++;
      pipes[i].passed = true;
    }}

    // Kiểm tra va chạm
    if (
      bird.x < pipes[i].x + pipeWidth &&
      bird.x + bird.width > pipes[i].x &&
      (bird.y < pipes[i].top || bird.y + bird.height > canvas.height - pipes[i].bottom)
    ) {{
      isGameOver = true;
    }}

    // Xóa ống đã ra ngoài màn hình
    if (pipes[i].x + pipeWidth < 0) {{
      pipes.splice(i, 1);
    }}
  }}

  // 2. Cập nhật và vẽ chú chim
  bird.velocity += bird.gravity;
  bird.y += bird.velocity;

  // Vẽ hình ảnh chú chim lên canvas
  ctx.drawImage(birdImg, bird.x, bird.y, bird.width, bird.height);

  // Kiểm tra va chạm đất hoặc trần nhà
  if (bird.y + bird.height >= canvas.height || bird.y <= 0) {{
    isGameOver = true;
  }}

  // 3. Hiển thị điểm số
  ctx.fillStyle = "#FFF";
  ctx.font = "bold 30px Arial";
  ctx.shadowColor = "rgba(0, 0, 0, 0.5)";
  ctx.shadowBlur = 4;
  ctx.fillText("Điểm: " + score, 20, 40);
  ctx.shadowBlur = 0; // Reset shadow

  // 4. Xử lý khi Game Over
  if (isGameOver) {{
    ctx.fillStyle = "rgba(0, 0, 0, 0.6)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#FF5722";
    ctx.font = "bold 40px Arial";
    ctx.textAlign = "center";
    ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 20);

    ctx.fillStyle = "#FFF";
    ctx.font = "20px Arial";
    ctx.fillText("Nhấn chuột hoặc phím Space để chơi lại", canvas.width / 2, canvas.height / 2 + 30);
    ctx.textAlign = "left"; // Reset align
    return;
  }}

  frameCount++;
  requestAnimationFrame(loop);
}}

// Bắt đầu vòng lặp game khi ảnh đã tải xong
birdImg.onload = function() {{
  loop();
}};
</script>

</body>
</html>
"""

# Nhúng HTML vào Streamlit thông qua thành phần components.html
import streamlit.components.v1 as components

components.html(game_html, height=620, scrolling=False)
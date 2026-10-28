import base64
import streamlit as st

st.set_page_config(page_title="Flappy Bird - Retro Style", layout="centered")

st.title("🐦 Flappy Bird - Phiên Bản Cổ Điển Chuẩn Retro")


def get_image_base64(path):
  try:
    with open(path, "rb") as f:
      return base64.b64encode(f.read()).decode()
  except:
    return ""


img_base64 = get_image_base64("bird.png")

# Đọc file giao diện HTML game
try:
  with open("index.html", "r", encoding="utf-8") as f:
    game_html = f.read()
  # Chèn ảnh chú chim vào code game
  game_html = game_html.replace("INSERT_BIRD_BASE64_HERE", img_base64)
except FileNotFoundError:
  game_html = (
      "<h1>Chưa tìm thấy file index.html, vui lòng kiểm tra lại!</h1>"
  )

import streamlit.components.v1 as components

components.html(game_html, height=620, scrolling=False)

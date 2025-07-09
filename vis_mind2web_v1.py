"""
Mind2Web Visualizer (Streamlit)

Run with:
    streamlit run vis_mind2web.py
"""

import json
import os
from typing import Tuple

import streamlit as st
from PIL import Image, ImageDraw


# ---------- Helper Functions ----------
def load_data(json_file: str) -> list:
    """Load and return the full Mind2Web JSON list."""
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def draw_bbox(
    img_path: str,
    bbox: dict,
    radius: int = 4,
) -> Tuple[Image.Image, bool]:
    """
    Open an image, draw bounding-box + center dot, and return it.
    Returns (image, success_flag).
    """
    if not os.path.exists(img_path):
        return None, False

    img = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    x1 = bbox.get("x", 0)
    y1 = bbox.get("y", 0)
    x2 = x1 + bbox.get("width", 0)
    y2 = y1 + bbox.get("height", 0)

    # red rectangle
    draw.rectangle([(x1, y1), (x2, y2)], outline=(255, 0, 0), width=2)
    # green center point
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    draw.ellipse(
        [(cx - radius, cy - radius), (cx + radius, cy + radius)],
        fill=(0, 255, 0),
    )
    return img, True


# ---------- Streamlit Layout ----------
st.set_page_config(page_title="Mind2Web Visualizer", layout="wide")
st.title("Mind2Web Sample Explorer")

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Settings")

# file-path inputs
json_path = st.sidebar.text_input(
    label="JSON path",
    value="/home/t-rsun/code/Adaptive-Multimodal-Agent/data/datasets/Mind2Web/metadata/hf_train.json",
)
image_root = st.sidebar.text_input(
    label="Image root",
    value="/home/t-rsun/code/Adaptive-Multimodal-Agent/data/datasets/Mind2Web/images",
)

# load button
if st.sidebar.button("Load / Reload JSON"):
    try:
        st.session_state["data"] = load_data(json_path)
        st.success(f"Loaded {len(st.session_state['data'])} samples.")
    except Exception as e:
        st.error(f"Failed to load JSON: {e}")

data = st.session_state.get("data", None)
if data is None:
    st.info("👈 Please load JSON and view dataset")
    st.stop()

# optional filtering
domains = sorted({item.get("domain", "") for item in data})
selected_domain = st.sidebar.selectbox("Filter by domain", ["<All>"] + domains)
if selected_domain != "<All>":
    data = [d for d in data if d.get("domain") == selected_domain]

total = len(data)
if total == 0:
    st.warning("No samples found after filtering.")
    st.stop()

# choose sample index
idx = st.sidebar.slider("Sample index", 0, total - 1, 0)
item = data[idx]

# ---------- Display Metadata ----------
st.subheader(f"Sample #{idx}  —  ID: {item.get('id')}")
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
**Task**: {item.get("task")}  
**Domain**: {item.get("domain")}  
**Action type**: {item.get("step", {}).get("operation", {}).get("op", "")}  
"""
    )

    # text typed by TYPE action
    op_info = item.get("step", {}).get("operation", {})
    if op_info.get("op") == "TYPE":
        st.markdown(f"**Typed text**: `{op_info.get('value', '')}`")

# ---------- Display Image ----------
rel_path = item.get("img_url", "")
full_path = os.path.join(image_root, rel_path)
img, ok = draw_bbox(full_path, item.get("step", {}).get("bbox", {}))

with col2:
    if ok:
        st.image(img, caption=rel_path, use_column_width=True)
    else:
        st.error(f"Image not found: {full_path}")

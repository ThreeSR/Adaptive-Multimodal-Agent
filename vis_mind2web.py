"""
Mind2Web Episode Visualizer  (Streamlit)

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
    """Load the entire episode list."""
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


def draw_bbox(img_path: str, bbox: dict, radius: int = 4) -> Tuple[Image.Image, bool]:
    """
    Open an image, draw bounding box + center dot, and return it.
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

    draw.rectangle([(x1, y1), (x2, y2)], outline=(255, 0, 0), width=2)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    draw.ellipse(
        [(cx - radius, cy - radius), (cx + radius, cy + radius)],
        fill=(0, 255, 0),
    )
    return img, True


def resolve_img_path(annotation_id: str, action_uid: str, image_root: str) -> str:
    """Image naming: <annotation_id>-<action_uid>.jpg"""
    return os.path.join(image_root, f"{annotation_id}-{action_uid}.jpg")


# ---------- Streamlit Layout ----------
st.set_page_config(page_title="Mind2Web Episode Visualizer", layout="wide")
st.title("Mind2Web Episode Explorer")

# ---------- Sidebar Controls ----------
st.sidebar.header("⚙️ Settings")

json_path = st.sidebar.text_input(
    label="JSON path",
    value=(
        "/mnt/data1/t-rsun/datasets/"
        "Mind2Web/metadata/mind2web_data_train.json"
    ),
)
image_root = st.sidebar.text_input(
    label="Image root",
    value="/mnt/data1/t-rsun/datasets/Mind2Web/images",
)

# Load / reload data
if st.sidebar.button("Load / Reload JSON"):
    try:
        st.session_state["episodes"] = load_data(json_path)
        st.success(f"Loaded {len(st.session_state['episodes'])} episodes.")
        # reset index pointer when reloading
        st.session_state["epi_idx"] = 0
    except Exception as e:
        st.error(f"Failed to load JSON: {e}")

episodes = st.session_state.get("episodes")
if episodes is None:
    st.info("← Load a JSON file to start.")
    st.stop()

# ---------- Domain Filter ----------
domains = sorted({ep.get("domain", "") for ep in episodes})
selected_domain = st.sidebar.selectbox("Filter by domain", ["<All>"] + domains)
if selected_domain != "<All>":
    episodes = [ep for ep in episodes if ep.get("domain") == selected_domain]

if not episodes:
    st.warning("No episodes found after filtering.")
    st.stop()

# ---------- Episode Index State ----------
if "epi_idx" not in st.session_state:
    st.session_state["epi_idx"] = 0
max_idx = len(episodes) - 1


def set_index(new_idx: int) -> None:
    """Clamp and set episode index in session state."""
    st.session_state["epi_idx"] = new_idx % (max_idx + 1)


# ---------- Navigation Widgets ----------
col_nav_left, col_nav_mid, col_nav_right = st.sidebar.columns([1, 1, 1])

with col_nav_left:
    if st.button("◀ Prev"):
        set_index(st.session_state["epi_idx"] - 1)

with col_nav_mid:
    # number_input allows direct jump by index
    entered_idx = st.number_input(
        "Go to",
        min_value=0,
        max_value=max_idx,
        value=st.session_state["epi_idx"],
        step=1,
        key="go_to_idx",
    )
    if entered_idx != st.session_state["epi_idx"]:
        set_index(int(entered_idx))

with col_nav_right:
    if st.button("Next ▶"):
        set_index(st.session_state["epi_idx"] + 1)

epi_idx = st.session_state["epi_idx"]
episode = episodes[epi_idx]

# ---------- Episode Metadata ----------
st.subheader(f"Episode #{epi_idx} — annotation_id: {episode.get('annotation_id')}")
st.markdown(
    f"""
**Website**: {episode.get("website")}  
**Domain**: {episode.get("domain")} / {episode.get("subdomain")}  
**Confirmed task**: {episode.get("confirmed_task")}  
**Total steps**: {len(episode.get("actions", []))}  
"""
)

# ---------- Show All Actions ----------
actions = episode.get("actions", [])
reprs = episode.get("action_reprs", [])

if not actions:
    st.error("This episode contains no actions.")
    st.stop()

for idx, action in enumerate(actions):
    action_repr = reprs[idx] if idx < len(reprs) else "<no repr>"
    with st.expander(f"Step {idx} — {action.get('operation', {}).get('op', '')}", expanded=False):
        col1, col2 = st.columns([1, 1.6])

        # ---- Left: Metadata ----
        with col1:
            st.markdown(
                f"""
- **action_uid**: `{action.get("action_uid")}`  
- **repr**: `{action_repr}`  
- **original_op**: `{action.get("operation", {}).get("original_op")}`  
- **op**: `{action.get("operation", {}).get("op")}`  
- **value / typed text**: `{action.get("operation", {}).get("value", "")}`  
"""
            )

        # ---- Right: Image ----
        img_path = resolve_img_path(
            episode.get("annotation_id", "unknown"),
            action.get("action_uid"),
            image_root,
        )
        img, ok = draw_bbox(img_path, action.get("bbox", {}))
        with col2:
            if ok:
                st.image(
                    img,
                    caption=os.path.relpath(img_path, image_root),
                    use_column_width=True,
                )
            else:
                st.error(f"Image not found: {img_path}")

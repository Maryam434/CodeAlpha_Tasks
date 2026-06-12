import streamlit as st
import cv2
from ultralytics import YOLO
import numpy as np

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Vision Dashboard",
    page_icon="📦",
    layout="wide"
)

# ---------------- CUSTOM UI ---------------- #

st.markdown("""
    <style>
    body {
        background-color: #0f172a;
    }

    h1 {
        text-align: center;
        color: #00ffd5;
        font-size: 40px;
    }

    .stButton>button {
        background-color: #00ffd5;
        color: black;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 10px;
        margin: 5px;
    }

    .stButton>button:hover {
        background-color: #00bfa6;
        color: white;
    }

    .card {
        background-color: #111827;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        color: white;
    }

    </style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #

st.markdown("<h1>📦 AI Vision Detection Dashboard</h1>", unsafe_allow_html=True)

st.markdown("---")

# ---------------- LOAD MODEL ---------------- #

@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("⚙️ Control Panel")

start = st.sidebar.button("🎥 Start Camera")
stop = st.sidebar.button("🛑 Stop Camera")

st.sidebar.markdown("---")

st.sidebar.info("Real-time AI object detection using YOLOv8")

# ---------------- MAIN UI ---------------- #

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">📡 Status: Ready</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">🧠 Model: YOLOv8n</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">🎯 Detection: Active AI Vision</div>', unsafe_allow_html=True)

st.markdown("---")

frame_window = st.image([])

cap = cv2.VideoCapture(0)

object_count = 0

# ---------------- DETECTION ---------------- #

if start:

    st.success("🚀 Camera Started Successfully")

    while True:

        ret, frame = cap.read()

        if not ret:
            st.error("Camera Not Found!")
            break

        results = model(frame)

        object_count = 0

        for r in results:
            for box in r.boxes:

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls = int(box.cls[0])

                label = f"{model.names[cls]} {conf*100:.1f}%"

                object_count += 1

                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
                cv2.putText(frame, label, (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        # show object count
        cv2.putText(frame, f"Objects: {object_count}", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_window.image(frame)

        if stop:
            break

cap.release()

st.markdown("---")
st.caption("CodeAlpha Internship Project | AI Vision System")
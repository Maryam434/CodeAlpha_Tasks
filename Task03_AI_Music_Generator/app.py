import streamlit as st
import numpy as np
from scipy.io.wavfile import write
import random

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Music Generator",
    page_icon="🎵",
    layout="centered"
)

# ---------------- CUSTOM UI STYLE ---------------- #

st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
    }

    h1 {
        text-align: center;
        color: #00ffd5;
        font-size: 42px;
        font-weight: bold;
    }

    .stButton>button {
        background-color: #00ffd5;
        color: black;
        padding: 10px 20px;
        font-size: 18px;
        border-radius: 10px;
        border: none;
    }

    .stButton>button:hover {
        background-color: #00c2a8;
        color: white;
    }

    .stSlider {
        color: #00ffd5;
    }

    .css-1d391kg {
        padding: 2rem;
        border-radius: 15px;
        background-color: #111827;
    }

    </style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #

st.markdown("<h1>🎵 AI Music Generator</h1>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:gray;'>Generate beautiful AI-powered music instantly 🎶</p>", unsafe_allow_html=True)

st.markdown("---")

# ---------------- NOTES ---------------- #

notes = {
    60: 261,
    62: 293,
    64: 329,
    65: 349,
    67: 392,
    69: 440,
    71: 493,
    72: 523
}

markov_chain = {
    60: [62, 64, 65],
    62: [60, 64, 67],
    64: [65, 67, 69],
    65: [64, 67, 69],
    67: [65, 69, 71],
    69: [67, 71, 72],
    71: [69, 72],
    72: [71, 69]
}

# ---------------- GENERATE MUSIC ---------------- #

def generate_music(length=40):
    sequence = []
    current = random.choice(list(notes.keys()))

    for _ in range(length):
        sequence.append(current)
        current = random.choice(markov_chain[current])

    return sequence

# ---------------- CREATE AUDIO ---------------- #

def create_audio(sequence, filename="ai_music.wav"):
    sample_rate = 44100
    audio = np.array([], dtype=np.float32)

    duration = 0.25

    for note in sequence:
        freq = notes[note]
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = np.sin(freq * t * 2 * np.pi)
        audio = np.concatenate((audio, wave))

    audio = audio * 32767
    audio = audio.astype(np.int16)

    write(filename, sample_rate, audio)

    return filename

# ---------------- UI CONTROLS ---------------- #

st.markdown("### 🎚️ Control Panel")

length = st.slider("Select Music Length 🎼", 10, 100, 30)

st.markdown("")

col1, col2 = st.columns(2)

with col1:
    st.info("🎯 AI generates melody based on Markov Chain")

with col2:
    st.success("🎧 Download WAV audio file")

st.markdown("---")

if st.button("🎶 Generate AI Music"):

    music = generate_music(length)
    file = create_audio(music)

    st.markdown("### 🎼 Generated Music Notes")
    st.write(music)

    st.success("✨ Music Generated Successfully!")

    with open(file, "rb") as f:
        st.download_button(
            label="⬇ Download AI Music (WAV)",
            data=f,
            file_name="ai_music.wav",
            mime="audio/wav"
        )

st.markdown("---")
st.caption("CodeAlpha Internship Project | AI Music Generation")
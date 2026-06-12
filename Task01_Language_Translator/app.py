import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS

# Page Config
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
.stApp{
    background-color:#f8fafc;
}

.main-title{
    background:linear-gradient(90deg,#4F46E5,#7C3AED);
    padding:25px;
    border-radius:15px;
    text-align:center;
    color:white;
    margin-bottom:20px;
}

.result-box{
    background:white;
    padding:20px;
    border-radius:12px;
    border-left:6px solid #4F46E5;
    box-shadow:0px 2px 10px rgba(0,0,0,0.1);
    font-size:18px;
}

.stButton > button{
    width:100%;
    background:linear-gradient(90deg,#4F46E5,#7C3AED);
    color:white;
    border:none;
    border-radius:10px;
    padding:12px;
    font-weight:bold;
}

.stButton > button:hover{
    color:white;
}

footer{
    visibility:hidden;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🌍 About Project")

    st.info("""
AI Language Translator

✨ Features

✔ Multiple Languages
✔ Text Translation
✔ Text To Speech
✔ Download Translation
✔ Modern UI
✔ Translation Statistics
""")

    st.markdown("---")
    st.success("CodeAlpha AI Internship")

# Header
st.markdown("""
<div class="main-title">
<h1>🌍 AI Language Translator</h1>
<p>Translate Text into Multiple Languages Instantly</p>
</div>
""", unsafe_allow_html=True)

# Languages
languages = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Arabic": "ar",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Russian": "ru"
}

# Input
text = st.text_area(
    "📝 Enter Text",
    height=200,
    placeholder="Type your text here..."
)

col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox(
        "🌐 Source Language",
        list(languages.keys())
    )

with col2:
    target_lang = st.selectbox(
        "🎯 Target Language",
        list(languages.keys())
    )

# Translate Button
if st.button("🚀 Translate Now"):

    if text.strip() == "":
        st.warning("⚠ Please enter some text.")

    else:
        try:

            translated_text = GoogleTranslator(
                source=languages[source_lang],
                target=languages[target_lang]
            ).translate(text)

            st.balloons()

            st.success("🎉 Translation Completed Successfully!")

            st.markdown("## ✅ Translation Result")

            st.markdown(
                f"""
                <div class="result-box">
                {translated_text}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("### 📊 Translation Statistics")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric("Characters", len(text))

            with c2:
                st.metric("Words", len(text.split()))

            with c3:
                st.metric("Status", "Done ✅")

            st.markdown("### 🔊 Listen Translation")

            tts = gTTS(translated_text)
            tts.save("translated_audio.mp3")

            with open("translated_audio.mp3", "rb") as audio_file:
                st.audio(audio_file.read())

            st.markdown("### ⬇ Download Translation")

            st.download_button(
                label="Download Text File",
                data=translated_text,
                file_name="translation.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error: {e}")

# Footer
st.markdown("---")

st.markdown("""
<div style="text-align:center;color:gray;">
❤️ Developed for CodeAlpha AI Internship
<br>
Powered by Python • Streamlit • Deep Translator • gTTS
</div>
""", unsafe_allow_html=True)
import streamlit as st
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- PAGE SETUP ---------------- #

st.set_page_config(
    page_title="AI University Admission Assistant",
    page_icon="🎓",
    layout="wide"
)

# ---------------- LOAD DATA ---------------- #

df = pd.read_csv("faq_data.csv")

# ---------------- SAFE PREPROCESS (NO NLTK) ---------------- #

def preprocess(text):
    text = str(text).lower()
    tokens = text.split()   # simple tokenization (no error)
    return " ".join(tokens)

df["processed"] = df["question"].apply(preprocess)

# ---------------- TF-IDF MODEL ---------------- #

vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(df["processed"])

# ---------------- SIDEBAR ---------------- #

with st.sidebar:
    st.title("🎓 Admission Assistant")

    st.markdown("---")

    st.write("AI-powered FAQ chatbot for university admissions.")

    st.write(f"Total FAQs: {len(df)}")

    st.markdown("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------- TITLE ---------------- #

st.title("🎓 AI University Admission Assistant")
st.caption("NLP + TF-IDF + Cosine Similarity Based Chatbot")

# ---------------- CHAT HISTORY ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- USER INPUT ---------------- #

user_question = st.chat_input("Ask your admission related question...")

if user_question:

    # save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.write(user_question)

    # preprocess input
    processed_question = preprocess(user_question)

    # vector conversion
    user_vector = vectorizer.transform([processed_question])

    # similarity check
    similarity = cosine_similarity(user_vector, question_vectors)

    best_match = similarity.argmax()
    confidence = similarity[0][best_match]

    # response logic
    if confidence < 0.25:
        response = "Sorry, I could not find a relevant answer. Please ask admission related questions."
    else:
        response = df.iloc[best_match]["answer"]

    # bot response
    with st.chat_message("assistant"):
        st.write(response)
        st.caption(f"Confidence Score: {confidence*100:.1f}%")

    # save bot message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
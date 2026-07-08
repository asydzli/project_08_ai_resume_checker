import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

from utils import read_pdf
from utils import read_docx

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY tidak ditemukan.")
    st.stop()

client = genai.Client(api_key=api_key)

st.set_page_config(
    page_title="AI Resume Checker",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Checker")

st.write(
    "Upload resume Anda lalu biarkan AI memberikan analisis dan saran perbaikan."
)

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

if st.button("🚀 Analisis Resume", use_container_width=True):

    if uploaded_file is None:

        st.warning("Silakan upload resume terlebih dahulu.")

    else:

        extension = uploaded_file.name.split(".")[-1]

        if extension == "pdf":
            text = read_pdf(uploaded_file)

        else:
            text = read_docx(uploaded_file)

        prompt = f"""
Berikut adalah isi resume.

{text}

Analisis resume tersebut.

Berikan jawaban menggunakan format berikut.

# Ringkasan Resume

# Kelebihan

# Kekurangan

# Saran Perbaikan

# ATS Friendly

Jelaskan apakah resume sudah ATS Friendly atau belum.

# Skor Resume

Berikan skor dari 1-100 beserta alasannya.

Gunakan Bahasa Indonesia.
"""

        with st.spinner("Menganalisis Resume..."):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                st.success("Analisis selesai!")

                st.markdown(response.text)

            except Exception as e:

                st.error(e)
                
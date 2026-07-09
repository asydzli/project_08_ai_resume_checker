import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


MODEL_NAME = "gemini-2.5-flash"
MAX_RESUME_CHARACTERS = 12000


def load_api_key() -> str | None:
    """Membaca API key Gemini dari file .env atau environment variable."""
    load_dotenv()
    return os.getenv("GEMINI_API_KEY")


def build_prompt(resume_text: str, target_role: str, job_description: str) -> str:
    """Menyusun prompt review resume agar hasilnya actionable."""
    return f"""
Anda adalah career coach untuk programmer pemula hingga intermediate.

Review resume berikut berdasarkan detail:
- Target posisi: {target_role}
- Deskripsi pekerjaan: {job_description or "Tidak disediakan"}

Aturan output:
- Gunakan bahasa Indonesia.
- Berikan skor resume dari 1 sampai 100.
- Tulis kekuatan utama resume.
- Tulis kelemahan atau bagian yang perlu diperbaiki.
- Berikan saran perbaikan yang spesifik dan mudah dilakukan.
- Berikan contoh rewrite untuk 3 bullet point yang lebih kuat.
- Jangan mengarang pengalaman baru yang tidak ada di resume.

Isi resume:
{resume_text}
"""


def check_resume(api_key: str, prompt: str) -> str:
    """Mengirim prompt ke Gemini dan mengembalikan hasil review resume."""
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return response.text or ""


def main() -> None:
    st.set_page_config(
        page_title="AI Resume Checker",
        page_icon="AI",
        layout="centered",
    )

    st.title("AI Resume Checker")
    st.caption("Review resume programmer dengan saran yang spesifik dan mudah diterapkan.")

    api_key = load_api_key()
    if not api_key:
        st.error("GEMINI_API_KEY belum ditemukan. Buat file .env dari .env.example.")
        st.stop()

    with st.sidebar:
        st.header("Pengaturan")
        target_role = st.text_input("Target posisi", value="Python Developer")
        st.info("Model: gemini-2.5-flash")

    with st.form("resume_form"):
        resume_text = st.text_area(
            "Tempel isi resume",
            height=280,
            placeholder="Tempel ringkasan profil, skill, pengalaman, project, dan pendidikan di sini.",
        )
        job_description = st.text_area(
            "Deskripsi pekerjaan (opsional)",
            height=160,
            placeholder="Tempel job description agar review lebih relevan.",
        )
        submitted = st.form_submit_button("Cek Resume")

    if submitted:
        clean_resume = resume_text.strip()
        clean_role = target_role.strip()
        clean_job_description = job_description.strip()

        if not clean_resume:
            st.warning("Masukkan isi resume terlebih dahulu.")
            st.stop()

        if not clean_role:
            st.warning("Masukkan target posisi terlebih dahulu.")
            st.stop()

        if len(clean_resume) < 150:
            st.warning("Isi resume terlalu pendek. Masukkan minimal 150 karakter.")
            st.stop()

        if len(clean_resume) > MAX_RESUME_CHARACTERS:
            st.warning(f"Resume terlalu panjang. Maksimal {MAX_RESUME_CHARACTERS} karakter.")
            st.stop()

        prompt = build_prompt(clean_resume, clean_role, clean_job_description)

        with st.spinner("Gemini sedang mengecek resume..."):
            try:
                result = check_resume(api_key, prompt)
            except Exception as error:
                st.error(f"Terjadi error saat menghubungi Gemini: {error}")
                st.stop()

        if not result.strip():
            st.warning("Gemini tidak mengembalikan hasil review. Coba lagi.")
            st.stop()

        st.subheader("Hasil Review Resume")
        st.markdown(result)


if __name__ == "__main__":
    main()

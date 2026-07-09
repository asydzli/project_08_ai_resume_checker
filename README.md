# Project 08 - AI Resume Checker

AI Resume Checker adalah aplikasi Streamlit untuk mengevaluasi resume programmer dan memberikan saran perbaikan yang spesifik. Project ini menggunakan Google Gemini API melalui package `google-genai`.

## Fitur

- Input isi resume
- Input target posisi
- Input deskripsi pekerjaan opsional
- Validasi panjang resume
- Error handling saat API gagal
- Output skor resume, kekuatan, kelemahan, dan contoh rewrite bullet point

## Teknologi

- Python 3.13+
- Streamlit
- Google Gemini API (`google-genai`)
- python-dotenv
- VS Code
- Virtual Environment

## Cara Menjalankan

1. Buat virtual environment.

```bash
python -m venv venv
```

2. Aktifkan virtual environment.

```bash
venv\Scripts\activate
```

3. Install dependency.

```bash
pip install -r requirements.txt
```

4. Buat file `.env` berdasarkan `.env.example`, lalu isi API key Gemini.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

5. Jalankan aplikasi.

```bash
streamlit run app.py
```

## Catatan

Jangan upload file `.env` ke repository. File tersebut sudah masuk ke `.gitignore`.

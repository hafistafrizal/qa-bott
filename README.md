# 🤖 QA Bot with LangChain, IBM watsonx, and Gradio

Proyek akhir ini adalah aplikasi *Question-Answering (QA)* berbasis *Retrieval-Augmented Generation* (RAG) yang dikembangkan untuk **Quest Analytics**. Asisten AI ini dirancang untuk membaca, memahami, dan menjawab pertanyaan berdasarkan dokumen PDF yang diunggah secara *real-time* menggunakan model LLM dari **IBM watsonx.ai** dan antarmuka **Gradio**.

---

## 📂 Struktur Proyek
```text
qa-bot/
├── my_env/               # Direktori virtual environment Python
├── qabot.py              # Skrip utama aplikasi QA Bot
└── README.md             # Dokumentasi proyek

```

---

## ⚙️ Prasyarat

Sebelum menginstal dan menjalankan aplikasi ini, pastikan komputer Anda telah terpasang:

* [Python](https://www.python.org/) (Direkomendasikan versi **3.11**)
* Git (Opsional, untuk sinkronisasi ke GitHub)
* Akun **IBM Cloud / watsonx.ai** (https://dataplatform.cloud.ibm.com) untuk mendapatkan `API Key` dan `Project ID`.

---

## 📥 Panduan Instalasi (Lokal / VS Code)

Ikuti langkah-langkah berikut di terminal komputer Anda (Command Prompt, PowerShell, atau Terminal VS Code):

### 1. Kloning atau Buka Folder Proyek

Buka folder proyek `qa-bot` melalui terminal Anda.

### 2. Buat dan Aktifkan Virtual Environment

* **Windows (PowerShell):**
```powershell
python -m venv my_env
.\my_env\Scripts\activate

```


* **macOS / Linux:**
```bash
python3 -m venv my_env
source my_env/bin/activate

```



### 3. Instal Dependensi yang Dibutuhkan

Instal seluruh *library* pendukung (LangChain, Gradio, ChromaDB, dll) dengan menjalankan perintah berikut:

```powershell
pip install gradio==4.44.0 ibm-watsonx-ai==1.1.2 langchain==0.2.11 langchain-community==0.2.10 langchain-ibm==0.1.11 chromadb==0.4.24 pypdf==4.3.1 pydantic==2.9.1 huggingface_hub==0.23.0 langchain-text-splitters langchain-classic

```

---

## 🔑 Konfigurasi Kredensial

Buka file `qabot.py`, lalu sesuaikan variabel kredensial IBM watsonx Anda pada bagian berikut:

```python
PROJECT_ID = "MASUKKAN_PROJECT_ID_ANDA"
API_KEY = "MASUKKAN_API_KEY_ANDA"
URL = "[https://us-south.ml.cloud.ibm.com](https://us-south.ml.cloud.ibm.com)" # Sesuaikan region server IBM Anda

```

---

## 🚀 Cara Menjalankan Aplikasi

1. Pastikan *virtual environment* Anda sudah aktif (ditandai dengan awalan `(my_env)` di terminal).
2. Jalankan skrip utama `qabot.py`:
```powershell
python qabot.py

```


3. Terminal akan menampilkan tautan lokal seperti berikut:
```text
Running on local URL:  [http://127.0.0.1:7860](http://127.0.0.1:7860)

```


4. Tahan tombol `Ctrl` lalu klik tautan tersebut, atau salin dan tempel ke peramban (*browser*) web Anda.
5. Antarmuka Gradio akan terbuka. Unggah dokumen PDF, ketik pertanyaan Anda (misalnya: *"Apa yang dibicarakan dalam makalah ini?"*), dan bot akan memberikan jawabannya secara instan!

---

## 🛠️ Komponen Utama Sistem

* **Document Loader (`PyPDFLoader`):** Membaca dan memuat isi file PDF mentah.
* **Text Splitter (`RecursiveCharacterTextSplitter`):** Memecah dokumen menjadi potongan-potongan teks (*chunks*) agar mudah diproses.
* **Embedding Model (`WatsonxEmbeddings`):** Mengubah teks menjadi representasi vektor menggunakan *IBM Slate model*.
* **Vector Database (`Chroma`):** Menyimpan dan melakukan pencarian vektor berbasis kesamaan (*similarity search*).
* **Retriever & QA Chain (`RetrievalQA`):** Mengambil data relevan dan memprosesnya dengan LLM (`mistralai/mixtral-8x7b-instruct-v01` / `ibm/granite-4-h-small`).
* **Frontend UI (`Gradio`):** Menyediakan antarmuka web interaktif yang ramah pengguna.

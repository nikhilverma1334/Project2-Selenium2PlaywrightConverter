# 🚀 Blast Converter: Selenium to Playwright

Blast Converter is a premium, high-speed migration tool designed to transform legacy **Selenium Java (TestNG)** test suites into modern **Playwright (JavaScript/TypeScript)** code using the power of local LLMs.

![Blast Converter UI](https://img.shields.io/badge/Aesthetics-Glassmorphism-blueviolet?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Powered%20By-Ollama-white?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green?style=for-the-badge)

## ✨ Features

*   **Real-time Streaming:** Watch your code being converted in real-time.
*   **Dual-Pane Editor:** Side-by-side comparison of Selenium vs. Playwright.
*   **Multi-Model Support:** Choose between `codellama`, `llama3.2`, or any model installed in your Ollama instance.
*   **Premium UI:** Modern dark-mode interface with Glassmorphism effects.
*   **Privacy First:** All conversions happen locally on your hardware via Ollama. No data ever leaves your machine.

## 🛠️ Architecture

*   **Frontend:** Vanilla JS, CSS3 (Glassmorphism), HTML5.
*   **Backend:** FastAPI (Python) with `httpx` for asynchronous streaming.
*   **Intelligence:** Local LLM integration via Ollama API.
*   **SOPs:** Pre-defined conversion protocols in `architecture/conversion_sop.md`.

## 🚀 Getting Started

### Prerequisites

1.  **Python 3.10+**
2.  **Ollama** (Installed and running)
3.  **Local Models:** 
    ```bash
    ollama pull codellama
    ollama pull llama3.2
    ```

### Installation

1.  Clone the repository or download the folder.
2.  Install dependencies:
    ```bash
    pip install fastapi uvicorn httpx python-dotenv
    ```
3.  Ensure Ollama is running in the background.

### Running the App

1.  Start the backend server:
    ```bash
    python backend/main.py
    ```
2.  Open your browser to:
    `http://localhost:8000`

## 📂 Project Structure

*   `backend/main.py` - FastAPI server handling LLM logic.
*   `backend/static/` - Frontend assets (HTML, CSS, JS).
*   `architecture/` - Standard Operating Procedures for conversion.
*   `tools/` - Utility scripts for verification and manual conversion.

## 📜 License

Project developed as part of the B.L.A.S.T Protocol. Built with Antigravity.

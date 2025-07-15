# SciBot: AI Chatbot for Science Students

## Table of Contents
- [Introduction](#introduction)  
- [Installation](#installation)  
- [Setting Up Your Gemini API Key](#setting-up-your-gemini-api-key)  
- [Usage](#usage)  
- [Features](#features)  
- [Screenshots](#screenshots)  
- [Troubleshooting](#troubleshooting)  
- [Contributing](#contributing)  
- [License](#license)  
- [Support Me](#support-me)

---

## Introduction

**SciBot** is a lightweight web-based AI chatbot designed to assist **university science students** in understanding complex academic materials using natural language. Built with Flask, Google Gemini API, and OCR tools, the app enables students to:
- Ask questions from uploaded past questions, PDFs, or notes.
- Chat with the bot for instant academic help.
- Analyze scanned images with OCR.
- Enjoy a clean, mobile-responsive interface.

This guide helps you deploy it locally or on a server.

---

## Installation

> 💡 Requires Python 3.10+ and pip

1. **Clone the repository**  
```bash
git clone https://github.com/Jaywinner/SCIBOT.git
cd SCIBOT
```

2. **Create a virtual environment (optional but recommended)**  
```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

3. **Install dependencies**  
```bash
pip install -r requirements.txt
```

---

## Setting Up Your Gemini API Key

This app uses Google's Gemini (Generative AI) to process documents and chat.

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)  
2. Copy your API key  
3. Open `app.py` and **replace** the placeholder line with your key:

```python
genai.configure(api_key="your_gemini_api_key_here")
```

4. Save the file.


 <img width="500" height="63" alt="INSERT API KEY" src="https://github.com/user-attachments/assets/1967090b-7650-4dee-9100-0c33e8e89e74" />

---

## Usage

Once installed and configured, run the app using:

```bash
python3 app.py
```

Then go to:

```
http://127.0.0.1:5000
```

Or on a server:

```
http://your-server-ip:5000
```

> You’ll be able to login/register and start chatting or uploading files.

---

## Features

| Feature | Description |
|--------|-------------|
|  AI Chat | Chatbot interface to ask questions based on documents |
|  File Upload | You can Upload past questions, PDFs, or .txt for context |
|  OCR Support | Extracts text from image-based scanned files |
|  Tailored for Science | Ideal for Physics, Chemistry, Biology, Math, etc |
|  User Auth | Login/register system for personalized experience |
|  Saved Context | Maintains document context during chat sessions |


## Screenshots

See previously uploaded past questions, if any
<img width="1366" height="685" alt="student chatbot demo interface" src="https://github.com/user-attachments/assets/697a4d89-6baa-4073-a537-2759fc7c988c" />

Register to be able to upload past question
<img width="706" height="619" alt="Upload page" src="https://github.com/user-attachments/assets/ffbb5f25-c103-4077-93e9-41d2ad1cb9c0" />

Select Past question to ask the AI assistant about
<img width="733" height="567" alt="chat page" src="https://github.com/user-attachments/assets/acfc5fae-9dda-4ca5-9e5f-a6fccffc6b50" />

Sample question with the OCR feature
<img width="733" height="567" alt="confirmed answer with ocr" src="https://github.com/user-attachments/assets/55857922-e6a2-436a-a6ef-f291992c3eb6" />







## Troubleshooting

| Issue | Fix |
|-------|-----|
| ❌ App not starting | Ensure Python 3.10+ is installed |
| 🔑 Gemini error | Make sure your API key is valid and in `app.py` |
| 📦 OCR not working | Install Tesseract: `sudo apt install tesseract-ocr` (Linux) |
| 🔒 Can't login | Make sure the database is created: `python3 app.py` will auto-create it |

---

## Contributing

We welcome contributions!

```bash
git clone https://github.com/Jaywinner/SCIBOT.git
cd SCIBOT
git checkout -b feature/my-new-feature
# make your changes
git commit -am "Add my feature"
git push origin feature/my-new-feature
```

Then open a pull request 👨🏽‍💻

---

## 📄 License

This project is licensed under the **MIT License**.  
See the `LICENSE` file for details.

---

## ☕ Support Me

If you found this project useful and want to support:

**Account Number**: 6834826017  
**Bank**: FCMB  
**Name**: Joseph Amodu (Jaywinner)

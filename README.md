
## 🧠 Code Assistant AI — PyQt5 App

An advanced AI-powered desktop assistant that helps you generate, explain, and fix code using the OpenAI GPT-4o-mini model. Built with **Python**, **PyQt5**, and **OpenAI API**, it includes features like:

### ✅ Key Features

* 🌑 **Dark Theme Modern UI**
* 🧠 **Ask AI using OpenAI GPT-4o-mini**
* 🎤 **Text-to-Speech** for output
* 📋 **Copy-to-Clipboard**
* 💾 **Save Q\&A as Styled PDF**
* 🕘 **Collapsible Search History**
* 🌐 **Internet fallback for errors**
* 🧩 **Syntax Highlighting & Structured Output**
* 🔘 **Copy Code buttons inside answers**
* 📄 **HTML/PDF output with same visual styles**
* ⌨️ **Press Enter to Ask**

---

## 📁 Folder Structure

```
code_assistant_app/
├── main.py                 # App entry point
├── gui.py                  # PyQt5 GUI with all features
├── openai_helper.py        # Handles OpenAI API interaction
├
├── history/                # Saved Q&A logs
│   └── log.txt
```

---

## 🚀 How to Run the App

### 1️⃣ Clone or Download

```bash
git clone https://github.com/yourname/code-assistant-app.git
cd code-assistant-app
```

### 2️⃣ Install Python Libraries

Make sure Python is installed (>= 3.7), then run:

```bash
pip install pyqt5 openai pyttsx3 pyperclip fpdf

```

### 3️⃣ Run the App

```bash
python main.py
```

---

## 🔑 OpenAI API Key

This app uses the new `OpenAI` SDK:

```python
from openai import OpenAI
client = OpenAI(api_key="YOUR_API_KEY")
```

> 🔐 Your API key is already embedded in `openai_helper.py`
> Make sure to **keep it safe and private**.

---

## 📷 Screenshots

| Ask AI                                                  | Output Panel                                                         |
| ------------------------------------------------------- | -------------------------------------------------------------------- |
| ![ask](https://via.placeholder.com/400x250?text=Ask+AI) | ![output](https://via.placeholder.com/400x250?text=Formatted+Answer) |

---

## ✨ Custom Styling

Answers are styled like web pages using HTML with:

* 🎨 Colors & fonts
* 📌 Headings/Subheadings
* 🧱 Code blocks
* 🧠 Copy buttons for code

---

## 📝 Logs & History

All your questions and answers are saved inside the `/history/log.txt` file.
Use the **"Show/Hide History"** button to view inside the app.

---

## 📄 Save as PDF

Click **💾 Save PDF** to download your answer with full formatting and styles.

---

## 📜 License

This project is free for educational and personal use.

---

Would you like me to ZIP this full app and share it as a download?

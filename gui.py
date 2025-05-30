import os
import html
import datetime
import pyttsx3
import pyperclip
from fpdf import FPDF
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QLabel, QApplication, QScrollArea, QFileDialog
)
from PyQt5.QtCore import Qt, QSettings
from openai_helper import ask_code_assistant


class CustomTextEdit(QTextEdit):
    def __init__(self, on_enter_callback):
        super().__init__()
        self.on_enter_callback = on_enter_callback

    def keyPressEvent(self, event):
        if (event.key() in (Qt.Key_Return, Qt.Key_Enter)) and event.modifiers() == Qt.ControlModifier:
            if self.toPlainText().strip():
                self.on_enter_callback()
        else:
            super().keyPressEvent(event)


class CodeAssistantGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Code Assistant AI")
        self.setMinimumSize(900, 700)

        self.settings = QSettings("YourCompany", "CodeAssistant")
        self.engine = pyttsx3.init()
        self.current_question = ""
        self.current_answer = ""
        self.dark_mode = self.settings.value("dark_mode", True, type=bool)

        self.input_box = CustomTextEdit(self.get_answer)
        self.input_box.setPlaceholderText("Ask something...")
        self.input_box.setFixedHeight(80)

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setAcceptRichText(True)
        self.output_box.setLineWrapMode(QTextEdit.WidgetWidth)
        self.output_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.ask_button = QPushButton("Ask")
        self.ask_button.clicked.connect(self.get_answer)

        self.copy_button = QPushButton("📋 Copy")
        self.copy_button.clicked.connect(self.copy_answer)

        self.speak_button = QPushButton("🔊 Speak")
        self.speak_button.clicked.connect(self.speak_answer)

        self.save_button = QPushButton("💾 Save PDF")
        self.save_button.clicked.connect(self.save_as_pdf)

        self.toggle_history_button = QPushButton("📜 Show/Hide History")
        self.toggle_history_button.clicked.connect(self.toggle_history)

        self.export_history_button = QPushButton("📤 Export History")
        self.export_history_button.clicked.connect(self.export_history)

        self.clear_button = QPushButton("🧹 Clear")
        self.clear_button.clicked.connect(self.clear_fields)

        self.regenerate_button = QPushButton("♻️ Regenerate")
        self.regenerate_button.clicked.connect(self.regenerate_answer)

        self.theme_button = QPushButton("🌓 Toggle Theme")
        self.theme_button.clicked.connect(self.toggle_theme)

        self.history_box = QTextEdit()
        self.history_box.setReadOnly(True)
        self.history_box.setVisible(False)

        self.history_scroll = QScrollArea()
        self.history_scroll.setWidgetResizable(True)
        self.history_scroll.setWidget(self.history_box)
        self.history_scroll.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("💬 Your Question:"))
        layout.addWidget(self.input_box)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ask_button)
        button_layout.addWidget(self.regenerate_button)
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.speak_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.toggle_history_button)
        button_layout.addWidget(self.export_history_button)
        button_layout.addWidget(self.theme_button)

        layout.addLayout(button_layout)
        layout.addWidget(QLabel("🧠 Assistant Reply:"))
        layout.addWidget(self.output_box)
        layout.addWidget(self.history_scroll)

        self.setLayout(layout)
        self.history_log = []

        self.apply_theme()

    def get_answer(self):
        question = self.input_box.toPlainText().strip()
        if not question:
            return
        try:
            self.current_question = question
            self.current_answer = ask_code_assistant(question)
            if self.current_answer:
                self.output_box.setHtml(self.format_output(question, self.current_answer))
                self.save_history(question, self.current_answer)
                self.input_box.clear()
        except Exception as e:
            self.output_box.setHtml(f"<p style='color:red;'>❌ Error: {str(e)}</p>")

    def regenerate_answer(self):
        if not self.current_question:
            return
        try:
            self.current_answer = ask_code_assistant(self.current_question)
            self.output_box.setHtml(self.format_output(self.current_question, self.current_answer))
            self.save_history(self.current_question, self.current_answer)
        except Exception as e:
            self.output_box.setHtml(f"<p style='color:red;'>❌ Error: {str(e)}</p>")

    def format_output(self, question, answer):
        return f"""
        <html>
        <head>
        <style>
            body {{ font-family: 'Segoe UI'; color: #00ffcc; background-color: #1e1e1e; }}
            h1 {{ color: #ffffff; font-size: 20px; }}
            h2 {{ color: #ffcc00; font-size: 17px; }}
            p {{ font-size: 14px; line-height: 1.5; }}
            pre {{
                background-color: #000000;
                color: #00ffaa;
                padding: 10px;
                border-radius: 5px;
                font-family: 'Courier New';
                white-space: pre-wrap;
            }}
        </style>
        </head>
        <body>
            <h1>🤖 Question:</h1>
            <p>{html.escape(question)}</p>
            <h2>💡 Answer:</h2>
            <div>{self.highlight_answer(answer)}</div>
        </body>
        </html>
        """

    def highlight_answer(self, answer):
        lines = html.escape(answer).split("\n")
        in_code = False
        html_lines = []
        in_list = False

        for line in lines:
            if "```" in line:
                html_lines.append("<pre>" if not in_code else "</pre>")
                in_code = not in_code
            elif in_code:
                html_lines.append(line)
            else:
                if line.strip().startswith("-"):
                    if not in_list:
                        html_lines.append("<ul>")
                        in_list = True
                    html_lines.append(f"<li>{line.strip()[1:].strip()}</li>")
                else:
                    if in_list:
                        html_lines.append("</ul>")
                        in_list = False
                    if ":" in line:
                        parts = line.split(":", 1)
                        html_lines.append(f"<b>{parts[0].strip()}:</b> {parts[1].strip()}<br>")
                    else:
                        html_lines.append(f"<p>{line}</p>")

        if in_code:
            html_lines.append("</pre>")
        if in_list:
            html_lines.append("</ul>")
        return "\n".join(html_lines)

    def speak_answer(self):
        try:
            self.engine.say(self.output_box.toPlainText())
            self.engine.runAndWait()
        except Exception as e:
            self.output_box.append(f"\n🔇 Text-to-Speech error: {str(e)}")

    def copy_answer(self):
        pyperclip.copy(self.output_box.toPlainText())

    def save_as_pdf(self):
        if not self.current_answer:
            return
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.set_text_color(30, 30, 30)
        text = f"Question:\n{self.current_question}\n\nAnswer:\n{self.current_answer}"
        pdf.multi_cell(0, 10, text, align='L')
        filename = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF files (*.pdf)")[0]
        if filename:
            if not filename.endswith(".pdf"):
                filename += ".pdf"
            pdf.output(filename)

    def save_history(self, question, answer):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}]\nQ: {question}\nA: {answer}\n\n"
        self.history_log.append(entry)
        if self.history_box.isVisible():
            self.history_box.clear()
            self.history_box.append("".join(self.history_log))
        if not os.path.exists("history"):
            os.makedirs("history")
        with open("history/log.txt", "a", encoding="utf-8") as file:
            file.write(entry)

    def toggle_history(self):
        visible = not self.history_box.isVisible()
        self.history_box.setVisible(visible)
        self.history_scroll.setVisible(visible)
        if visible:
            self.history_box.clear()
            self.history_box.append("".join(self.history_log))

    def export_history(self):
        if not self.history_log:
            return
        filename, _ = QFileDialog.getSaveFileName(self, "Save History", "", "Text Files (*.txt)")
        if filename:
            if not filename.endswith(".txt"):
                filename += ".txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.writelines(self.history_log)

    def clear_fields(self):
        self.input_box.clear()
        self.output_box.clear()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.settings.setValue("dark_mode", self.dark_mode)
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            self.setStyleSheet("background-color: #121212; color: #ffffff;")
            self.input_box.setStyleSheet("background-color: #1e1e1e; color: #ffffff; font-size: 16px;")
            self.output_box.setStyleSheet("background-color: #1e1e1e; color: #ffffff; font-size: 14px;")
            self.history_box.setStyleSheet("background-color: #1e1e1e; color: #aaaaaa; font-size: 12px;")
        else:
            self.setStyleSheet("background-color: #f5f5f5; color: #000000;")
            self.input_box.setStyleSheet("background-color: #ffffff; color: #000000; font-size: 16px;")
            self.output_box.setStyleSheet("background-color: #ffffff; color: #000000; font-size: 14px;")
            self.history_box.setStyleSheet("background-color: #ffffff; color: #333333; font-size: 12px;")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = CodeAssistantGUI()
    window.show()
    sys.exit(app.exec_())

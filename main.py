# main.py
import sys
from PyQt5.QtWidgets import QApplication
from gui import CodeAssistantGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CodeAssistantGUI()
    window.show()
    sys.exit(app.exec_())

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon


class ScriptLauncher(QMainWindow):
    def __init__(self):
        super().__init__()

        base_path = os.path.abspath(os.path.dirname(__file__))
        # Icon-Image laden
        image = os.path.join(base_path, 'content', 'app_ico.png')

        # Fenster- und Icon-Einstellungen
        self.setWindowTitle("Script Launcher")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon(image))

        # Haupt-Layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        # Liste der Skripte
        script_list = ["script1.py", "script2.py", "script3.py"]

        # Skript-Layout
        script_layout = QVBoxLayout()
        layout.addLayout(script_layout)

        # Skript-Buttons hinzufügen
        for script in script_list:
            button = QPushButton(f"Start {script}")
            button.clicked.connect(lambda _, s=script: self.start_script(s))
            script_layout.addWidget(button)

        # Status-Label
        self.status_label = QLabel("Warte auf Start...")
        layout.addWidget(self.status_label)

    def start_script(self, script):
        # Hier den Code einfügen, um das Skript zu starten
        self.status_label.setText(f"Starte {script}...")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = ScriptLauncher()
    launcher.show()
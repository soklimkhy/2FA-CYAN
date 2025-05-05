import sys
import pyotp
import pyperclip
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class TFAApp(QWidget):
    def __init__(self):
        super().__init__()
        # Set the application icon
        self.setWindowIcon(QIcon("logo.ico"))
        # Set Window Size (Resizable)
        self.resize(500, 300)

        # Apply Modern Styling with Unified Button Color
        self.setStyleSheet("""
            QWidget {
                background-color: #344a4a;
                color: #E0E0E0;
            }
            QLineEdit {
                background-color: #2D2D2D;
                border: 1px solid #03DAC5;
                border-radius: 3px;
                padding: 10px;
                color: #FFFFFF;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton {
                padding: 12px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 13px;
                background-color: #00cfbb;
                color: #00322d;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
            QFrame {
                border: 1px solid #03DAC5;
                border-radius: 3px;
                padding: 5px;
            }
            QLabel#generated-code {
                font-size: 13px;
                font-weight: bold;
            }
            QLabel#status {
                font-size: 13px;
                font-weight: bold;
            }
            QLabel#title {
                font-size: 15px;
                font-weight: bold;
                text-align: center;
            }
        """)

        # Main Layout
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Title Label
        self.title_label = QLabel("2FA-CYAN")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setObjectName("title")
        layout.addWidget(self.title_label)

        # Secret Key Input with Clear Button
        input_layout = QHBoxLayout()
        self.secret_input = QLineEdit()
        self.secret_input.setPlaceholderText("ENTER 32-CHARACTER SECRET KEY")
        self.secret_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        input_layout.addWidget(self.secret_input)

        self.clear_button = QPushButton("CLEAR")
        self.clear_button.clicked.connect(self.clear_secret)
        input_layout.addWidget(self.clear_button)

        layout.addLayout(input_layout)

        # Generate OTP Button
        self.generate_button = QPushButton("GENERATE OTP")
        self.generate_button.clicked.connect(self.generate_otp)
        layout.addWidget(self.generate_button)

        # OTP & Status Box
        otp_status_layout = QVBoxLayout()
        otp_frame = QFrame()  # Box for OTP display
        otp_frame.setLayout(otp_status_layout)

        self.otp_label = QLabel("GENERATED 2FA CODE : ")
        self.otp_label.setObjectName("generated-code")
        self.otp_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        otp_status_layout.addWidget(self.otp_label)

        self.status_label = QLabel("STATUS : ")
        self.status_label.setObjectName("status")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        otp_status_layout.addWidget(self.status_label)

        layout.addWidget(otp_frame)

        # Copy OTP Button
        self.copy_button = QPushButton("COPY OTP")
        self.copy_button.clicked.connect(self.copy_otp)
        layout.addWidget(self.copy_button)

        self.setLayout(layout)
        self.setWindowTitle("2FA-CYAN")

    def generate_otp(self):
        secret_key = self.secret_input.text().replace(" ", "").strip()
        if len(secret_key) != 32:
            self.status_label.setText("SECRET KEY MUST BE 32 CHARACTERS!")
            return
        
        totp = pyotp.TOTP(secret_key)
        otp = totp.now()

        self.otp_label.setText(f"GENERATED 2FA CODE : {otp}")
        self.status_label.setText(f"STATUS : OTP GENERATED!")

    def copy_otp(self):
        otp_text = self.otp_label.text().replace("GENERATED 2FA CODE : ", "").strip()
        if otp_text and otp_text.isdigit():
            pyperclip.copy(otp_text)
            self.status_label.setText(f"STATUS : OTP COPIED TO CLIPBOARD!")

    def clear_secret(self):
        self.secret_input.clear()

# Run the application
app = QApplication(sys.argv)
window = TFAApp()
window.show()
sys.exit(app.exec())

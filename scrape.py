import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QTextEdit,
    QMessageBox,
    QFileDialog
)


class WebScraperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Web Scraper")
        self.setGeometry(100, 100, 800, 600)
        self.setup_layout()
        self.setup_styles()

    def setup_layout(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Enter URL:"))
        self.url_entry = QLineEdit(self)
        layout.addWidget(self.url_entry)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.fetch_button = self.create_button("Fetch HTML", self.fetch_url)
        layout.addWidget(self.fetch_button)

        self.export_button = self.create_button("Export to File", self.export_to_file)
        layout.addWidget(self.export_button)

    def create_button(self, text, callback):
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        return button

    def setup_styles(self):
        self.fetch_button.setStyleSheet(self.get_button_style("green", "lightgreen"))
        self.export_button.setStyleSheet(self.get_button_style("blue", "lightblue"))
        self.url_entry.setStyleSheet("border-radius: 8px; padding: 5px;")
        self.output_text.setStyleSheet("border-radius: 8px;")

    def get_button_style(self, default_color, hover_color):
        return f"""
            QPushButton {{
                border-radius: 8px;
                padding: 10px;
                background-color: {default_color};
                color: black;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                color: white;
            }}
        """

    def fetch_url(self):
        url = self.url_entry.text().strip()
        if not url:
            self.show_error("Please enter a URL.")
            return
        
        try:
            response = requests.get(url)
            response.raise_for_status()  
            self.output_text.setPlainText(response.text)
        except requests.RequestException as e:
            self.show_error(f"Error: {e}")

    def export_to_file(self):
        text_content = self.output_text.toPlainText().strip()
        if not text_content:
            self.show_error("No content to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Text File", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            if not file_path.endswith('.txt'):
                file_path += '.txt'
            self.save_to_file(file_path, text_content)

    def save_to_file(self, file_path, content):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            QMessageBox.information(self, "Success", "File exported successfully.")
        except Exception as e:
            self.show_error(f"Failed to save file: {e}")

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    scraper = WebScraperApp()
    scraper.show()
    sys.exit(app.exec_())

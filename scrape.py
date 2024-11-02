import sys
import requests as re
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QMessageBox, QFileDialog

class WebScraperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Web Scraper")

        self.url_label = QLabel("Enter URL:")
        self.url_entry = QLineEdit(self)
        self.fetch_button = QPushButton("Fetch HTML", self)
        self.fetch_button.clicked.connect(self.fetch_url)
        
        self.export_button = QPushButton("Export to File", self)
        self.export_button.clicked.connect(self.export_to_file)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_entry)
        layout.addWidget(self.fetch_button)
        layout.addWidget(self.export_button)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def fetch_url(self):
        url = self.url_entry.text()
        if not url:
            self.show_error("Please enter a URL.")
            return
        
        try:
            response = re.get(url)
            response.raise_for_status() 
            self.output_text.setPlainText(response.text)
        except Exception as e:
            self.show_error(f"Error: {e}")

    def export_to_file(self):
        text_content = self.output_text.toPlainText()
        if not text_content.strip():
            self.show_error("No content to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Text File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            if not file_path.endswith('.txt'):
                file_path += '.txt'
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(text_content)
                QMessageBox.information(self, "Success", "File exported successfully.")
            except Exception as e:
                self.show_error(f"Failed to save file: {e}")

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scraper = WebScraperApp()
    scraper.resize(800, 600)
    scraper.show()
    sys.exit(app.exec_())

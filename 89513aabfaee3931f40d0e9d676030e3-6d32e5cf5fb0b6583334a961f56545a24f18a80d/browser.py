import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class BrowserBasilare(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MiniBrowser - Cerca Siti e Immagini")
        self.setGeometry(100, 100, 1200, 800)

        # Layout principale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Barra degli indirizzi + pulsanti
        barra = QHBoxLayout()
        self.indietro = QPushButton("←")
        self.avanti = QPushButton("→")
        self.ricarica = QPushButton("↻")
        self.cerca_input = QLineEdit()
        self.cerca_input.setPlaceholderText("Cerca su Google o inserisci URL...")
        self.vai = QPushButton("Vai")
        self.immagini = QPushButton("🖼️ Immagini")

        barra.addWidget(self.indietro)
        barra.addWidget(self.avanti)
        barra.addWidget(self.ricarica)
        barra.addWidget(self.cerca_input)
        barra.addWidget(self.vai)
        barra.addWidget(self.immagini)

        layout.addLayout(barra)

        # Web view
        self.webview = QWebEngineView()
        self.webview.load(QUrl("https://www.google.com"))
        layout.addWidget(self.webview)

        # Connessioni
        self.vai.clicked.connect(self.cerca_o_vai)
        self.immagini.clicked.connect(self.cerca_immagini)
        self.cerca_input.returnPressed.connect(self.cerca_o_vai)
        self.indietro.clicked.connect(self.webview.back)
        self.avanti.clicked.connect(self.webview.forward)
        self.ricarica.clicked.connect(self.webview.reload)
        self.webview.urlChanged.connect(self.aggiorna_url)

    def cerca_o_vai(self):
        testo = self.cerca_input.text().strip()
        if not testo:
            return

        if testo.startswith("http://") or testo.startswith("https://"):
            url = testo
        elif "." in testo and testo.split(".")[-1] in ["com", "it", "org", "net", "io"]:
            url = "https://" + testo
        else:
            # Rileva immagini nel testo
            if any(parola in testo.lower() for parola in ["immagine", "foto", "img", "picture"]):
                url = f"https://www.google.com/search?q={testo.replace(' ', '+')}&tbm=isch"
            else:
                url = f"https://www.google.com/search?q={testo.replace(' ', '+')}"

        self.webview.load(QUrl(url))

    def cerca_immagini(self):
        testo = self.cerca_input.text().strip()
        if not testo:
            return
        url = f"https://www.google.com/search?q={testo.replace(' ', '+')}&tbm=isch"
        self.webview.load(QUrl(url))

    def aggiorna_url(self, qurl):
        self.cerca_input.setText(qurl.toString())

# Avvio
if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = BrowserBasilare()
    browser.show()
    sys.exit(app.exec_())
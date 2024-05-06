from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal
from kayit_ui import Ui_Form

class KayitSayfa(QWidget):
    kayit_sinyal = pyqtSignal(list)

    def __init__(self) -> None:
        super().__init__()
        self.anasayfa = Ui_Form()
        self.anasayfa.setupUi(self)
        self.anasayfa.kayitButon.clicked.connect(self.kayitol)

    def kayitol(self):
        kullaniciadi = self.anasayfa.kullaniciadiLabel.text()
        sifre = self.anasayfa.sifreLabel.text()
        telefon = self.anasayfa.telefonLabel.text()
        soyad = self.anasayfa.soyadLine.text()
        ad = self.anasayfa.adLine.text()

        self.kayit_sinyal.emit([kullaniciadi, sifre, ad, soyad, telefon])

        yanit = QMessageBox.information(self, "Kayıt", "Kayıt işlemi tamamlandı.",QMessageBox.Ok)

        self.close()

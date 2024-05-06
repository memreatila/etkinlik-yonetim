from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtGui
from giris_ui import Ui_MainWindow
from etkinlik import Katilimci
from ana import AnaSayfa
from kayit import KayitSayfa
from veritabani import Veritabani

class arayuz(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.qtprogram = Ui_MainWindow()
        self.qtprogram.setupUi(self)
        self.qtprogram.girisButon.clicked.connect(self.girisyap)
        self.anasayfa = AnaSayfa()
        kayitsayfa = KayitSayfa()
        self.qtprogram.kayitButon.clicked.connect(lambda: kayitsayfa.show())
        kayitsayfa.kayit_sinyal.connect(self.kayitol)

    def girisyap(self):
        kullaniciadi = self.qtprogram.adLine.text()
        sifre = self.qtprogram.sifreLine.text()
        Veritabani.query('SELECT * FROM kullanicilar WHERE kullaniciadi = ? AND sifre = ?', (kullaniciadi, sifre))
        uye = Veritabani.fetchone()

        if uye is None:
            QMessageBox.warning(self, "Giris", "Kullanıcı adı veya şifre yanlış.", QMessageBox.Ok)
            return
        self.anasayfa.goster(uye)
        self.close()

    def kayitol(self,liste):
        Katilimci.kayitol(liste[0],liste[1],liste[2],liste[3],liste[4])


app = QApplication([])
pencere = arayuz()
pencere.show()
app.exec_()
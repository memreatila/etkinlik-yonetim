from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from etkinlik_ui import Ui_Form
from PyQt5 import QtCore
from veritabani import Veritabani
from etkinlik import Etkinlik, Katilimci

class EtkinlikSayfa(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.etkinlikform = Ui_Form()
        self.etkinlikform.setupUi(self)
        self.etkinlikform.etkinlikBox.currentIndexChanged.connect(self.katilimci_liste_guncelle)

    def goster(self):
        Veritabani.query('SELECT * FROM etkinlikler')
        etkinliklersql = Veritabani.fetchall()
        etkinlikler = []
        for etkinlik in etkinliklersql:
            etkinlikler.append(Etkinlik(*etkinlik))
        self.etkinlikler = etkinlikler

        tablo = self.etkinlikform.katilimciTable
        tablo.setRowCount(0)
        self.etkinlikform.etkinlikBox.clear()
        for etkinlik in etkinlikler:
            self.etkinlikform.etkinlikBox.addItem(etkinlik.ad)

        self.show()
        tablo.setColumnWidth(0, 120)
        tablo.setColumnWidth(1, 120)
        tablo.setColumnWidth(2, 80)

    def katilimci_liste_guncelle(self):
        etkinlik = self.etkinlikler[self.etkinlikform.etkinlikBox.currentIndex()]
        tablo = self.etkinlikform.katilimciTable
        katilimcilar = etkinlik.katilimcilar

        if len(katilimcilar) < 1:
            tablo.setRowCount(0)
            return
        katilimcisayisi = len(katilimcilar.split(','))
        tablo.setRowCount(katilimcisayisi)
        satir = 0


        for katilimciid in katilimcilar.split(','):
            Veritabani.query('SELECT * FROM kullanicilar WHERE id = ?', (katilimciid,))
            katilimcisql = Veritabani.fetchone()
            katilimci = Katilimci(*katilimcisql)

            ad = QTableWidgetItem(katilimci.ad)
            soyad = QTableWidgetItem(katilimci.soyad)
            telefon = QTableWidgetItem(katilimci.telefon)

            #Hepsinin yazısını ortala
            ad.setTextAlignment(QtCore.Qt.AlignCenter)
            soyad.setTextAlignment(QtCore.Qt.AlignCenter)
            telefon.setTextAlignment(QtCore.Qt.AlignCenter)

            tablo = self.etkinlikform.katilimciTable
            tablo.setItem(satir, 0, ad)
            tablo.setItem(satir, 1, soyad)
            tablo.setItem(satir, 2, telefon)
            
            satir+=1


        #tablo.resizeColumnsToContents()
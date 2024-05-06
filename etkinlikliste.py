from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from etkinlik_ui import Ui_Form
from PyQt5 import QtCore
from veritabani import Veritabani

class EtkinlikSayfa(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.etkinlikform = Ui_Form()
        self.etkinlikform.setupUi(self)
        self.etkinlikform.etkinlikBox.currentIndexChanged.connect(self.katilimci_liste_guncelle)

    def goster(self, etkinlikler):
        self.etkinlikler = etkinlikler
        tablo = self.etkinlikform.katilimciTable
        tablo.setRowCount(0)
        self.etkinlikform.etkinlikBox.clear()
        for etkinlik in etkinlikler:
            self.etkinlikform.etkinlikBox.addItem(etkinlik[1])


        self.show()
        tablo.setColumnWidth(0, 120)
        tablo.setColumnWidth(1, 120)
        tablo.setColumnWidth(2, 80)

    def katilimci_liste_guncelle(self):
        etkinlik = self.etkinlikler[self.etkinlikform.etkinlikBox.currentIndex()]
        tablo = self.etkinlikform.katilimciTable
            
        if len(etkinlik[5]) < 1:
            tablo.setRowCount(0)
            return
        katilimcisayisi = len(etkinlik[5].split(','))
        tablo.setRowCount(katilimcisayisi)
        satir = 0


        for katilimciid in etkinlik[5].split(','):
            Veritabani.query('SELECT ad, soyad, telefon FROM kullanicilar WHERE id = ?', (katilimciid,))
            katilimci = Veritabani.fetchone()
            ad = QTableWidgetItem(katilimci[0])
            soyad = QTableWidgetItem(katilimci[1])
            telefon = QTableWidgetItem(katilimci[2])

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
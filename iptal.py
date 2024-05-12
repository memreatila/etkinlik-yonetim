from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal
from iptal_ui import Ui_Form
from veritabani import Veritabani
from etkinlik import Etkinlik

class BiletIptalSayfa(QWidget):
    bilet_iptal_sinyal = pyqtSignal()
    def __init__(self, uye) -> None:
        super().__init__()
        self.biletiptalform = Ui_Form()
        self.biletiptalform.setupUi(self)
        self.biletiptalform.iptalButon.clicked.connect(self.iptal)
        self.uye = uye

    def goster(self):
        self.show()
        self.biletiptalform.etkinlikBox.clear()

        Veritabani.query('SELECT * FROM etkinlikler')
        etkinliklersql = Veritabani.fetchall()
        etkinlikler = []
        for etkinlik in etkinliklersql:
            etkinlikler.append(Etkinlik(*etkinlik))
        self.etkinlikler = etkinlikler

        for index, etkinlik in enumerate(etkinlikler):
            if str(self.uye.id) in etkinlik.katilimcilar.split(','):
                self.biletiptalform.etkinlikBox.addItem(etkinlik.ad, index)

    def iptal(self):        
        yanit = QMessageBox.warning(self, "Bilet İade", "Bilet iptal işlemini onaylıyor musunuz?", QMessageBox.Yes, QMessageBox.No)
        if yanit == QMessageBox.No:
            return
        
        etkinlikindex = self.biletiptalform.etkinlikBox.currentData()
        silinecekindex = self.biletiptalform.etkinlikBox.currentIndex()

        etkinlik = self.etkinlikler[etkinlikindex]
        etkinlik.bilet_iptal(self.uye.id)   

        self.biletiptalform.etkinlikBox.removeItem(silinecekindex)
        self.bilet_iptal_sinyal.emit()
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal
from iptal_ui import Ui_Form

class BiletIptalSayfa(QWidget):
    bilet_iptal_sinyal = pyqtSignal(int)
    def __init__(self) -> None:
        super().__init__()
        self.biletiptalform = Ui_Form()
        self.biletiptalform.setupUi(self)
        self.biletiptalform.iptalButon.clicked.connect(self.iptal)

    def goster(self, etkinlikler, katilimci):
        self.show()
        self.biletiptalform.etkinlikBox.clear()
        for index, etkinlik in enumerate(etkinlikler):
            if f'{katilimci[0]}' in etkinlik[5].split(','):
                self.biletiptalform.etkinlikBox.addItem(etkinlik[1],index)

    def iptal(self):        
        yanit = QMessageBox.warning(self, "bilet İade", "bilet iptal işlemini onaylıyor musunuz?", QMessageBox.Yes, QMessageBox.No)
        if yanit == QMessageBox.No:
            return
        
        etkinlikindex = self.biletiptalform.etkinlikBox.currentIndex()
        silinecekindex = self.biletiptalform.etkinlikBox.currentData()        
        self.biletiptalform.etkinlikBox.removeItem(etkinlikindex)
        self.bilet_iptal_sinyal.emit(silinecekindex)
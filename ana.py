from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
from ana_ui import Ui_MainWindow
from PyQt5.QtGui import QIntValidator
from etkinlik import Bilet
from PyQt5 import QtGui
from etkinlikliste import EtkinlikSayfa
from iptal import BiletIptalSayfa
from veritabani import Veritabani

class AnaSayfa(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.anasayfa = Ui_MainWindow()
        self.anasayfa.setupUi(self)
        self.index = 0
        self.anasayfa.sonrakiButon.clicked.connect(self.sonraki)
        self.anasayfa.oncekiButon.clicked.connect(self.onceki)
        Veritabani.query('SELECT * FROM etkinlikler')
        self.etkinlikler = Veritabani.fetchall()
        #self.anasayfa.biletButon.clicked.connect(self.oduncal)
        etkinliksayfa = EtkinlikSayfa()
        self.anasayfa.etkinlikListe.triggered.connect(lambda: etkinliksayfa.goster(self.etkinlikler))
        self.anasayfa.biletButon.clicked.connect(self.biletal)
        iptalsayfa = BiletIptalSayfa()
        self.anasayfa.biletIptal.triggered.connect(lambda: iptalsayfa.goster(self.etkinlikler, self.uye))
        iptalsayfa.bilet_iptal_sinyal.connect(self.biletiptal)


        
    def goster(self, uye):
        self.uye = uye
        self.show()
        self.etkinlikguncelle()

    def sonraki(self):
        self.index += 1
        if len(self.etkinlikler) == self.index:
            self.index = 0
        self.etkinlikguncelle()

    def onceki(self):
        self.index -= 1
        if self.index == -1:
            self.index = len(self.etkinlikler)-1
        self.etkinlikguncelle()

    def etkinlikguncelle(self):
        etkinlik = self.etkinlikler[self.index]
        self.anasayfa.foto.setPixmap(QtGui.QPixmap("Fotograflar/"+etkinlik[3]))
        self.anasayfa.aciklamaLabel.setText(etkinlik[4])
        self.anasayfa.etkinlikLabel.setText(etkinlik[1])
        self.anasayfa.tarihLabel.setText(etkinlik[7])
        self.anasayfa.saatLabel.setText(etkinlik[8])
        self.anasayfa.konumLabel.setText(etkinlik[9])
        self.anasayfa.turLabel.setText(etkinlik[2])
        katilimcisayisi = 0
        if (len(etkinlik[5]) > 0):
            katilimcisayisi = len(etkinlik[5].split(','))
        kontenjan = f"{katilimcisayisi}/{etkinlik[6]}"
        self.anasayfa.kontenjanLabel.setText(kontenjan)

    def biletal(self):
        etkinlik = self.etkinlikler[self.index]
        print(etkinlik[5].split(','))
        print(self.uye[0])
        katilimcisayisi = ''
        if (len(etkinlik[5]) > 0):
            katilimcisayisi = etkinlik[5].split(',')
        if len(katilimcisayisi) == etkinlik[6]:
            QMessageBox.warning(self, "Etkinlik", "Seçtiğiniz etkinlğin Kontenjanı Doludur.",QMessageBox.Ok)
            return
        if f'{self.uye[0]}' in etkinlik[5].split(','):
            QMessageBox.warning(self, "Etkinlik", "Bu etkinliğe zaten katılmışsınız.",QMessageBox.Ok)
            return

        yanit = QMessageBox.warning(self, "etkinlik", "Bu etkinliğe katılım işlemini onaylıyor musunuz?", QMessageBox.Yes, QMessageBox.No)
        if yanit == QMessageBox.No:
            return
        Bilet.bilet_al(self.index, self.uye[0])
        Veritabani.query('SELECT * FROM etkinlikler')
        self.etkinlikler = Veritabani.fetchall()
        self.etkinlikguncelle()
        QMessageBox.information(self, "etkinlik", "Etkinliğe Katıldınız", QMessageBox.Ok)

    def biletiptal(self, index):
        Bilet.bilet_iptal(index, self.uye[0])
        Veritabani.query('SELECT * FROM etkinlikler')
        self.etkinlikler = Veritabani.fetchall()
        self.etkinlikguncelle()

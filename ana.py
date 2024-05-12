from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
from ana_ui import Ui_MainWindow
from PyQt5.QtGui import QIntValidator
from etkinlik import Etkinlik, Katilimci
from PyQt5 import QtGui
from etkinlikliste import EtkinlikSayfa
from iptal import BiletIptalSayfa
from veritabani import Veritabani

class AnaSayfa(QMainWindow):
    def __init__(self, uye) -> None:
        super().__init__()
        self.uye = uye
        self.anasayfa = Ui_MainWindow()
        self.anasayfa.setupUi(self)
        self.index = 0
        self.anasayfa.sonrakiButon.clicked.connect(self.sonraki)
        self.anasayfa.oncekiButon.clicked.connect(self.onceki)
        self.liste_guncelle()
        self.etkinlikguncelle()
        #self.anasayfa.biletButon.clicked.connect(self.oduncal)
        etkinliksayfa = EtkinlikSayfa()
        self.anasayfa.etkinlikListe.triggered.connect(lambda: etkinliksayfa.goster())
        self.anasayfa.biletButon.clicked.connect(self.biletal)
        iptalsayfa = BiletIptalSayfa(uye)
        self.anasayfa.biletIptal.triggered.connect(lambda: iptalsayfa.goster())
        iptalsayfa.bilet_iptal_sinyal.connect(self.herseyi_guncelle)

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
        self.anasayfa.foto.setPixmap(QtGui.QPixmap("Fotograflar/"+etkinlik.fotograf))
        self.anasayfa.aciklamaLabel.setText(etkinlik.aciklama)
        self.anasayfa.etkinlikLabel.setText(etkinlik.ad)
        self.anasayfa.tarihLabel.setText(etkinlik.tarih)
        self.anasayfa.saatLabel.setText(etkinlik.saat)
        self.anasayfa.konumLabel.setText(etkinlik.konum)
        self.anasayfa.turLabel.setText(etkinlik.tur)

        katilimcisayisi = 0
        if (len(etkinlik.katilimcilar) > 0):
            katilimcisayisi = len(etkinlik.katilimcilar.split(','))
            
        kontenjan = f"{katilimcisayisi}/{etkinlik.kontenjan}"
        self.anasayfa.kontenjanLabel.setText(kontenjan)

    def biletal(self):
        etkinlik = self.etkinlikler[self.index]
        katilimcisayisi = ''
        katilimcilar = etkinlik.katilimcilar
        if len(katilimcilar) > 0:
            katilimcisayisi = katilimcilar.split(',')

        if len(katilimcisayisi) == etkinlik.kontenjan:
            QMessageBox.warning(self, "Etkinlik", "Seçtiğiniz etkinlğin kontenjanı doludur.",QMessageBox.Ok)
            return
        
        if str(self.uye.id) in katilimcilar.split(','):
            QMessageBox.warning(self, "Etkinlik", "Bu etkinliğe zaten katılmışsınız.",QMessageBox.Ok)
            return

        yanit = QMessageBox.warning(self, "Etkinlik", "Bu etkinliğe katılım işlemini onaylıyor musunuz?", QMessageBox.Yes, QMessageBox.No)
        if yanit == QMessageBox.No:
            return
        
        etkinlik.bilet_al(self.uye.id)
        self.herseyi_guncelle()
        QMessageBox.information(self, "Etkinlik", "Etkinliğe Katıldınız", QMessageBox.Ok)

    def herseyi_guncelle(self):
        self.liste_guncelle()
        self.etkinlikguncelle()

    def liste_guncelle(self):
        Veritabani.query('SELECT * FROM etkinlikler')
        etkinliklersql = Veritabani.fetchall()
        etkinlikler = []
        for etkinlik in etkinliklersql:
            etkinlikler.append(Etkinlik(*etkinlik))
        self.etkinlikler = etkinlikler
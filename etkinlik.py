from datetime import datetime, timedelta
from veritabani import Veritabani

class Etkinlik:
    def __init__(self, id, ad, tur, fotograf, aciklama, katilimcilar, kontenjan, tarih, saat, konum):
        self.id = id
        self.ad = ad
        self.tur = tur
        self.fotograf = fotograf
        self.aciklama = aciklama
        self.katilimcilar = katilimcilar
        self.kontenjan = kontenjan
        self.tarih = tarih
        self.saat = saat
        self.konum = konum

    def bilet_al(self, katilimci):
        Veritabani.query('SELECT katilimcilar FROM etkinlikler WHERE id = ?', (self.id,))
        katilimcilar = Veritabani.fetchone()[0]
        if (len(katilimcilar) > 0):
            katilimcilar += f',{katilimci}'
        else:
            katilimcilar = katilimci
        Veritabani.query('UPDATE etkinlikler SET katilimcilar = ? WHERE id = ?', (katilimcilar, self.id))

    def bilet_iptal(self, katilimciid):
        Veritabani.query('SELECT katilimcilar FROM etkinlikler WHERE id = ?', (self.id,))
        katilimcilar = Veritabani.fetchone()[0].split(',')
        katilimcilar.remove(f'{katilimciid}')
        if (len(katilimcilar) > 0):
            katilimcilar = ','.join(katilimcilar)
        else:
            katilimcilar = ''
        Veritabani.query('UPDATE etkinlikler SET katilimcilar = ? WHERE id = ?', (katilimcilar, self.id))

class Katilimci:
    def __init__(self, id, kullaniciadi, sifre, ad, soyad, telefon):
        self.id = id
        self.kullaniciadi = kullaniciadi
        self.sifre = sifre
        self.ad = ad
        self.soyad = soyad
        self.telefon = telefon

    @staticmethod
    def kayitol(kullaniciadi, sifre, ad, soyad, telefon):
        Veritabani.query('INSERT INTO kullanicilar (kullaniciadi, sifre, ad, soyad, telefon) VALUES(?, ?, ?, ?, ?)', (kullaniciadi, sifre, ad, soyad, telefon))
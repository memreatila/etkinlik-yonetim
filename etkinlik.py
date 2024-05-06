from datetime import datetime, timedelta
from veritabani import Veritabani

class Bilet:
    @staticmethod
    def bilet_al(etkinlikindex, katilimci):
        Veritabani.query('SELECT katilimcilar FROM etkinlikler WHERE id = ?', (etkinlikindex + 1,))
        katilimcilar = Veritabani.fetchone()[0]
        if (len(katilimcilar) > 0):
            katilimcilar += f',{katilimci}'
        else:
            katilimcilar = katilimci
        Veritabani.query('UPDATE etkinlikler SET katilimcilar = ? WHERE id = ?', (katilimcilar, etkinlikindex + 1))

    @staticmethod
    def bilet_iptal(etkinlikindex, katilimciid):
        Veritabani.query('SELECT katilimcilar FROM etkinlikler WHERE id = ?', (etkinlikindex + 1,))
        katilimcilar = Veritabani.fetchone()[0].split(',')
        katilimcilar.remove(f'{katilimciid}')
        if (len(katilimcilar) > 0):
            katilimcilar = ','.join(katilimcilar)
        else:
            katilimcilar = ''
        Veritabani.query('UPDATE etkinlikler SET katilimcilar = ? WHERE id = ?', (katilimcilar, etkinlikindex + 1))



        
class Katilimci:
    @staticmethod
    def kayitol(kullaniciadi, sifre, ad, soyad, telefon):
        Veritabani.query('INSERT INTO kullanicilar (kullaniciadi, sifre, ad, soyad, telefon) VALUES(?, ?, ?, ?, ?)', (kullaniciadi, sifre, ad, soyad, telefon))

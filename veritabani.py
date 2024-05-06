import sqlite3

class veritabani:
    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='etkinlikler'")
        tablo_var_mi = self.cursor.fetchone()

        if not tablo_var_mi:  # Tablo yok
            self.cursor.execute('CREATE TABLE IF NOT EXISTS etkinlikler (ID INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT, tur TEXT, fotograf TEXT, aciklama TEXT, katilimcilar TEXT, kontenjan INTEGER, tarih TEXT, saat TEXT, konum TEXT)')
            self.cursor.execute('CREATE TABLE IF NOT EXISTS kullanicilar (ID INTEGER PRIMARY KEY AUTOINCREMENT, kullaniciadi TEXT, sifre TEXT, ad TEXT, soyad TEXT, telefon TEXT)')

            etkinlikler_tuple = [
                ("Kültür Bahar Şenliği", "Müzik", "baharsenligi.jpg", "Kültür Üniversitesi'nin bahar şenliği, her yıl öğrencilerin heyecanla beklediği bir etkinlik. Baharın coşkusunu ve enerjisini yansıtan bu şenlik, renkli etkinlikleriyle kampüsü hareketlendiriyor. Müzik, dans, tiyatro gibi birçok sanat dalından örneklerin sergilendiği şenlikte, öğrenciler hem eğlenip stres atıyor hem de bir araya gelerek sosyal bağlarını güçlendiriyor.", "", 100, "09.05.2024", "19:00", "Ataköy Kampüsü"),
                ("Duman Konseri", "Müzik", "duman.jpg", "Duman konseri, müzikseverler için uzun zamandır heyecanla beklenen bir etkinlik olacak. Konser mekanı, coşkulu kalabalıkla dolup taşacak ve sahne, Duman'ın efsane şarkılarını seslendirmek için hazır olacak. Grup üyeleri sahneye çıktığında, izleyicilerin coşkusu doruk noktaya ulaşacak. Duman'ın hit şarkıları, seyircileri adeta büyüleyecek ve herkesin birlikte söylediği unutulmaz bir atmosfer oluşturacak.", "", 200, "10.05.2024", "18:00", "Kuruçeşme"),
                ("İstanbul Gençlik Atölyeleri", "Eğitim", "genclik.png", "YEKDER Gençlik Eğitimleri bünyesinde 2 yıldır düzenlenmekte olan Gençlik Atölyeleri yeni dönemde iki ayrı atölye ile ilgilerle buluşacak. İstanbul ve El Becerileri özelinde gerçekleştirilecek olan iki atölyede gençlerin günlük yoğunluklarından sıyrılarak ders formatından uzak şekilde bir araya gelmesi hedeflendi.Bu kapsamda İstanbul Atölyesi’nde İstanbul’un kadim tarihi ve kültürel birikimi birbirinden değerli uzman hocalarımızın mihmandarlığında işlenecek.", "", 50, "14.05.2024", "18:00", "Yekder Genel Merkezi"),
                ("Tarkan Konseri", "Müzik", "tarkan.jpg", "Tarkan konseri, müzik tutkunlarını coşkuyla dolacak. Konser alanı, hayranlarını ağırlamak için hazır hale gelecek ve sahne, Tarkan'ın efsanevi performansını sergilemek için aydınlatılacak. Tarkan sahneye adım attığında, izleyicilerin enerjisi tavan yapacak. Tarkan'ın unutulmaz şarkıları, seyircileri dans ettirecek ve birlikte söylenen melodilerle dolu bir atmosfer oluşturacak. ", "", 300, "01.07.2024", "20:00", "Harbiye Açık Hava Tiyatrosu"),
                ("Teknofest", "Bilim", "teknofest.jpg", "TEKNOFEST, Türkiye’de milli teknolojinin geliştirilmesi konusunda kritik rol oynayan birçok kuruluşun paydaşlığıyla düzenlenen Türkiye'nin ilk ve tek havacılık, uzay ve teknoloji festivalidir.İlki 2018'de gerçekleştirilen TEKNOFEST Havacılık, Uzay ve Teknoloji Festivali; teknoloji yarışmaları, hava gösterileri, konserler, çeşitli konularda gerçekleştirilen söyleşi ve etkinlikler gibi birçok faaliyete ev sahipliği yaparak toplumda teknolojiye olan ilgiyi artırmayı hedeflemektedir.", "", 1000, "27.04.2024", "13:00", "Atatürk Havalimanı")
            ]

            self.cursor.executemany('INSERT INTO etkinlikler (ad, tur, fotograf, aciklama, katilimcilar, kontenjan, tarih, saat, konum) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', etkinlikler_tuple)
            self.cursor.execute("INSERT INTO kullanicilar (kullaniciadi, sifre, ad, soyad, telefon) VALUES ('enes', '123', 'Enes', 'Biçici', '5323184256')")
            self.connection.commit()

    def query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        return self.cursor
    
    def fetchall(self):
        return self.cursor.fetchall()
    
    def fetchone(self):
        return self.cursor.fetchone()
    
Veritabani = veritabani('sql.db')

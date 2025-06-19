Brevo mail gönderimi için kullanıcı dostu bir GUI 
Modern ve kullanıcı dostu bir GUI uygulaması
![image](https://github.com/user-attachments/assets/8a1fd1dd-ef4b-4997-b3f8-ff0be9559272)

İşte özellikleri:

 🎯 Özellikler

 ✨ Temel Fonksiyonlar
 Tekil Mail: Bir kişiye özel mail gönderimi
 Toplu Mail: CSV dosyasından toplu mail gönderimi
 HTML & Metin: Her iki format da destekleniyor
 Template Sistemi: {{name}} ile kişiselleştirme

 📊 Gelişmiş Özellikler
 CSV Desteği: Excel'den export edilen CSV dosyalarını okur
 Template Kaydetme: Mail şablonlarını kaydetme/yükleme
 Durum Takibi: Gerçek zamanlı durum göstergesi
 Hata Yönetimi: Detaylı hata mesajları
 Async Gönderim: Gönderim sırasında arayüz donmaz

 🛡️ Güvenlik
 API anahtarı gizli gösterilir
 Form validasyonu
 Hata yakalama

 📝 Kullanım

 Kurulum
bash
pip install tkinter requests


 CSV Formatı (Toplu Mail İçin)
csv
email,name
ahmet@example.com,Ahmet Yılmaz
fatma@example.com,Fatma Özkan
mehmet@example.com,Mehmet Demir


 Template Kullanımı
Mail içeriğinde `{{name}}` yazarsanız, otomatik olarak alıcının ismiyle değiştirilir.

 🚀 Nasıl Çalıştırılır

1. Kodu çalıştırın
2. API anahtarınızı girin
3. Gönderen bilgilerini doldurun
4. Mail türünü seçin (Tekil/Toplu)
5. İçeriği hazırlayın
6. "Mail Gönder" butonuna basın

 💡 İpuçları

 Template Kaydetme: Sık kullandığınız mail şablonlarını kaydedin
 CSV Hazırlama: Excel'de hazırlayıp "CSV" olarak kaydedin
 Kişiselleştirme: {{name}} ile kişisel mesajlar oluşturun
 Test Etme: Önce kendinize test maili gönderin

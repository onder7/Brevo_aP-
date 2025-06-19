import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import requests
import json
import csv
from threading import Thread
import os

class BrevoMailGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Brevo Mail Gönderici")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Ana frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid ağırlık ayarları
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Başlık
        title_label = ttk.Label(main_frame, text="📧 Brevo Mail Gönderici", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # API Ayarları Bölümü
        api_frame = ttk.LabelFrame(main_frame, text="API Ayarları", padding="10")
        api_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        api_frame.columnconfigure(1, weight=1)
        
        ttk.Label(api_frame, text="API Anahtarı:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.api_key_entry = ttk.Entry(api_frame, show="*", width=50)
        self.api_key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Gönderen Bilgileri
        sender_frame = ttk.LabelFrame(main_frame, text="Gönderen Bilgileri", padding="10")
        sender_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        sender_frame.columnconfigure(1, weight=1)
        
        ttk.Label(sender_frame, text="Gönderen Email:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.sender_email_entry = ttk.Entry(sender_frame, width=40)
        self.sender_email_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(sender_frame, text="Gönderen İsim:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.sender_name_entry = ttk.Entry(sender_frame, width=40)
        self.sender_name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))
        
        # Mail Tipi Seçimi
        type_frame = ttk.LabelFrame(main_frame, text="Mail Türü", padding="10")
        type_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.mail_type = tk.StringVar(value="tekil")
        ttk.Radiobutton(type_frame, text="Tekil Mail", variable=self.mail_type, 
                       value="tekil", command=self.toggle_mail_type).grid(row=0, column=0, padx=(0, 20))
        ttk.Radiobutton(type_frame, text="Toplu Mail", variable=self.mail_type, 
                       value="toplu", command=self.toggle_mail_type).grid(row=0, column=1)
        
        # Alıcı Bilgileri
        self.recipient_frame = ttk.LabelFrame(main_frame, text="Alıcı Bilgileri", padding="10")
        self.recipient_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.recipient_frame.columnconfigure(1, weight=1)
        
        # Tekil mail için alanlar
        self.recipient_email_label = ttk.Label(self.recipient_frame, text="Alıcı Email:")
        self.recipient_email_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.recipient_email_entry = ttk.Entry(self.recipient_frame, width=40)
        self.recipient_email_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.recipient_name_label = ttk.Label(self.recipient_frame, text="Alıcı İsim:")
        self.recipient_name_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.recipient_name_entry = ttk.Entry(self.recipient_frame, width=40)
        self.recipient_name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))
        
        # Toplu mail için alanlar
        self.csv_frame = ttk.Frame(self.recipient_frame)
        self.csv_button = ttk.Button(self.csv_frame, text="CSV Dosyası Seç", command=self.select_csv)
        self.csv_label = ttk.Label(self.csv_frame, text="CSV dosyası seçilmedi", foreground="gray")
        
        # Mail İçeriği
        content_frame = ttk.LabelFrame(main_frame, text="Mail İçeriği", padding="10")
        content_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(1, weight=1)
        content_frame.rowconfigure(3, weight=1)
        
        ttk.Label(content_frame, text="Konu:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.subject_entry = ttk.Entry(content_frame, width=60)
        self.subject_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(content_frame, text="HTML İçerik:").grid(row=1, column=0, sticky=(tk.W, tk.N), padx=(0, 10))
        self.html_text = scrolledtext.ScrolledText(content_frame, height=8, width=60)
        self.html_text.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        ttk.Label(content_frame, text="Metin İçerik:").grid(row=2, column=0, sticky=(tk.W, tk.N), padx=(0, 10))
        self.text_content = scrolledtext.ScrolledText(content_frame, height=6, width=60)
        self.text_content.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Butonlar
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="🔧 API Test", command=self.test_api).pack(side=tk.LEFT, padx=(0, 10))
        self.send_button = ttk.Button(button_frame, text="📨 Mail Gönder", 
                                     command=self.send_mail, style='Accent.TButton')
        self.send_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="🗑️ Temizle", command=self.clear_form).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="💾 Kaydet", command=self.save_template).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="📂 Yükle", command=self.load_template).pack(side=tk.LEFT)
        
        # Durum çubuğu
        self.status_var = tk.StringVar(value="Hazır")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # İlk durumu ayarla
        self.toggle_mail_type()
        self.csv_file_path = None
        
        # Örnek veriler ekle
        self.load_sample_data()
    
    def toggle_mail_type(self):
        if self.mail_type.get() == "tekil":
            # Tekil mail arayüzünü göster
            self.recipient_email_label.grid()
            self.recipient_email_entry.grid()
            self.recipient_name_label.grid()
            self.recipient_name_entry.grid()
            self.csv_frame.grid_remove()
        else:
            # Toplu mail arayüzünü göster
            self.recipient_email_label.grid_remove()
            self.recipient_email_entry.grid_remove()
            self.recipient_name_label.grid_remove()
            self.recipient_name_entry.grid_remove()
            self.csv_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
            self.csv_button.pack(side=tk.LEFT, padx=(0, 10))
            self.csv_label.pack(side=tk.LEFT)
    
    def select_csv(self):
        file_path = filedialog.askopenfilename(
            title="CSV Dosyası Seç",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.csv_file_path = file_path
            filename = os.path.basename(file_path)
            self.csv_label.config(text=f"Seçilen dosya: {filename}", foreground="green")
    
    def load_sample_data(self):
        """Örnek veriler yükle"""
        self.api_key_entry.insert(0, "xkeysib-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        self.sender_email_entry.insert(0, "gonderen@sirketim.com")
        self.sender_name_entry.insert(0, "Şirket Adı")
        self.recipient_email_entry.insert(0, "alici@example.com")
        self.recipient_name_entry.insert(0, "Değerli Müşterimiz")
        self.subject_entry.insert(0, "Test Maili")
        
        html_sample = """<html>
<body>
    <h2>Merhaba {{name}}!</h2>
    <p>Bu bir <strong>test maili</strong>dir.</p>
    <p>Brevo API ile Python GUI kullanarak gönderilmiştir.</p>
    <br>
    <p>İyi günler dileriz!</p>
</body>
</html>"""
        self.html_text.insert(tk.END, html_sample)
        
        text_sample = """Merhaba {{name}}!

Bu bir test mailidir.
Brevo API ile Python GUI kullanarak gönderilmiştir.

İyi günler dileriz!"""
        self.text_content.insert(tk.END, text_sample)
    
    def test_api(self):
        """API bağlantısını test et"""
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showerror("Hata", "API anahtarı girin!")
            return
        
        headers = {
            'accept': 'application/json',
            'api-key': api_key
        }
        
        try:
            self.status_var.set("API test ediliyor...")
            
            # Hesap bilgilerini kontrol et
            response = requests.get("https://api.brevo.com/v3/account", headers=headers)
            
            if response.status_code == 200:
                account_info = response.json()
                company_name = account_info.get('companyName', 'Bilinmeyen')
                
                # SMS kredilerini ve email limitlerini kontrol et
                plan_info = account_info.get('plan', [])
                email_credits = "Sınırsız"
                for plan in plan_info:
                    if plan.get('type') == 'payAsYouGo':
                        credits_info = plan.get('credits', {})
                        email_credits = credits_info.get('emails', 'Bilinmeyen')
                
                success_msg = f"✅ API bağlantısı başarılı!\n"
                success_msg += f"Hesap: {company_name}\n"
                success_msg += f"Email kredisi: {email_credits}"
                
                messagebox.showinfo("Başarılı", success_msg)
                self.status_var.set("API test başarılı")
                
            elif response.status_code == 401:
                messagebox.showerror("Hata", "❌ API anahtarı geçersiz!\n\nÇözüm:\n- Brevo'dan yeni API anahtarı alın\n- API anahtarının doğru kopyalandığından emin olun")
                self.status_var.set("API anahtarı geçersiz")
                
            elif response.status_code == 403:
                messagebox.showerror("Hata", "❌ Erişim izni yok! (403)\n\nÇözüm:\n1. Gönderen email adresinizi Brevo'da doğrulayın\n2. Hesap durumunuzu kontrol edin\n3. Yeni API anahtarı oluşturun\n4. Günlük limitinizi kontrol edin")
                self.status_var.set("Erişim izni yok")
                
            else:
                messagebox.showerror("Hata", f"❌ API hatası: {response.status_code}\n{response.text}")
                self.status_var.set("API hatası")
                
        except Exception as api_error:
            error_msg = f"❌ Bağlantı hatası: {str(api_error)}"
            messagebox.showerror("Hata", error_msg)
            self.status_var.set("Bağlantı hatası")

    def send_mail(self):
        """Mail gönderme işlemi"""
        # Form validasyonu
        if not self.validate_form():
            return
        
        # Gönderme işlemini ayrı thread'de çalıştır
        self.send_button.config(state='disabled', text='Gönderiliyor...')
        self.status_var.set("Mail gönderiliyor...")
        
        thread = Thread(target=self.send_mail_thread)
        thread.daemon = True
        thread.start()
    
    def send_mail_thread(self):
        """Mail gönderme thread'i"""
        try:
            api_key = self.api_key_entry.get()
            sender_email = self.sender_email_entry.get()
            sender_name = self.sender_name_entry.get()
            subject = self.subject_entry.get()
            html_content = self.html_text.get(1.0, tk.END).strip()
            text_content = self.text_content.get(1.0, tk.END).strip()
            
            headers = {
                'accept': 'application/json',
                'api-key': api_key,
                'content-type': 'application/json'
            }
            
            if self.mail_type.get() == "tekil":
                # Tekil mail gönder
                recipient_email = self.recipient_email_entry.get()
                recipient_name = self.recipient_name_entry.get()
                
                # Template değişkenlerini değiştir
                html_content = html_content.replace("{{name}}", recipient_name)
                text_content = text_content.replace("{{name}}", recipient_name)
                
                mail_data = {
                    "sender": {"name": sender_name, "email": sender_email},
                    "to": [{"email": recipient_email, "name": recipient_name}],
                    "subject": subject,
                    "htmlContent": html_content,
                    "textContent": text_content
                }
                
                response = requests.post(
                    "https://api.brevo.com/v3/smtp/email",
                    headers=headers,
                    data=json.dumps(mail_data)
                )
                
                if response.status_code == 201:
                    self.root.after(0, lambda: self.show_success("Mail başarıyla gönderildi!"))
                elif response.status_code == 401:
                    self.root.after(0, lambda: self.show_error("Hata: API anahtarı geçersiz! Lütfen doğru API anahtarını girin."))
                elif response.status_code == 400:
                    self.root.after(0, lambda: self.show_error("Hata: Gönderen email adresi doğrulanmamış! Brevo'da email adresinizi doğrulayın."))
                elif response.status_code == 403:
                    self.root.after(0, lambda: self.show_error("Hata: Erişim izni yok!\n\nÇözüm:\n1. Gönderen email'i Brevo'da doğrulayın\n2. Hesap durumunuzu kontrol edin\n3. Günlük limitinizi kontrol edin"))
                else:
                    error_msg = f"Hata {response.status_code}: {response.text}"
                    self.root.after(0, lambda msg=error_msg: self.show_error(msg))
            
            else:
                # Toplu mail gönder
                if not self.csv_file_path:
                    self.root.after(0, lambda: self.show_error("CSV dosyası seçmediniz!"))
                    return
                
                # CSV dosyasını oku
                recipients = []
                try:
                    with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                        csv_reader = csv.DictReader(file)
                        for row in csv_reader:
                            if 'email' in row and 'name' in row:
                                recipients.append({
                                    "email": row['email'],
                                    "name": row['name']
                                })
                except Exception as csv_error:
                    error_msg = f"CSV okuma hatası: {str(csv_error)}"
                    self.root.after(0, lambda msg=error_msg: self.show_error(msg))
                    return
                
                if not recipients:
                    self.root.after(0, lambda: self.show_error("CSV dosyasında geçerli alıcı bulunamadı!"))
                    return
                
                # Her alıcı için ayrı mail gönder (kişiselleştirme için)
                success_count = 0
                for recipient in recipients:
                    personal_html = html_content.replace("{{name}}", recipient['name'])
                    personal_text = text_content.replace("{{name}}", recipient['name'])
                    
                    mail_data = {
                        "sender": {"name": sender_name, "email": sender_email},
                        "to": [recipient],
                        "subject": subject,
                        "htmlContent": personal_html,
                        "textContent": personal_text
                    }
                    
                    response = requests.post(
                        "https://api.brevo.com/v3/smtp/email",
                        headers=headers,
                        data=json.dumps(mail_data)
                    )
                    
                    if response.status_code == 201:
                        success_count += 1
                    elif response.status_code == 401:
                        self.root.after(0, lambda: self.show_error("API anahtarı geçersiz!"))
                        break
                    elif response.status_code == 400:
                        continue  # Bu alıcıyı atla, diğerlerini göndermeye devam et
                
                success_msg = f"{success_count}/{len(recipients)} mail başarıyla gönderildi!"
                self.root.after(0, lambda msg=success_msg: self.show_success(msg))
        
        except Exception as e:
            error_msg = f"Beklenmeyen hata: {str(e)}"
            self.root.after(0, lambda msg=error_msg: self.show_error(msg))
        
        finally:
            self.root.after(0, self.reset_send_button)
    
    def validate_form(self):
        """Form validasyonu"""
        if not self.api_key_entry.get().strip():
            messagebox.showerror("Hata", "API anahtarı gerekli!")
            return False
        
        if not self.sender_email_entry.get().strip():
            messagebox.showerror("Hata", "Gönderen email gerekli!")
            return False
        
        if not self.subject_entry.get().strip():
            messagebox.showerror("Hata", "Mail konusu gerekli!")
            return False
        
        if self.mail_type.get() == "tekil":
            if not self.recipient_email_entry.get().strip():
                messagebox.showerror("Hata", "Alıcı email gerekli!")
                return False
        else:
            if not self.csv_file_path:
                messagebox.showerror("Hata", "Toplu mail için CSV dosyası seçmelisiniz!")
                return False
        
        return True
    
    def show_success(self, message):
        """Başarı mesajı göster"""
        messagebox.showinfo("Başarılı", message)
        self.status_var.set("İşlem tamamlandı")
    
    def show_error(self, message):
        """Hata mesajı göster"""
        messagebox.showerror("Hata", message)
        self.status_var.set("Hata oluştu")
    
    def reset_send_button(self):
        """Gönder butonunu sıfırla"""
        self.send_button.config(state='normal', text='📨 Mail Gönder')
    
    def clear_form(self):
        """Formu temizle"""
        self.api_key_entry.delete(0, tk.END)
        self.sender_email_entry.delete(0, tk.END)
        self.sender_name_entry.delete(0, tk.END)
        self.recipient_email_entry.delete(0, tk.END)
        self.recipient_name_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.html_text.delete(1.0, tk.END)
        self.text_content.delete(1.0, tk.END)
        self.csv_file_path = None
        self.csv_label.config(text="CSV dosyası seçilmedi", foreground="gray")
        self.status_var.set("Form temizlendi")
    
    def save_template(self):
        """Template kaydet"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            template_data = {
                "sender_email": self.sender_email_entry.get(),
                "sender_name": self.sender_name_entry.get(),
                "subject": self.subject_entry.get(),
                "html_content": self.html_text.get(1.0, tk.END),
                "text_content": self.text_content.get(1.0, tk.END)
            }
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Başarılı", "Template kaydedildi!")
    
    def load_template(self):
        """Template yükle"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                
                self.sender_email_entry.delete(0, tk.END)
                self.sender_email_entry.insert(0, template_data.get("sender_email", ""))
                
                self.sender_name_entry.delete(0, tk.END)
                self.sender_name_entry.insert(0, template_data.get("sender_name", ""))
                
                self.subject_entry.delete(0, tk.END)
                self.subject_entry.insert(0, template_data.get("subject", ""))
                
                self.html_text.delete(1.0, tk.END)
                self.html_text.insert(1.0, template_data.get("html_content", ""))
                
                self.text_content.delete(1.0, tk.END)
                self.text_content.insert(1.0, template_data.get("text_content", ""))
                
                messagebox.showinfo("Başarılı", "Template yüklendi!")
            except Exception as load_error:
                error_msg = f"Template yüklenemedi: {str(load_error)}"
                messagebox.showerror("Hata", error_msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = BrevoMailGUI(root)
    root.mainloop()

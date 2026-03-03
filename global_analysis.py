import ollama
import sqlite3
import datetime
import os

def analyze_all_posts():
    # 1. Veritabanı Bağlantısı
    try:
        conn = sqlite3.connect('osint_data_v2.db')
        cursor = conn.cursor()
        
        # Daha fazla detay çekiyoruz: summary ve content eklendi
        cursor.execute("SELECT title, subreddit, published_date, author, summary, content FROM reddit_posts ORDER BY id DESC")
        posts = cursor.fetchall()
        
        if not posts:
            print("Veritabanında yeterli veri bulunamadı. Lütfen önce getDataFromReddit.py çalıştırın.")
            return

        print(f"{len(posts)} adet veri çekildi, analiz başlıyor...")

        # 2. Veriyi Hazırlama
        # Format: [Tarih] [Subreddit] Başlık (Yazar: YazarAdı) | Özet/İçerik Başlangıcı
        formatted_data_list = []
        for post in posts:
            title = post[0]
            subreddit = post[1]
            date = post[2]
            author = post[3]
            summary = post[4]
            content = post[5]

            # İçerik varsa onu, yoksa özeti kullan, çok uzunsa kısalt (Token limiti için)
            text_body = content if content and len(content) > 10 else summary
            
            # HTML etiketlerini temizlemek iyi olurdu ama şimdilik doğrudan kısaltarak alıyoruz
            # İlk 300 karakteri alarak bağlamı zenginleştiriyoruz
            short_body = text_body[:300].replace("\n", " ") + "..." if text_body else ""
            
            formatted_data_list.append(f"- [{date}] [{subreddit}] {title} (Yazar: {author}) | Detay: {short_body}")

        formatted_data = "\n".join(formatted_data_list)

        # 3. Prompt Hazırlama
        system_prompt = "Sen uzman bir istihbarat ve veri analistisin. Verilen veri setindeki trendleri, ilişkileri ve gizli bağlantıları ortaya çıkarmakta uzmansın."
        
        user_prompt = f"""Aşağıda çeşitli savunma, jeopolitik ve askeri Reddit kaynaklarından toplanmış son haber başlıkları bulunmaktadır.
        
        Lütfen bu verileri bütüncül olarak incele ve şu başlıkları içeren detaylı bir rapor oluştur:
        
        1. **Ana Gündem Maddeleri:** Şu an en çok tartışılan 3-5 ana konu nedir?
        2. **Konular Arası İlişkiler:** Farklı subredditler (örneğin TankPorn ve UkrainianConflict) arasında konu veya teçhizat bazlı kesişmeler var mı?
        3. **Trend Analizi:** Haberlerin yoğunlaştığı belirli coğrafyalar veya teknolojik sistemler neler?
        4. **Çıkarım:** Bu veriler küresel gündem hakkında ne söylüyor?

        Veri Seti:
        {formatted_data}
        """

        # 4. Ollama (Gemma-3) ile Analiz
        response = ollama.chat(model='gemma3:4b', messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt},
        ])
        report_content = response['message']['content']
        
        reports_dir = "./reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
            
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(reports_dir, f"report_{timestamp}.md")
        
        # Raporu .md dosyasına kaydet
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# KÜRESEL İLİŞKİ VE TREND ANALİZİ RAPORU\n")
            f.write(f"**Oluşturulma Tarihi:** {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
            f.write(report_content)

        # print("\n" + "="*40)
        # print(f"Rapor başarıyla kaydedildi: {filename}")
        # print("="*40 + "\n")
        # print(response['message']['content'])

    except sqlite3.Error as e:
        print(f"Veritabanı hatası: {e}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    analyze_all_posts()

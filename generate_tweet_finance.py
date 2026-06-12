import ollama
import sqlite3
import datetime
import os

# Veritabanından finans/osint verilerini çekip Twitter flood'u hazırlayan fonksiyon
def generate_tweet_thread(tweet_count=5):
    try:
        conn = sqlite3.connect('osint_finance_data.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT title, subreddit, published_date, summary, content FROM reddit_posts ORDER BY id DESC")
        posts = cursor.fetchall()
        
        if not posts:
            print("Veritabanında yeterli veri bulunamadı.")
            return

        print(f"{len(posts)} adet veri üzerinden tweet analizi başlıyor...")

        # 2. Veriyi Hazırlama (Mevcut mantığın aynısı)
        formatted_data_list = []
        for post in posts:
            title, subreddit, date, summary, content = post[0], post[1], post[2], post[3], post[4]
            text_body = content if content and len(content) > 10 else summary
            short_body = text_body[:250].replace("\n", " ") + "..." if text_body else ""
            formatted_data_list.append(f"- [{subreddit}] {title} | Detay: {short_body}")

        formatted_data = "\n".join(formatted_data_list)

        # 3. Tweet Odaklı Prompt Tasarımı
        system_prompt = (
            "Sen sosyal medyayı ve finans/savunma gündemini çok iyi yöneten, "
            "karmaşık verileri net, vurucu ve etkileşim alacak tweetlere dönüştüren "
            "profesyonel bir içerik üreticisi ve analistsin."
        )
        
        user_prompt = f"""Aşağıdaki ham verileri incele ve bu verilerden yola çıkarak finans/jeopolitik gündemi özetleyen, 
birbiriyle bağlantılı tam {tweet_count} adet tweetten oluşan bir Twitter (X) flood'u (zinciri) hazırla.

Kurallar:
1. Toplamda kesinlikle tam {tweet_count} adet tweet olmalı.
2. Tweetler [1/{tweet_count}], [2/{tweet_count}] şeklinde numaralandırılmalı.
3. Her tweet finansal veya jeopolitik bir trendi, bölge/konu bazlı bir analizi net bir dille anlatmalı.
4. Karakter sınırına (maksimum 280 karakter) uygun, okunması kolay, emoji içeren ve dikkat çekici bir üslup kullanılmalı.
5. Sadece tweet metinlerini döndür, başka hiçbir açıklama veya giriş metni yazma.

Veri Seti:
{formatted_data}
"""

        # 4. Ollama (Gemma-3) Çağrısı
        response = ollama.chat(model='gemma3:4b', messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt},
        ])
        tweet_content = response['message']['content']
        
        # 5. Tweetleri Dosyaya Kaydetme
        tweets_dir = "./tweets"
        if not os.path.exists(tweets_dir):
            os.makedirs(tweets_dir)
            
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(tweets_dir, f"tweets_{timestamp}.md")
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# SOSYAL MEDYA PAYLAŞIM TASLAĞI (TWEET FLOOD)\n")
            f.write(f"**Oluşturulma Tarihi:** {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
            f.write(tweet_content)

        print("\n" + "="*40)
        print(f"Tweet taslağı başarıyla kaydedildi: {filename}")
        print("="*40 + "\n")
        print(tweet_content)

    except sqlite3.Error as e:
        print(f"Veritabanı hatası: {e}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # İster raporlama fonksiyonunu çalıştır, ister tweet fonksiyonunu
    # ya da her ikisini birden sırayla çalıştırabilirsin.
    
    # 5 adet tweet üretmesini istiyoruz (Miktarı buradan değiştirebilirsin)
    generate_tweet_thread(tweet_count=5)
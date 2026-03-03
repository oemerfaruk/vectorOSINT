# VectorOSINT

VectorOSINT, stratejik savunma, askeri ve jeopolitik Reddit topluluklarından (subreddit) RSS beslemeleri aracılığıyla sürekli veri toplayan, bunları yerel bir veritabanında saklayan ve Google'ın gelişmiş `gemma3` modelini kullanarak periyodik analiz raporları (Markdown ve PDF) üreten bir OSINT (Açık Kaynak İstihbarat) aracıdır.

## Özellikler

- **Otomatik Veri Toplama:** 20'den fazla hedefli subreddit'ten (örn. Intelligence, Geopolitics, CombatFootage) sürekli veri akışı sağlar.
- **Veri Zenginleştirme:** Başlıkların yanı sıra gönderi özetleri, içerik detayları, yazar bilgileri ve yayın tarihlerini saklar (`osint_data_v2.db`).
- **Yapay Zeka Destekli Analiz:** Yerel LLM (Ollama - Gemma 3) kullanarak küresel trendleri, konular arası ilişkileri ve askeri hareketliliği analiz eder.
- **Çoklu Raporlama Formatı:** Analiz sonuçlarını hem okunabilir **Markdown (`.md`)** hem de **PDF (`.pdf`)** formatında `reports/` klasörüne kaydeder.
- **Otomasyon:** `auto_reporter.py` sayesinde belirli aralıklarla (varsayılan: 5 dakika) otomatik analiz ve raporlama yapar.

## Gereksinimler

Bu projeyi tam kapasiteyle çalıştırmak için aşağıdaki yazılımlara ihtiyacınız vardır:

### Sistem Gereksinimleri
- **Python 3.8+**
- **[Ollama](https://ollama.com/):** Yerel LLM çalıştırmak için gereklidir.
- **wkhtmltopdf:** Raporları PDF'e dönüştürmek için gereklidir.
  - **macOS:** `brew install wkhtmltopdf`
  - **Linux (Debian/Ubuntu):** `sudo apt-get install wkhtmltopdf`
  - **Windows:** [Resmi sitesinden](https://wkhtmltopdf.org/downloads.html) indirip kurabilirsiniz.

### Python Kütüphaneleri
Gerekli kütüphaneleri yüklemek için:

```bash
pip install requests feedparser sqlalchemy ollama markdown pdfkit
```

### Ollama Model Kurulumu
Proje analiz için `gemma3:4b` modelini kullanmaktadır. Ollama'yı kurduktan sonra terminalden modeli indirin:

```bash
ollama pull gemma3:4b
```

## Kurulum ve Kullanım

1. **Projeyi Klonlayın:**
   ```bash
   git clone https://github.com/kullaniciadi/vectorOSINT.git
   cd vectorOSINT
   ```

2. **Veri Toplamayı Başlatın (Terminal 1):**
   `getDataFromReddit.py` dosyası sürekli çalışan bir döngüde verileri toplar ve veritabanına kaydeder. Bu script arka planda sürekli açık kalmalıdır.
   
   ```bash
   python getDataFromReddit.py
   ```

3. **Otomatik Raporlamayı Başlatın (Terminal 2):**
   Veriler biriktikçe otomatik analiz yapıp PDF rapor üretmek için bu scripti çalıştırın. Varsayılan olarak her 120 dakikada bir rapor üretir.
   
   ```bash
   python auto_reporter.py
   ```
   
   *Alternatif (Manuel):* Tek seferlik rapor almak isterseniz:
   ```bash
   python global_analysis.py
   ```

4. **Raporları İnceleyin:**
   Oluşturulan tüm raporlar `reports/` klasörü altında tarih etiketli olarak (`report_YYYY-MM-DD_HH-MM-SS.pdf`) saklanır.

## Hedeflenen Kaynaklar (Örnekler)

* **İstihbarat & Analiz:** r/Intelligence, r/OSINT, r/CredibleDefense, r/WarCollege
* **Jeopolitik & Haberler:** r/Geopolitics, r/WorldNews, r/UkrainianConflict, r/SyrianCivilWar
* **Teknoloji & Teçhizat:** r/Tanks, r/Warships, r/Submarines, r/Aviation, r/CombatFootage

## Dosya Yapısı

- `getDataFromReddit.py`: RSS verilerini çeken ve veritabanına yazan ana bot.
- `auto_reporter.py`: Belirli zaman aralıklarıyla analiz sürecini tetikleyen otomasyon scripti.
- `global_analysis.py`: Veritabanındaki verileri bütüncül olarak analiz edip Markdown ve PDF raporları üreten çekirdek script.
- `osint_data_v2.db`: Verilerin saklandığı SQLite veritabanı.
- `reports/`: Üretilen analiz raporlarının (PDF ve MD) kaydedildiği klasör.

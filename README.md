# VectorOSINT

VectorOSINT, belirli savunma, askeri ve jeopolitik Reddit topluluklarından (subreddit) RSS beslemeleri aracılığıyla veri toplayan ve bu verileri yerel bir veritabanında saklayıp yapay zeka ile analiz eden bir OSINT (Açık Kaynak İstihbarat) aracıdır.

## Özellikler

- **Veri Toplama:** 20'den fazla savunma ve istihbarat odaklı subreddit'ten (örn. OSINT, Military, Geopolitics) otomatik veri çeker.
- **Veri Saklama:** Toplanan verileri SQLite veritabanında (`osint_data_v2.db`) saklar, tekrarlayan kayıtları önler.
- **Yapay Zeka Analizi:** Toplanan verileri yerel olarak çalışan LLM (Ollama - Gemma 3) kullanarak analiz eder ve anahtar kavramları çıkarır.

## Gereksinimler

Bu projeyi çalıştırmak için aşağıdaki yazılımlara ve Python kütüphanelerine ihtiyacınız vardır:

### Sistem Gereksinimleri
- Python 3.8+
- [Ollama](https://ollama.com/) (Yerel LLM çalıştırmak için)

### Python Kütüphaneleri
Gerekli kütüphaneleri yüklemek için aşağıdaki komutu kullanabilirsiniz:

```bash
pip install requests feedparser sqlalchemy ollama
```

### Ollama Kurulumu
Proje analiz için `gemma3:4b` modelini kullanmaktadır. Ollama'yı kurduktan sonra terminalden aşağıdaki komutla modeli indirin:

```bash
ollama pull gemma3:4b
```

## Kurulum ve Kullanım

1. **Projeyi Klonlayın:**
   ```bash
   git clone https://github.com/kullaniciadi/vectorOSINT.git
   cd vectorOSINT
   ```

2. **Veri Toplamayı Başlatın:**
   `getDataFromReddit.py` dosyası sürekli çalışan bir döngüde verileri toplar ve veritabanına kaydeder.
   
   ```bash
   python getDataFromReddit.py
   ```
   *Not: Bu script sürekli çalışacak şekilde ayarlanmıştır. Durdurmak için `Ctrl+C` yapabilirsiniz.*

3. **Verileri Analiz Edin:**
   Toplanan verileri analiz etmek için `global_analysis.py` dosyasını çalıştırın. Bu script veritabanındaki tüm verileri bütüncül olarak inceler ve `.md` formatında rapor oluşturur.

   ```bash
   python global_analysis.py
   ```

## Hedeflenen Subredditler

Proje şu anda aşağıdaki kaynaklardan veri toplamaktadır:
* CredibleDefense, WarCollege, Military, Intelligence
* Geopolitics, OSINT, WorldNews
* UkrainianConflict, SyrianCivilWar, CombatFootage
* Aviation, Tanks, TankPorn, Warships, Submarines
* Ve daha fazlası...

## Dosya Yapısı

- `getDataFromReddit.py`: RSS beslemelerini çeken, parse eden ve veritabanına kaydeden ana bot.
- `global_analysis.py`: Veritabanındaki tüm verileri bütüncül olarak analiz edip rapor (.md) oluşturan script.
- `analysis.py`: (Eski) Basit seviyede tekil veri analizi yapan örnek script.
- `osint_data_v2.db`: Verilerin saklandığı SQLite veritabanı.

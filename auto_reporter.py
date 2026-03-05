import time
from global_analysis import analyze_all_posts

def main():
    sec = 360
    print("=== Otomatik Raporlama Servisi Başlatıldı ===")
    print(f"Mod: Test (Her {sec} saniyede bir analiz)")
    
    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{current_time}] Raporlama işlemi tetikleniyor...")
        
        try:
            analyze_all_posts()
            print(f"[{current_time}] İşlem başarıyla tamamlandı.")
        except Exception as e:
            print(f"[{current_time}] Rapor oluşturulurken hata oluştu: {e}")
            
        print(f"Bir sonraki analiz için bekleniyor ({sec} saniye)...")
        
        # Saat başı çalıştırmak için bu değeri 3600 yapın.
        time.sleep(sec)

if __name__ == "__main__":
    main()

import time
from global_analysis import analyze_all_posts

def main():
    print("=== Otomatik Raporlama Servisi Başlatıldı ===")
    print("Mod: Test (Her 5 dakikada bir analiz)")
    
    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{current_time}] Raporlama işlemi tetikleniyor...")
        
        try:
            analyze_all_posts()
            print(f"[{current_time}] İşlem başarıyla tamamlandı.")
        except Exception as e:
            print(f"[{current_time}] Rapor oluşturulurken hata oluştu: {e}")
            
        print("Bir sonraki analiz için bekleniyor (5 dakika)...")
        
        # Test için 5 dakika (300 saniye). 
        # Saat başı çalıştırmak için bu değeri 3600 yapın.
        time.sleep(7200)

if __name__ == "__main__":
    main()

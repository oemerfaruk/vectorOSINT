import requests
import feedparser
import time
from sqlalchemy import create_engine, Column, String, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Veritabanı ayarları
engine = create_engine('sqlite:///osint_finance_data.db')
Base = declarative_base()

# Tablo yapısını tanımlama
class RedditPost(Base):
    __tablename__ = 'reddit_posts'
    
    id = Column(Integer, primary_key=True)
    post_id = Column(String, unique=True)
    subreddit = Column(String, index=True)
    title = Column(String)
    summary = Column(Text)
    content = Column(Text)
    link = Column(String, unique=True)
    published_date = Column(String)
    updated_date = Column(String)
    author = Column(String)

# Tabloları oluştur
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def fetch_rss(rss_url):
    # RSS beslemesini çek
    response = requests.get(rss_url)
    if response.status_code == 200:
        feed = feedparser.parse(response.content)
        print("RSS Beslemesine erişildi.")
        return feed.entries
    else:
        print("RSS Beslemesine erişilemedi.")
        return []

def display_entries(entries):
    for entry in entries:
        print(f"Başlık: {entry.title}")
        print(f"Açıklama: {entry.summary}")
        print(f"Bağlantı: {entry.link}")
        print("------------")

def store_posts(entries, subreddit):
    for entry in entries:
        # Zaten kaydedilmişse atla
        if session.query(RedditPost).filter_by(link=entry.link).first() is None:
            pub_date = getattr(entry, 'published', 'Bilinmiyor')
            update_date = getattr(entry, 'updated', 'Bilinmiyor')
            author_name = getattr(entry, 'author', 'Bilinmiyor')
            p_id = getattr(entry, 'id', 'Bilinmiyor')
            
            # İçerik kısmını kontrol et (content listesi boş olabilir)
            content_val = ""
            if hasattr(entry, 'content') and len(entry.content) > 0:
                content_val = entry.content[0].value

            post = RedditPost(
                post_id=p_id,
                subreddit=subreddit, 
                title=entry.title, 
                summary=entry.summary, 
                content=content_val,
                link=entry.link,
                published_date=pub_date,
                updated_date=update_date,
                author=author_name
            )
            session.add(post)
            print(f"Kaydedildi: {entry.title}")
        else:
            print(f"Zaten mevcut: {entry.title}")
    
    session.commit()

subreddits = [
    # --- Küresel Finans & Ekonomi (Yeni Eklenenler) ---
    'Economics',           # Makroekonomi makaleleri ve akademik düzeyde tartışmalar
    'investing',           # Temel/teknik analiz odaklı ciddi yatırım topluluğu
    'stocks',              # Küresel borsa, hisse senetleri ve piyasa haberleri
    'personalfinance',     # Bireysel finans, portföy yönetimi ve bütçeleme
    'finance',             # Kurumsal finans ve finans sektörü üzerine profesyonel tartışmalar
    'wallstreetbets',      # Spekülatif hamleler ve yüksek riskli piyasa hareketleri
    'options',             # Türev piyasalar ve opsiyon ticareti odaklı
    'MacroEconomics',      # Küresel para politikaları ve merkez bankası kararları
    
    # --- Küresel Politika & Uluslararası İlişkiler (Yeni Eklenenler) ---
    'politics',            # Ağırlıklı ABD ve global etkileri olan en büyük politika subbredit'i
    'PoliticalDiscussion', # Haber linki paylaşımından ziyade medeni fikir teatisi alanı
    'InternationalRelations', # Uluslararası ilişkiler teorileri ve dış politika analizleri
    'news',                # Dünya genelinden güncel siyasi ve toplumsal gelişmeler
    'EuropeanFederalists', # Avrupa Birliği politikaları ve geleceği üzerine odaklı
    'ukpolitics'           # Avrupa ve Birleşik Krallık siyasetinin merkezi
]

while True:
    for subreddit in subreddits:
        rss_entries = fetch_rss(f'https://www.reddit.com/r/{subreddit}.rss')
        store_posts(rss_entries, subreddit)
    
    time.sleep(360)
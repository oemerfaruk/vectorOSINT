import requests
import feedparser
import time
from sqlalchemy import create_engine, Column, String, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Veritabanı ayarları
engine = create_engine('sqlite:///reddit_rss.db')
Base = declarative_base()

# Tablo yapısını tanımlama
class RedditPost(Base):
    __tablename__ = 'reddit_posts'
    
    id = Column(Integer, primary_key=True)
    subreddit = Column(String, index=True)
    title = Column(String)
    summary = Column(Text)
    link = Column(String, unique=True)

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
            post = RedditPost(subreddit=subreddit, title=entry.title, summary=entry.summary, link=entry.link)
            session.add(post)
            print(f"Kaydedildi: {entry.title}")
        else:
            print(f"Zaten mevcut: {entry.title}")
    
    session.commit()

subreddits = ['CredibleDefense','WarCollege','Military','Intelligence','geopolitics','OSINT','worldnews','UkrainianConflict','SyrianCivilWar','CombatFootage','Aviation','Tanks','TankPorn','Army','AFV','Warships','WarshipPorn','Navy','Submarines','MilitarySpace','Defense']

while True:
    for subreddit in subreddits:
        rss_entries = fetch_rss(f'https://www.reddit.com/r/{subreddit}.rss')
        store_posts(rss_entries, subreddit)
    
    time.sleep(10)
import ollama
import sqlite3

# 1. SQL Bağlantısı
conn = sqlite3.connect('reddit_rss.db')
cursor = conn.cursor()
cursor.execute("SELECT title FROM reddit_posts LIMIT 5") # Test için 5 tane
posts = cursor.fetchall()

# 2. Gemma-3 ile Analiz
for post in posts:
    response = ollama.chat(model='gemma3:4b', messages=[
      {'role': 'system', 'content': 'Sen bir veri analistisin. Posttaki anahtar kavramları çıkar.'},
      {'role': 'user', 'content': post[0]},
    ])
    print(f"Analiz Sonucu: {response['message']['content']}")
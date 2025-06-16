import feedparser
import hashlib
import sqlite3
from datetime import datetime

# --------- CONFIG ---------
RSS_FEEDS = {
    "TechCrunch": "https://techcrunch.com/feed/",
    "CNET": "https://www.cnet.com/rss/all/",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "Engadget": "https://www.engadget.com/rss.xml"
}

DB_NAME = "articles.db"

# --------- SETUP DB ---------
def setup_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            title TEXT,
            summary TEXT,
            url TEXT,
            source TEXT,
            published_at TEXT,
            image_url TEXT
        )
    """)
    conn.commit()
    conn.close()

# --------- HASH URL TO ID ---------
def make_id(url):
    return hashlib.sha1(url.encode("utf-8")).hexdigest()

# --------- SAVE ONE ARTICLE ---------
def save_article(article):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO articles (id, title, summary, url, source, published_at, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            article['id'],
            article['title'],
            article['summary'],
            article['url'],
            article['source'],
            article['published_at'],
            article['image_url']
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # already exists
    finally:
        conn.close()

# --------- MAIN FETCH LOOP ---------
def fetch_all():
    setup_db()
    for source, feed_url in RSS_FEEDS.items():
        print(f"📡 Fetching from {source}...")
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            url = entry.get("link")
            if not url:
                continue

            article = {
                "id": make_id(url),
                "title": entry.get("title", "No title"),
                "summary": entry.get("summary", "No summary"),
                "url": url,
                "source": source,
                "published_at": entry.get("published", datetime.now().isoformat()),
                "image_url": entry.get("media_content", [{}])[0].get("url") if entry.get("media_content") else None
            }
            save_article(article)
        print(f"✅ Done: {len(feed.entries)} entries checked for {source}.\n")

if __name__ == "__main__":
    fetch_all()

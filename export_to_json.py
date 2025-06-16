import sqlite3
import json

DB_NAME = "articles.db"
OUTPUT_FILE = "articles.json"

def export_articles():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT title, summary, url, source, published_at, image_url
        FROM articles
        ORDER BY published_at DESC
        LIMIT 50
    """)
    rows = c.fetchall()
    conn.close()

    articles = []
    for row in rows:
        articles.append({
            "title": row[0],
            "summary": row[1],
            "url": row[2],
            "source": row[3],
            "published_at": row[4],
            "image_url": row[5]
        })

    with open(OUTPUT_FILE, "w") as f:
        json.dump(articles, f, indent=2)

    print(f"✅ Exported {len(articles)} articles to {OUTPUT_FILE}")

if __name__ == "__main__":
    export_articles()

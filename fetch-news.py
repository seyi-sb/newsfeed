import requests
import json
from datetime import datetime

# Replace with your actual API key
API_KEY = "16cb6436c114446aa58e4c88a188e22d"

# Define the endpoint and parameters
url = "https://newsapi.org/v2/everything"
params = {
    "q": "technology",
    "sortBy": "publishedAt",
    "language": "en",
    "pageSize": 10,
    "apiKey": API_KEY
}

# Send the request
response = requests.get(url, params=params)

# Parse the response
if response.status_code == 200:
    articles = response.json().get("articles", [])
    
    # Save to a local JSON file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"tech_news_{timestamp}.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2)

    print(f"✅ {len(articles)} articles saved to tech_news_{timestamp}.json")
else:
    print(f"❌ Failed to fetch articles: {response.status_code}")
    print(response.text)

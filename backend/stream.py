import os
import time
import json
import redis
import praw
from dotenv import load_dotenv
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
)

# subs = ["news", "worldnews", "technology", "politics", "science"]
subs = [
  "news",
  "politics",
  "politicaldebate",
  "politicaldiscussion",
  "worldnews",
  "technology",
  "science",
  "artificial",
  "artificialintelligence",
  "geopolotics"
]

subreddit = reddit.subreddit("+".join(subs))
buffer_key = "news_buffer"

def stream_and_buffer():
    print("Streaming r/news submissions into Redis…")
    for submission in subreddit.stream.submissions(skip_existing=True):
        payload = {
            "id": submission.id,
            "title": submission.title,
            "selftext": submission.selftext,
            "url": submission.url,
            "created_utc": submission.created_utc
        }
        # push JSON-encoded post into a Redis list
        r.rpush(buffer_key, json.dumps(payload))
        print(f"  • buffered {submission.id}")

if __name__ == "__main__":
    try:
        stream_and_buffer()
    except KeyboardInterrupt:
        print("\n🛑  Stream interrupted, exiting.")

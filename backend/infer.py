import os
import json
import redis
from transformers import pipeline

# — Redis connection —
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
)

# — Initialize Hugging Face sentiment pipeline —
sentiment = pipeline(
    "sentiment-analysis",
    model=os.getenv(
        "SENTIMENT_MODEL",
        "distilbert-base-uncased-finetuned-sst-2-english"
    )
)

buffer_key = "news_buffer"

def run_inference():
    # pop everything in the buffer
    raw_items = []
    while True:
        raw = r.lpop(buffer_key)
        if raw is None:
            break
        raw_items.append(json.loads(raw))

    if not raw_items:
        print("⚠️  No items to process right now.")
        return

    for item in raw_items:
        text = (item["title"] or "") + " " + (item["selftext"] or "")
        result = sentiment(text[:512])[0]  # truncate to 512 tokens
        print(f"{item['id']}: {result['label']} ({result['score']:.2f})")

if __name__ == "__main__":
    run_inference()

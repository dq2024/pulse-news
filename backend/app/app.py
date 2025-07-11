import os
import json
import threading
import time
from datetime import datetime, timezone, timedelta

import redis
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from model import get_sentiment_pipeline

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Reddit Sentiment Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Redis setup
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
)
BUFFER_KEY  = "news_buffer"
RESULTS_KEY = "sentiment_buffer"

classifier = None

# Shemas
class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    label: str
    score: float

class ResultItem(BaseModel):
    id: str
    title: str
    url: str
    label: str
    score: float
    created_utc: int

class StatsResponse(BaseModel):
    window_minutes: int
    start_time_utc: int
    end_time_utc: int
    average_sentiment: float
    positive_count: int
    negative_count: int
    total_count: int

# Startup
@app.on_event("startup")
def startup_event():
    global classifier
    classifier = get_sentiment_pipeline()
    thread = threading.Thread(target=process_buffer, daemon=True)
    thread.start()

def process_buffer():
    """
    Poll news_buffer -> classify -> push full record into sentiment_buffer
    """
    while True:
        raw = r.lpop(BUFFER_KEY)
        if raw:
            item = json.loads(raw)
            text = ((item.get("title") or "") + " " + (item.get("selftext") or ""))[:512]
            try:
                result = classifier(text)[0]
                out = {
                    "id":    item.get("id"),
                    "title": item.get("title") or "",
                    "url":   item.get("url") or "",
                    "label": result["label"],
                    "score": result["score"],
                    "created_utc": item.get("created_utc")
                }
                r.rpush(RESULTS_KEY, json.dumps(out))
                print(f"✔ Processed {out['id']}: {out['label']} ({out['score']:.2f})")
            except Exception as e:
                print(f"Error processing {item.get('id')}: {e}")
        else:
            time.sleep(1)

# --- Endpoints ----------------------------------------------

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        res = classifier(req.text[:512])[0]
        return PredictResponse(label=res["label"], score=res["score"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results", response_model=list[ResultItem])
def get_results(limit: int = Query(50, ge=1, le=200)):
    """
    Return the most recent `limit` classified items.
    """
    raw_list = r.lrange(RESULTS_KEY, -limit, -1)
    # each raw is JSON string
    items = [json.loads(x) for x in raw_list]
    # Redis LRANGE -limit,-1 gives oldest→newest; we want newest first
    items.reverse()
    return items

@app.get("/stats", response_model=StatsResponse)
def get_stats(window: int = Query(60, ge=1, le=1440)):
    """
    Aggregate sentiment over the past `window` minutes.
    POSITIVE → +1, NEGATIVE → -1.
    """
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(minutes=window)
    cutoff_ts = int(cutoff.timestamp())

    raw_list = r.lrange(RESULTS_KEY, 0, -1)
    total, pos, neg, acc = 0, 0, 0, 0.0

    for raw in raw_list:
        obj = json.loads(raw)
        ts = obj.get("created_utc", 0)
        # if ts < cutoff_ts:
        #     continue
        total += 1
        if obj["label"] == "POSITIVE":
            pos += 1
            acc += 1
        else:
            neg += 1
            acc -= 1

    avg = (acc / total) if total else 0.0

    return StatsResponse(
        window_minutes=window,
        start_time_utc=cutoff_ts,
        end_time_utc=int(now.timestamp()),
        average_sentiment=avg,
        positive_count=pos,
        negative_count=neg,
        total_count=total
    )

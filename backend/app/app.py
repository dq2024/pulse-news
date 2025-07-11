import os
import json
import threading
import time

import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from model import get_sentiment_pipeline

# FastAPI app
app = FastAPI(title="Reddit Sentiment Service")

# Redis setup
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
)
BUFFER_KEY = "news_buffer"        
RESULTS_KEY = "sentiment_buffer"  

# Sentiment pipeline (populated at startup)
classifier = None

# Request/response schemas
class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    label: str
    score: float

@app.on_event("startup")
def startup_event():
    global classifier
    classifier = get_sentiment_pipeline()

    # launch background thread to process the buffer
    thread = threading.Thread(target=process_buffer, daemon=True)
    thread.start()

def process_buffer():
    """
    Continuously poll news_buffer, run inference, and push
    results into sentiment_buffer.
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
                    "label": result["label"],
                    "score": result["score"],
                }
                r.rpush(RESULTS_KEY, json.dumps(out))
                print(f"Processed {out['id']}: {out['label']} ({out['score']:.2f})")
            except Exception as e:
                print(f"Error processing {item.get('id')}: {e}")
        else:
            time.sleep(1)  # no items, back off briefly

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    """
    On-demand sentiment for arbitrary text.
    """
    try:
        res = classifier(req.text[:512])[0]
        return PredictResponse(label=res["label"], score=res["score"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import os
from transformers import pipeline

def get_sentiment_pipeline():
    model_name = os.getenv(
        "SENTIMENT_MODEL",
        "distilbert-base-uncased-finetuned-sst-2-english"
    )
    # load once at startup
    return pipeline("sentiment-analysis", model=model_name)

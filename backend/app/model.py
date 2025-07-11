import os
from transformers import pipeline

def get_sentiment_pipeline():
    model_name = os.getenv(
        "SENTIMENT_MODEL",
        "siebert/sentiment-roberta-large-english"
    )
    # load once at startup
    return pipeline("sentiment-analysis", model=model_name)

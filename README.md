**PulseNews: Real-Time Twitter Sentiment Dashboard**

This project implements an end-to-end machine learning engineering pipeline that streams live tweets from Twitter, performs sentiment analysis using a transformer-based NLP model, and visualizes real-time sentiment trends on a web dashboard. It covers data ingestion, model serving, frontend visualization, containerization, deployment, and monitoring, showcasing a full production-style workflow suitable for ML Engineer roles.

---

## Features

- **Live Tweet Streaming**: Collect tweets matching configurable keywords via the Twitter API.
- **Sentiment Analysis Service**: Wrap a fine-tuned transformer (e.g., DistilBERT) in a FastAPI microservice for low-latency inference.
- **Interactive Dashboard**: React-based frontend that polls sentiment scores and renders a time-series chart of average sentiment, plus top positive/negative tweet examples.
- **Containerization**: Docker files for both backend and frontend; local testing via Docker Compose.
- **Cloud Deployment**: CI/CD pipeline (GitHub Actions) to build, test, and deploy services to AWS ECS (Fargate) or Elastic Beanstalk.
- **Monitoring & Alerts**: Prometheus metrics for latency, error rate, and sentiment drift; Grafana dashboard and alerting via Slack or email.

---

## Tech Stack

- **Backend**: Python, FastAPI, Hugging Face Transformers, Kafka/Redis (optional streaming buffer)
- **Frontend**: React, Chart.js (or D3.js)
- **Infrastructure**: Docker, Docker Compose, AWS ECS (Fargate) or Elastic Beanstalk, GitHub Actions
- **Monitoring**: Prometheus, Grafana, Alertmanager

---

## Getting Started

1. **Clone the repo**

   ```bash
   git clone https://github.com/<your-username>/twitter-sentiment-dashboard.git
   cd twitter-sentiment-dashboard
   brew services start redis
   ```

2. **Configure environment variables**

   - Set Twitter API keys, Redis/Kafka endpoints, and other settings in `.env` file

3. **Local development**

   ```bash
   docker-compose up --build
   ```

   - Backend at `http://localhost:8000`
   - Frontend at `http://localhost:3000`


---

## Deployment

1. Push images to Docker Hub or ECR via GitHub Actions on merge to `main`.
2. GitHub Actions deploy job updates services on AWS ECS (Fargate).
3. Prometheus and Grafana run in a sidecar or separate EC2 instance; dashboards auto-provisioned via Terraform or CloudFormation.

---

## Project Structure

```
twitter-sentiment-dashboard/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entrypoint
│   │   ├── model.py          # Sentiment model loader & inference
│   │   ├── schemas.py        # Pydantic request/response schemas
│   │   └── stream.py         # Tweet streaming & buffer logic
│   ├── Dockerfile
│   ├── requirements.txt
│   └── tests/                # Pytest test cases
│       └── test_model.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── components/       # Dashboard components
│   │   └── api.js            # API client to backend
│   ├── Dockerfile
│   └── package.json
│
├── infra/
│   ├── docker-compose.yml    # Local orchestration
│   ├── ecs-terraform/        # Terraform configs for ECS & monitoring
│   └── github-actions.yml    # CI/CD workflow definition
│
├── .env.example
├── README.md
└── LICENSE
```

---

## Next Steps

1. Set up Twitter developer account and generate API credentials.
2. Prototype tweet collection and model inference in a Jupyter notebook.
3. Containerize services and iterate on the CI/CD workflow.
4. Add monitoring dashboards and alert rules.

Feel free to customize keywords, extend the front-end UI, or swap in other streaming sources. Good luck, and happy coding!


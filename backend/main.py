from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Farmer Bot backend chal raha hai! 🌾"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
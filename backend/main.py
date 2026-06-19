from fastapi import FastAPI
from routes.mandi_routes import router as mandi_router

app = FastAPI()

app.include_router(mandi_router)


@app.get("/")
def home():
    return {"message": "AI Farmer Bot backend chal raha hai! 🌾"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
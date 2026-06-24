from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.mandi_routes import router as mandi_router
from routes.scheme_routes import router as scheme_router

app = FastAPI()

# CORS allow karo taaki React frontend backend se baat kar sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development ke liye sab allow, production mein specific URL dena
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mandi_router)
app.include_router(scheme_router)

@app.get("/")
def home():
    return {"message": "AI Farmer Bot backend chal raha hai! 🌾"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
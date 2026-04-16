from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.api.routes import router

app = FastAPI(
    title="Mechanical Hand Calculation Tools API",
    version="0.1.0",
    description="Plugin-based catalog API for mechanical hand calculations.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

handler = Mangum(app)

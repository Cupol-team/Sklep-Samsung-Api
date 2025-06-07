from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.config import config
from routers import product_router, photo_router, category_router

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"])

origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router)
app.include_router(photo_router)
app.include_router(category_router)

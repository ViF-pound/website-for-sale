from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db import engine, Base
from src.catalog.catalog_router import catalog_router
from src.app_auth.auth_router import auth_router
from src.seller.seller_router import seller_router

from binascii import Error
import os

app = FastAPI()

app.include_router(auth_router)
app.include_router(catalog_router)
app.include_router(seller_router)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type",
                   "Set-Cookie",
                   "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

@app.get("/init")
async def create_db():
    
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
        except Error as e:
            print(e)
        await  conn.run_sync(Base.metadata.create_all)

UPLOAD_FOLDER = 'uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
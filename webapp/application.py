from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os, sys
sys.path.insert(1, os.getcwd())

from webapp.backend import all_routers

app = FastAPI()
[app.include_router(r) for r in all_routers]

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
async def connect():
    return {"message": "Hello World"}
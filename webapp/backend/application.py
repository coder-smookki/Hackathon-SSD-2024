from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from users import users_routers
import os, sys


sys.path.insert(1, os.getcwd())
all_routers = [*users_routers]
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
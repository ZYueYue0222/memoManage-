from fastapi import FastAPI, HTTPException
from app.router import router
from fastapi.middleware.cors import CORSMiddleware
from app.get_db import create_tables
from fastapi.responses import JSONResponse
from fastapi import Request

app=FastAPI(title="备忘录信息管理系统API")

create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router.router)
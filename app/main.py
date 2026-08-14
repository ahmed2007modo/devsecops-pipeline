"""FastAPI application with /health and /login endpoints."""

import datetime
import os

import jwt
from fastapi import FastAPI, HTTPException
from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel

app = FastAPI(title="DevSecOps Demo App", version="1.0.0")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-only-insecure-fallback")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_MINUTES = 30

# Demo credentials: username=admin / password=password (pbkdf2_sha256 hash)
DEMO_USER_HASH = "$pbkdf2-sha256$29000$s7a2FiKk9F6L8V7rXat1rg$gwIIve6/qSIkz4vV4.nOoBLK.8vh917JWCIysNDunH0"


class LoginRequest(BaseModel):
    username: str
    password: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/login")
def login(payload: LoginRequest) -> dict:
    if payload.username != "admin" or not pbkdf2_sha256.verify(payload.password, DEMO_USER_HASH):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {
            "sub": payload.username,
            "exp": datetime.datetime.now(datetime.UTC)
            + datetime.timedelta(minutes=JWT_EXPIRES_MINUTES),
        },
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )
    return {"access_token": token, "token_type": "bearer"}

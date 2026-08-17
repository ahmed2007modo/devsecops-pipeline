#not infected code

"""FastAPI application with /health and /login endpoints."""

import datetime
import os

import jwt
from fastapi import FastAPI, HTTPException
from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel

app = FastAPI(title="DevSecOps Demo App", version="1.0.0")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise RuntimeError("CRITICAL: JWT_SECRET_KEY environment variable is not set.")

JWT_ALGORITHM = "HS256"
JWT_EXPIRES_MINUTES = 30

DEMO_USER_HASH = os.getenv("DEMO_USER_HASH")
if not DEMO_USER_HASH:
    raise RuntimeError("CRITICAL: DEMO_USER_HASH environment variable is not set.")


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

    now = datetime.datetime.now(datetime.timezone.utc)
    token = jwt.encode(
        {
            "sub": payload.username,
            "exp": now + datetime.timedelta(minutes=JWT_EXPIRES_MINUTES),
        },
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )
    return {"access_token": token, "token_type": "bearer"}
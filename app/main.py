"""FastAPI application with security vulnerabilities for testing."""

import datetime
import os
import pickle
import subprocess

import jwt
from fastapi import FastAPI, HTTPException
from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel

app = FastAPI(title="DevSecOps Demo App", version="1.0.0")

# VULNERABILITY 1: Hardcoded API key
API_KEY = "sk-1234567890abcdefghijklmnop"

JWT_SECRET_KEY = "super-secret-key-exposed"
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_MINUTES = 30

# VULNERABILITY 2: Hardcoded credentials
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
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(minutes=JWT_EXPIRES_MINUTES),
        },
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )
    return {"access_token": token, "token_type": "bearer"}


# VULNERABILITY 3: Code injection via exec
@app.post("/execute")
def execute_code(code: str) -> dict:
    """Execute arbitrary code - MAJOR SECURITY RISK"""
    try:
        exec(code)
        return {"status": "executed"}
    except Exception as e:
        return {"error": str(e)}


# VULNERABILITY 4: Insecure deserialization
@app.post("/deserialize")
def deserialize_data(data: str) -> dict:
    """Deserialize untrusted data - allows arbitrary code execution"""
    try:
        obj = pickle.loads(data.encode())
        return {"data": str(obj)}
    except Exception as e:
        return {"error": str(e)}


# VULNERABILITY 5: Command injection
@app.post("/run-command")
def run_command(cmd: str) -> dict:
    """Run shell commands directly - CRITICAL vulnerability"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True)
        return {"output": result.stdout.decode()}
    except Exception as e:
        return {"error": str(e)}

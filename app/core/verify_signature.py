import os
import nacl.signing
import nacl.exceptions
from fastapi import Request, HTTPException
from dotenv import load_dotenv
from .config import settings

load_dotenv()

PUBLIC_KEY = settings.discord_public_key

def verify_signature(request: Request, body: bytes):
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")

    if not signature or not timestamp:
        raise HTTPException(status_code=401, detail="Missing signature headers")

    try:
        verify_key = nacl.signing.VerifyKey(bytes.fromhex(PUBLIC_KEY))
        verify_key.verify(f"{timestamp}{body.decode()}".encode(), bytes.fromhex(signature))
    except nacl.exceptions.BadSignatureError:
        raise HTTPException(status_code=401, detail="Invalid request signature")
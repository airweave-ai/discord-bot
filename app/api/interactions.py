from fastapi import APIRouter, Request
from app.core.verify_signature import verify_signature

router = APIRouter()

@router.post("/interactions")
async def interactions(request: Request):
    body = await request.body()
    verify_signature(request, body)
    payload = await request.json()

    if payload.get("type") == 1:
        # PING request
        return {"type": 1}

    # Handle other interaction types here
    return {"type": 4, "data": {"content": "Hello from FastAPI!"}}
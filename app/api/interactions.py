from fastapi import APIRouter, Request
from app.core.verify_signature import verify_signature
from app.api import auth, user

router = APIRouter()
router.include_router(auth.router, prefix="/discord/auth", tags=["auth"])
router.include_router(user.router, prefix="/discord/user", tags=["user"])

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
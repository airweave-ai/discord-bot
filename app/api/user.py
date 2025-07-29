from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.auth_service import AuthService
from app.services.session_service import SessionService
from app.services.user_service import UserService
router = APIRouter()

# Writing api endpoints for getting User data and guilds
class UserRequest(BaseModel):
    session_token: str
def get_auth_service() -> AuthService:
    return AuthService()
def get_session_service() -> SessionService:
    return SessionService()
def get_user_service() -> UserService:
    return UserService()

@router.post("/")
async def get_user_data(
    request: UserRequest,
    session_service: SessionService = Depends(get_session_service),
    user_service: UserService = Depends(get_user_service)
    ):
    if not request.session_token:
        raise HTTPException(status_code=400, detail="Session token is required")
    
    session = await session_service.get_session(request.session_token)
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_id = session.user_id # type: ignore
    token = await session_service.get_token_from_session(request.session_token)
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_data = await user_service.get_user_data(token.access_token)  # type: ignore
    if not user_data:
        raise HTTPException(status_code=404, detail="User data not found")
    await user_service.save_user_data(user_id=user_id,user_data=user_data)
    return user_data
    

@router.post("/guilds")
async def get_user_guilds(
    request: UserRequest,
    session_service: SessionService = Depends(get_session_service),
    user_service: UserService = Depends(get_user_service)
    ):

    if not request.session_token:
        raise HTTPException(status_code=400, detail="Session token is required")
    
    session = await session_service.get_session(request.session_token)
    print(f"Session: {session}")
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized session")
    user_id = session.user_id  
    
    token = await session_service.get_token_from_session(request.session_token)
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized session")
    return await user_service.get_user_guilds(user_id, token)  
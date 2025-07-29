from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from loguru import logger
from app.models.types.auth import CodePayload,BotPayload
from app.services.auth_service import AuthService
from app.services.session_service import SessionService

router = APIRouter()

def get_auth_service() -> AuthService:
    return AuthService()
def get_session_service() -> SessionService:
    return SessionService()

@router.post("/code")
async def authenticate_with_code(
    payload: CodePayload,
    auth_service: AuthService = Depends(get_auth_service)
    ):
    """
    Endpoint to exchange authorization code for access token and user data.
    """
    if not payload.code:
        raise HTTPException(status_code=400, detail="Authorization Code is required")
    try:
        session_token, status_code = await auth_service.authenticate_with_discord(payload.code)
        return JSONResponse(status_code=status_code, content={"session_token": session_token})
    except HTTPException as e:
        logger.error(f"Authentication failed: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/bot")
async def bot_authentication(
    user_request: BotPayload,
    session_service: SessionService = Depends(get_session_service),
    auth_service: AuthService = Depends(get_auth_service)
    ):
    session = await session_service.get_session(user_request.session_token)
    if not session:
        raise HTTPException(status_code=401, detail="Session does not exist")
    user_id = session.user_id
    guild_id = user_request.guild_id
    if not guild_id:
        raise HTTPException(status_code=400, detail="Guild ID is required")
    return await auth_service.bot_auth(user_id= user_id, guild_id=guild_id)

# Reference: https://discord.com/developers/docs/topics/oauth2#revoking-a-token

# SECTION: OAuth2 Enhancements
# TODO: Implement token revocation
#       Revoke user tokens securely using Discord's OAuth2 revoke endpoint.
# TODO: Add refresh fallback logic
#       Automatically refresh tokens on expiry and retry failed API calls.
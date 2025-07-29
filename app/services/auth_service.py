import httpx
from loguru import logger
from datetime import datetime, timezone
from fastapi import HTTPException
from urllib.parse import urlencode
from typing import Dict, Any
from app.core.redis_client import redis_client
from app.models.types.auth import OauthToken
from app.core.config import settings
from app.services import user_service, session_service
class AuthService:
    
    def __init__(self):
        self.redis_client = redis_client
        self.user_service = user_service.UserService()
        self.session_service = session_service.SessionService()
    
    async def authenticate_with_discord(self,code:str):

        token_data = await self.exchange_code_for_token(code)
        if not token_data:
            raise HTTPException(status_code=400, detail="Failed to exchange code for token")
        user_data = await self.user_service.get_user_data(token_data['access_token'])
        if not user_data:
            raise HTTPException(status_code=400, detail="Failed to fetch user data")
        user_id = user_data['id']
        await self.user_service.save_user_data(user_id, user_data)
        await self.save_tokens(user_id, token_data)
        session_data = {
            "user_id": user_data["id"],
            "username": user_data["username"],
            "global_name": user_data.get("global_name", None),
            "is_authenticated": True
        }
        session_token = await self.session_service.create_session(session_data=session_data, expires_in=86400)

        return session_token, 200
    
    async def exchange_code_for_token(self, code: str)-> Dict[Any,str]:
        """
        Exchange the authorization code for an access token.
        """
        if not code:
            raise HTTPException(status_code=400, detail="Autherisation Code is required")
        
        data = {
            "client_id": settings.discord.CLIENT_ID,
            "client_secret": settings.discord.CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.discord.REDIRECT_URI,
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
                if response.status_code != 200:
                    logger.error(f"Discord token exchange failed: {response.status_code} - {response.text}")
                    raise HTTPException(status_code=400, detail="Authentication failed")
                if response.status_code != 200:
                    print("Discord token exchange failed:", response.status_code, response.text)
                    logger.error(f"Discord token exchange failed: {response.status_code} - {response.text}")
                    raise HTTPException(status_code=400, detail="Token exchange failed")
                token_data = response.json()
                logger.info(f"Token data received: {token_data}")
                return token_data # Pydantic validation
        except httpx.TimeoutException:
            raise HTTPException(status_code=408, detail="Request timeout")
        except httpx.RequestError as e:
            logger.error(f"Request error during Discord OAuth: {e}")
            raise HTTPException(status_code=500, detail="External service error")
    
    async def save_tokens(self, user_id: str, token_data):
        """ 
        Save the access and refresh tokens for a user.
        """
        if 'expires_in' in token_data:
    # If token has expires_in, convert to expires_at
            expires_at = int(datetime.now(timezone.utc).timestamp()) + token_data['expires_in']
            token_data['expires_at'] = expires_at
            token_data.pop('expires_in', None)  

        user_oauth_token = OauthToken(**token_data) 
        try:
            await redis_client.set(f"user:{user_id}:token", user_oauth_token.model_dump_json())
        except Exception as e:
            logger.error(f"Error saving tokens: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        
    async def get_valid_access_token(self,session_token:str):
        """
        Retrieve a valid access token for a user.
        """
        session_data =  await self.session_service.get_session(session_token=session_token)
        print(session_data)
        if not session_data:
            raise HTTPException(status_code=401, detail="Unauthorized")
        user_id = session_data.user_id # type: ignore
        token_data = await redis_client.get(f"user:{user_id}:token")
        if not token_data:
            return None
        token = OauthToken.model_validate_json(token_data)
        if token.expires_at - int(datetime.now(timezone.utc).timestamp()) < 3600:
            return await self.refresh_access_token(user_id = user_id,token=token)
        return token
    
    async def refresh_access_token(self, user_id: str,token: OauthToken):
        """
        Refresh the access token for a user.
        """
        refresh_token = token.refresh_token
        data = {
            "client_id": settings.discord.CLIENT_ID,
            "client_secret": settings.discord.CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token

        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        async with httpx.AsyncClient() as client:
            response = await client.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Token exchange failed")
        
        token_data = response.json()
        await self.save_tokens(user_id=user_id,token_data=token_data)

        return token_data
    async def bot_auth(self, user_id: str, guild_id: str):
        """
        Handle bot authorization requests.
        """
        # Implementation of bot authorization logic
        try:
            
            # Build the authorization URL for bot installation
            params = {
                "client_id": settings.discord.CLIENT_ID,
                "scope": "bot applications.commands",
                "permissions": "364870364415",
                "guild_id": guild_id,
                "disable_guild_select": "false"
            }
            
            # Generate the URL that the user needs to visit
            auth_url = f"{settings.discord.API_BASE_URL}/oauth2/authorize?" + urlencode(params)
            
            return {
                "authorization_url": auth_url,
                "message": "Please visit this URL to add the bot to your guild"
            }
        except Exception as e:
            logger.error(f"Error during bot authorization: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        

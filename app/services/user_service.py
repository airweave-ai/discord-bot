import httpx
from typing import Optional, List, Dict, Any
from fastapi import HTTPException
from loguru import logger
from app.core.redis_client import redis_client
from app.models.types.user import User
from app.core.config import settings


class UserService:
    
    def __init__(self):
        self.redis_client = redis_client

    async def get_user_data(self,access_token:str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user data from the database.
        """
        try:
            async with httpx.AsyncClient() as client:
                user_response = await client.get(
                "https://discord.com/api/users/@me",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10.0
            )
            
            if user_response.status_code != 200:
                logger.error(f"Failed to fetch Discord user data: {user_response.status_code}")
                raise HTTPException(status_code=400, detail="Failed to fetch user data")
            
            user_data = user_response.json()
            return user_data
        except httpx.TimeoutException:
            raise HTTPException(status_code=408, detail="Request timeout")
        except httpx.RequestError as e:
            logger.error(f"Request error during Discord API call: {e}")
            raise HTTPException(status_code=500, detail="External service error")
        

    async def save_user_data(self, user_id: str, user_data: Dict[str, Any]):
        """
        Save user data to the database.
        """
        try:
            user = User(**user_data)  # Pydantic validation
            await self.redis_client.set(f"user:{user_id}", user.model_dump_json())
        except Exception as e:
            logger.error(f"Error saving user data: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        
    async def delete_user_data(self, user_id: str):
        """ 
        Delete user data from the database.
        """
        try:
            await self.redis_client.delete(f"user:{user_id}")
        except Exception as e:
            logger.error(f"Error deleting user data: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def get_user_guilds(self, user_id: str,token) -> List[Dict[str, Any]]:
        """
        Retrieve a list of guild IDs the user is part of.
        """
        try:
            async with httpx.AsyncClient() as client:
                headers={
                "Authorization": f"Bearer {token.access_token}",  
                }   
            async with httpx.AsyncClient() as client:
                guilds_response = await client.get(
                    f"{settings.discord.API_BASE_URL}/users/@me/guilds",
                    headers=headers
                )
            if guilds_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to fetch user guilds")      
            guilds_data = guilds_response.json()
            filtered_guilds = [guild for guild in guilds_data if guild.get("owner", False)]
            if not filtered_guilds:
                raise HTTPException(status_code=404, detail="No guilds found for the user")
            
            return filtered_guilds
        except httpx.TimeoutException:
            raise HTTPException(status_code=408, detail="Request timeout")
        except httpx.RequestError as e:
            logger.error(f"Request error during Discord API call: {e}")
            raise HTTPException(status_code=500, detail="External service error")
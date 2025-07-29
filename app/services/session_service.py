from typing import Optional
from fastapi import HTTPException
from app.core.redis_client import redis_client
from app.models.types.auth import Session
import uuid
from loguru import logger
from app.models.types.auth import OauthToken

class SessionService:
    def __init__(self) -> None:
        self.redis_client = redis_client
    async def create_session(self, session_data: dict,expires_in: int = 86400)-> str:
        """Create a new user session and store it in Redis.
        Args:
            session_data (dict): The session data to store.
            session_token (str): The unique token for the session.
            expires_in (int): The expiration time in seconds for the session.
        """
        try:
            session_token = str(uuid.uuid4())
            session = Session(**session_data)
            print(f"Session Data: {session_data}")
            await self.redis_client.set(f"session:{session_token}:session",session.model_dump_json(),ex=expires_in)
            return session_token
        except Exception as e:
            logger.error(f"Error creating session: {str(e)}")
            raise HTTPException(status_code=500, detail="Error creating session")
        
    async def get_session(self, session_token)-> Optional[Session]:
        """
        Retrieve a user session by its token.
        """
        try:
            session_data = await self.redis_client.get(f"session:{session_token}:session")
            if not session_data:
                return None
            return Session.model_validate_json(session_data) 
        except Exception as e:
            logger.error(f"Error retrieving session: {str(e)}")
            raise HTTPException(status_code=500, detail="Error retrieving session")
    async def get_token_from_session(self, session_token: str):
        """
        Retrieve the session token from a user session.
        """
        session = await self.get_session(session_token)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        user_id = session.user_id  
        token = await self.redis_client.get(f"user:{user_id}:token")
        return OauthToken.model_validate_json(token)
    
    async def delete_session(self, session_token: str):
        """
        Delete a user session by its token.
        """
        try:
            await self.redis_client.delete(f"session:{session_token}:session")
        except Exception as e:
            logger.error(f"Error deleting session: {str(e)}")
            raise HTTPException(status_code=500, detail="Error deleting session")

    
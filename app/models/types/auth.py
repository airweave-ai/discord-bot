from typing import Optional
from pydantic import BaseModel, Field

class CodePayload(BaseModel):
    code: str

class BotPayload(BaseModel):
    session_token: str
    guild_id: str

class Session(BaseModel):
    user_id: str
    username: str
    global_name: Optional[str] = Field(default=None)
    # avatar: str
    is_authenticated: bool = False

class OauthToken(BaseModel):
    access_token: str
    token_type: str
    expires_at: int
    refresh_token: str
    scope: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str

    def to_dict(self) -> dict:
        """Convert the TokenResponse to a dictionary."""
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "refresh_token": self.refresh_token,
            "scope": self.scope
        }
    def is_expired(self) -> bool:
        """Check if the token is expired based on the current time."""
        return self.expires_in <= 0
    def __str__(self) -> str:
        """Return a string representation of the TokenResponse."""
        return f"TokenResponse(access_token={self.access_token}, token_type={self.token_type}, expires_in={self.expires_in}, refresh_token={self.refresh_token}, scope={self.scope})"
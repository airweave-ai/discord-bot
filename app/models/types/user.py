from typing import Literal, Optional
from pydantic import BaseModel, Field
from .snowflake import Snowflake



class UserSession(BaseModel):
    user_id: str
    username: str
    global_name: Optional[str] = Field(default=None)
    # avatar: str
    is_authenticated: bool = False
    
class AvatarDecorationData(BaseModel):
    asset: str
    sku_id: Snowflake

class PartialUser(BaseModel):
    model_type:str = "partial_user"
    id: Snowflake
    username: str
    discriminator: str
    avatar: Optional[str] = Field(default=None)
    global_name: Optional[str] = Field(default=None)
    avatar_decoration_data: Optional[AvatarDecorationData] = Field(default=None)

PremiumType = Literal[0, 1, 2, 3]

class User(BaseModel):
    model_type:str = "user"
    id: Snowflake
    username: str
    discriminator: str
    avatar: Optional[str] = Field(default=None)
    global_name: Optional[str] = Field(default=None)
    avatar_decoration_data: Optional[AvatarDecorationData] = Field(default=None)
    bot: Optional[bool] = Field(default=None)
    system: Optional[bool] = Field(default=None)
    mfa_enabled: Optional[bool] = Field(default=None)
    locale: Optional[str] = Field(default=None)
    verified: Optional[bool] = Field(default=None)
    email: Optional[str] = Field(default=None)
    flags: Optional[int] = Field(default=None)
    premium_type: Optional[PremiumType] = Field(default=None)
    public_flags: Optional[int] = Field(default=None)
from typing import TYPE_CHECKING
from fastapi import Body
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from app.models.types.user import UserSession, User as UserPayload, PartialUser as PartialUserPayload
    from datetime import datetime, timedelta

__all__ = (
    'User',
    # 'ClientUser',
)

class User():
    def __init__(self, data: Union[UserPayload,PartialUserPayload] = Body(...,discriminator='model_type'))-> None:
        if data.model_type == 'partial_user':
            self._update_partialUser(data) # type: ignore
        elif data.model_type == 'user':
            self._update_fullUser(data) # type: ignore
        
    def __repr__(self) -> str:
        return (
            f"<BaseUser id={self.id} name={self.name!r} global_name={self.global_name!r}"
            f" bot={self.bot} system={self.system}>"
        )

    def __str__(self) -> str:
        if self.discriminator == '0':
            return self.name
        return f'{self.name}#{self.discriminator}'

    def __eq__(self, other: object) -> bool:
        return  isinstance(other, User) and self.id == other.id
        
    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
    
    def _update_partialUser(self, data: 'PartialUserPayload') -> None:
        """Update the user instance with partial data."""
        self.id = data.id
        self.name = data.username
        self.discriminator = data.discriminator
        self.global_name = data.global_name
        self.avatar = data.avatar
        self.avatar_decoration_data = data.avatar_decoration_data

    def _update_fullUser(self, data: 'UserPayload') -> None:
        """Update the user instance with new data."""
        self.id = data.id
        self.name = data.username
        self.discriminator = data.discriminator
        self.global_name = data.global_name
        self.avatar = data.avatar
        self.avatar_decoration_data = data.avatar_decoration_data
        self.mfa_enabled = data.mfa_enabled
        self.locale = data.locale
        self.verified = data.verified
        self.email = data.email
        self.flags = data.flags
        self.premium_type = data.premium_type
        self.bot = data.bot
        self.system = data.system
        self._avatar = data.avatar
        self._public_flags = data.public_flags
    
    @property
    def display_name(self) -> str:
        """:class:`str`: Returns the user's display name.

        For regular users this is just their global name or their username,
        but if they have a guild specific nickname then that
        is returned instead.
        """
        if self.global_name:
            return self.global_name
        return self.name
    
    @property
    def is_authenticated(self) -> bool:
        """Check if the user is authenticated."""
        return self.id is not None

# class ClientUser(User):
   
    
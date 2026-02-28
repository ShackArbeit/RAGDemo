from fastapi import Depends, HTTPException
from .auth import User, get_current_user

def require_role(*allowed: str):
    def _dep(user: User = Depends(get_current_user)) -> User:
        if not set(user.roles).intersection(set(allowed)):
            raise HTTPException(status_code=403, detail=f"Need role in {allowed}")
        return user
    return _dep
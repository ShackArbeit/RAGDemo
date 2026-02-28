from fastapi import Depends, HTTPException
from .auth import User, get_current_user

def get_tenant(user: User = Depends(get_current_user)) -> str:
    if not user.tenant:
        raise HTTPException(status_code=403, detail="Tenant missing")
    return user.tenant
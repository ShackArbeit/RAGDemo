from jose import jwt, JWTError
from fastapi import Header, HTTPException
from pydantic import BaseModel
from .config import settings

ALGO = "HS256"

class User(BaseModel):
    sub: str
    name: str
    tenant: str
    roles: list[str]

def issue_dev_token(sub="u123", name="Shack", tenant="t1", roles=None):
    if roles is None:
        roles = ["viewer"]
    payload = {"sub": sub, "name": name, "tenant": tenant, "roles": roles}
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGO)

def get_current_user(authorization: str = Header(default="")) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    token = authorization.replace("Bearer ", "", 1).strip()
    try:
        data = jwt.decode(token, settings.jwt_secret, algorithms=[ALGO])
        return User(**data)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
from fastapi import HTTPException, Header, Depends
from typing import Optional, List
import os

# Simple In-Memory Role Config
ROLES = {
    "admin": ["run_agent", "view_metrics", "chat"],
    "user": ["chat"]
}

# Mock User DB
API_KEYS = {
    "sk-admin": {"user_id": "admin_user", "role": "admin"},
    "sk-user": {"user_id": "regular_user", "role": "user"}
}

def get_current_user(x_api_key: Optional[str] = Header(None)):
    """
    Validates API Key and returns user info.
    """
    # Allow bypass if no key set in dev (optional, but good for MVP)
    if not os.getenv("REQUIRE_AUTH", "false").lower() == "true":
        return {"user_id": "dev_user", "role": "admin"}
        
    if not x_api_key or x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
        
    return API_KEYS[x_api_key]

def require_role(role: str):
    def dependency(user: dict = Depends(get_current_user)):
        user_role = user.get("role", "guest")
        if user_role != role and user_role != "admin": # Admin superuser
             raise HTTPException(status_code=403, detail=f"Requires role: {role}")
        return user
    return dependency

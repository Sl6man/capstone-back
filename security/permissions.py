from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Optional

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY='e5bddc5ac6b78059204847592d3c26079eb505af91f31640ffa74a8a8d7f9dbd'
ALGORITHM='HS256'

PAGE_PERMISSIONS = {
    "team_page": {
        'admin': ['view','create','edit', 'delete'],
        'user': ['view']
    },
    'scraper_page': {
        "admin": ['view','create' ,'edit', 'delete'],
        'user': ['view', 'edit'],
    }
}

def has_permission(role: str, page: str, action: str) -> bool:
    """
    Checks if a user's role grants them permission to perform an action on a specific page.

    :param role: The role of the user (e.g., "admin", "user").
    :param page: The page where access is being checked (e.g., "team_page").
    :param action: The action the user wants to perform (e.g., "edit").
    :return: True if the user has permission, False otherwise.
    """
    allowed_actions = PAGE_PERMISSIONS.get(page, {}).get(role, [])
    return action in allowed_actions



def get_current_user_role(token: str = Depends(oauth2_scheme)) -> str:
    """
    Extracts the role_id from the JWT token.

    :param token: The JWT token from the request.
    :return: The role_id as a string.
    :raises HTTPException: If the token is invalid or does not contain a role_id.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role_id: Optional[str] = payload.get("role_id")

        if role_id is None:
            raise HTTPException(status_code=403, detail="Role not found in token")

        return role_id

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
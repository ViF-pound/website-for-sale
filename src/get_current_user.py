from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException
from fastapi.websockets import WebSocket

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.app_auth.auth_utils.utils import valid_access_token
from src.db import get_session
from src.models.user_model import User


bearer = HTTPBearer()


async def get_current_id(token: HTTPAuthorizationCredentials = Depends(bearer)):
    
    user_id = await valid_access_token(token=token.credentials)
    
    if not user_id:
            raise HTTPException(status_code=426, detail={"token":"Your token is not valid"})
            
    return user_id


async def get_current_user(user_id = Depends(get_current_id), session: AsyncSession = Depends(get_session)):
    
    user = await session.scalar(select(User).options(selectinload(User.seller), selectinload(User.backet)).where(User.id == user_id))
    
    if not user:
            raise HTTPException(status_code=426, detail={"token":"Your token is not valid"})

    return user


async def get_current_confirm_seller(user: User = Depends(get_current_user)):
    
    if not user.profile:
        raise HTTPException(status_code=426, detail={"token":"You have not profile"})
        
    if not user.profile.is_confirmed:
        raise HTTPException(status_code=426, detail={"token":"You have not confirmed your profile"})
        
    return user


async def get_current_user_ws(websocket: WebSocket, session: AsyncSession = Depends(get_session)):

    try:

        token = websocket.headers.get('authorization').split(' ')[1]
        user_id = await valid_access_token(token=token)
        
        if not user_id:
            await websocket.close(code=4001, reason="Invalid token")
            return None
            
        user = await session.scalar(
            select(User)
            .options(selectinload(User.profile), selectinload(User.backet))
            .where(User.id == user_id)
        )
        
        if not user:
            await websocket.close(code=4001, reason="User not found")
            return None
            
        return user
        
    except Exception:
        await websocket.close(code=4001, reason="Authentication failed")
        return None
    
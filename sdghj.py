user = await session.scalar(select(User).where(User.user_name == data_user.user_name))
    if user:
        raise HTTPException(status_code=400, detail="this name busy")
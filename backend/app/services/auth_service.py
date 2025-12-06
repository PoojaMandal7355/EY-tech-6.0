"""Authentication service"""
from datetime import timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.schemas.user import UserCreate, TokenResponse


class AuthService:
    """Service for handling authentication operations"""
    
    @staticmethod
    async def register(session: AsyncSession, user_create: UserCreate) -> User:
        """
        Register a new user.
        
        Args:
            session: Database session
            user_create: User creation schema
            
        Returns:
            Created user
            
        Raises:
            ValueError: If email already exists
        """
        # Check if email already exists
        result = await session.execute(
            select(User).where(User.email == user_create.email)
        )
        if result.scalar_one_or_none():
            raise ValueError(f"Email {user_create.email} already registered")
        
        # Create new user
        db_user = User(
            email=user_create.email,
            hashed_password=hash_password(user_create.password),
            full_name=user_create.full_name,
            role=user_create.role,
        )
        
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        
        return db_user
    
    @staticmethod
    async def login(session: AsyncSession, email: str, password: str) -> TokenResponse | None:
        """
        Authenticate user and return tokens.
        
        Args:
            session: Database session
            email: User email
            password: User password
            
        Returns:
            Token response or None if authentication fails
        """
        # Find user by email
        result = await session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        # Create tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    
    @staticmethod
    async def refresh_access_token(session: AsyncSession, refresh_token: str) -> TokenResponse | None:
        """
        Refresh access token using refresh token.
        
        Args:
            session: Database session
            refresh_token: Refresh token
            
        Returns:
            New token response or None if invalid
        """
        from app.core.security import decode_token
        
        payload = decode_token(refresh_token)
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        try:
            user_id_int = int(user_id)
        except (ValueError, TypeError):
            return None
        
        # Verify user exists and is active
        result = await session.execute(
            select(User).where(User.id == user_id_int)
        )
        user = result.scalar_one_or_none()
        
        if not user or not user.is_active:
            return None
        
        # Create new access token
        new_access_token = create_access_token(data={"sub": str(user.id)})
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=refresh_token,
        )

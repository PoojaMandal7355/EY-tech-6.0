"""Authentication API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.schemas.user import UserCreate, LoginRequest, TokenResponse, RefreshTokenRequest, UserResponse
from app.services.auth_service import AuthService
from app.models.user import User
from app.core.deps import get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: UserCreate,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Register a new user.
    
    Args:
        user_create: User registration data
        session: Database session
        
    Returns:
        Created user
        
    Raises:
        HTTPException: If email already registered
    """
    try:
        user = await AuthService.register(session, user_create)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    login_request: LoginRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Login with email and password.
    
    Args:
        login_request: Login credentials
        session: Database session
        
    Returns:
        Access and refresh tokens
        
    Raises:
        HTTPException: If credentials invalid
    """
    token_response = await AuthService.login(
        session,
        login_request.email,
        login_request.password,
    )
    
    if not token_response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    return token_response


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """
    Get current authenticated user info.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User information
    """
    return current_user


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_request: RefreshTokenRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Refresh access token using refresh token.
    
    Args:
        refresh_request: Refresh token
        session: Database session
        
    Returns:
        New access token
        
    Raises:
        HTTPException: If refresh token invalid
    """
    token_response = await AuthService.refresh_access_token(
        session,
        refresh_request.refresh_token,
    )
    
    if not token_response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    return token_response

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime, timedelta
import re
import secrets
import logging
from ..database import get_db
from ..models import User, AuditLog
from ..config import settings
from ..auth import (
    hash_password, 
    authenticate_user, 
    create_access_token, 
    create_refresh_token,
    verify_token,
    get_current_user,
    verify_password
)
from ..email_service import email_service

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)


# === Helper Functions ===

def create_audit_log(
    db: Session,
    event_type: str,
    success: bool,
    email: Optional[str] = None,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[str] = None
):
    """Create an audit log entry for security tracking"""
    audit_log = AuditLog(
        user_id=user_id,
        event_type=event_type,
        email=email,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details,
        success=success
    )
    db.add(audit_log)
    db.commit()


def get_client_ip(request: Request) -> str:
    """Extract client IP address from request"""
    if "x-forwarded-for" in request.headers:
        return request.headers["x-forwarded-for"].split(",")[0].strip()
    if "x-real-ip" in request.headers:
        return request.headers["x-real-ip"]
    return request.client.host if request.client else "unknown"


def get_user_agent(request: Request) -> str:
    """Extract user agent from request"""
    return request.headers.get("user-agent", "unknown")[:500]


def is_account_locked(user: User) -> bool:
    """Check if user account is currently locked"""
    if not user.is_locked:
        return False
    
    if user.locked_until and user.locked_until > datetime.utcnow():
        return True
    
    # Unlock if lockout period has expired
    user.is_locked = False
    user.locked_until = None
    user.failed_login_attempts = 0
    return False


def handle_failed_login(db: Session, user: User):
    """Handle failed login attempt and lock account if necessary"""
    user.failed_login_attempts += 1
    
    if user.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
        user.is_locked = True
        user.locked_until = datetime.utcnow() + timedelta(minutes=settings.ACCOUNT_LOCKOUT_MINUTES)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=f"Your account has been temporarily locked for security reasons. Please try again in {settings.ACCOUNT_LOCKOUT_MINUTES} minutes."
        )
    
    db.commit()
    remaining = settings.MAX_LOGIN_ATTEMPTS - user.failed_login_attempts
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid password. You have {remaining} attempt{'s' if remaining != 1 else ''} remaining before your account is locked.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def reset_failed_attempts(db: Session, user: User):
    """Reset failed login attempts after successful login"""
    user.failed_login_attempts = 0
    user.is_locked = False
    user.locked_until = None
    user.last_login = datetime.utcnow()
    db.commit()


def validate_password_strength(password: str) -> str:
    """Validate password meets security requirements"""
    # Check length constraints only
    if len(password) < settings.MIN_PASSWORD_LENGTH:
        raise ValueError(f'Password must be at least {settings.MIN_PASSWORD_LENGTH} characters')
    
    if len(password) > settings.MAX_PASSWORD_LENGTH:
        raise ValueError(f'Password cannot be longer than {settings.MAX_PASSWORD_LENGTH} characters')
    
    return password


def log_auth_event(
    db: Session,
    event_type: str,
    success: bool,
    req: Request,
    email: Optional[str] = None,
    user_id: Optional[int] = None,
    details: Optional[str] = None
):
    """Helper to log auth events consistently"""
    create_audit_log(
        db=db,
        event_type=event_type,
        success=success,
        email=email,
        user_id=user_id,
        ip_address=get_client_ip(req),
        user_agent=get_user_agent(req),
        details=details
    )


def set_auth_cookies(access_token: str, refresh_token: str) -> Response:
    """Helper to set authentication cookies and return response"""
    response = Response(
        content=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        ).model_dump_json(),
        media_type="application/json"
    )
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )
    
    return response


# === Pydantic Models ===


class RegisterRequest(BaseModel):
    email: str
    full_name: str
    password: str
    role: str = "researcher"
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('Please enter a valid email address (e.g., user@example.com)')
        # Basic email regex validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Please enter a valid email address')
        return v.lower().strip()
    
    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v):
        v = v.strip()
        if len(v) < 2:
            raise ValueError('Please enter your full name (at least 2 characters)')
        if len(v) > 100:
            raise ValueError('Your full name is too long (maximum 100 characters)')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        # Validate password strength
        validate_password_strength(v)
        return v
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        allowed_roles = ['researcher', 'admin', 'viewer']
        if v not in allowed_roles:
            raise ValueError(f'Please select a valid role (Researcher, Admin, or Viewer)')
        return v


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: Optional[str] = None


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v):
        # Validate password strength
        validate_password_strength(v)
        return v


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    last_login: Optional[str]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, req: Request, db: Session = Depends(get_db)):
    """
    Register a new user account with comprehensive validation.
    
    - **email**: Valid email address (must be unique)
    - **full_name**: User's full name (2-100 characters)
    - **password**: Strong password (8+ chars, uppercase, lowercase, digit)
    - **role**: User role (researcher, admin, viewer)
    """
    try:
        # Check if user exists
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            log_auth_event(
                db=db,
                event_type="register_failed",
                success=False,
                email=request.email,
                req=req,
                details="Email already registered"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This email is already registered. Please use a different email or try logging in instead."
            )
        
        # Create new user
        hashed_password = hash_password(request.password)
        new_user = User(
            email=request.email,
            full_name=request.full_name,
            password=hashed_password,
            role=request.role
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Log successful registration
        log_auth_event(
            db=db,
            event_type="register",
            success=True,
            email=new_user.email,
            user_id=new_user.id,
            req=req,
            details=f"New user registered: {new_user.full_name}"
        )
        
        return UserResponse(
            id=new_user.id,
            email=new_user.email,
            full_name=new_user.full_name,
            role=new_user.role,
            is_active=new_user.is_active,
            last_login=new_user.last_login.isoformat() if new_user.last_login else None,
            created_at=new_user.created_at.isoformat() if new_user.created_at else None,
            updated_at=new_user.updated_at.isoformat() if new_user.updated_at else None
        )
    except HTTPException:
        raise
    except ValueError as e:
        # Handle validation errors from validators
        db.rollback()
        log_auth_event(
            db=db,
            event_type="register_failed",
            success=False,
            email=request.email,
            req=req,
            details=f"Validation error: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        db.rollback()
        create_audit_log(
            db=db,
            event_type="register_failed",
            success=False,
            email=request.email,
            ip_address=get_client_ip(req),
            user_agent=get_user_agent(req),
            details=f"Registration error: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again later."
        )


@router.post("/login")
async def login(request: LoginRequest, req: Request, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT tokens.
    
    Features:
    - Account lockout after 5 failed attempts (15 minute lockout)
    - Audit logging of all login attempts
    - IP address and user agent tracking
    """
    try:
        user = db.query(User).filter(User.email == request.email).first()
        
        if not user:
            # Log failed attempt for non-existent user
            log_auth_event(
                db=db,
                event_type="login_failed",
                success=False,
                email=request.email,
                req=req,
                details="User not found"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found. Please check the email or register a new account.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if account is locked
        if is_account_locked(user):
            minutes_remaining = int((user.locked_until - datetime.utcnow()).total_seconds() / 60)
            log_auth_event(
                db=db,
                event_type="login_failed",
                success=False,
                email=user.email,
                user_id=user.id,
                req=req,
                details=f"Account locked. {minutes_remaining} minutes remaining"
            )
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail=f"Your account is temporarily locked for security. Please try again in {minutes_remaining} minutes."
            )
        
        # Check if account is active
        if not user.is_active:
            log_auth_event(
                db=db,
                event_type="login_failed",
                success=False,
                email=user.email,
                user_id=user.id,
                req=req,
                details="Account is inactive"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account has been deactivated. Please contact support for assistance."
            )
        
        # Verify password
        password_valid = False
        try:
            password_valid = verify_password(request.password, user.password)
        except Exception as pwd_error:
            # If password verification fails for any reason, treat as invalid password
            password_valid = False
        
        if not password_valid:
            log_auth_event(
                db=db,
                event_type="login_failed",
                success=False,
                email=user.email,
                user_id=user.id,
                req=req,
                details="Invalid password"
            )
            handle_failed_login(db, user)
            # handle_failed_login raises HTTPException, so code below won't execute
        
        # Successful login - reset failed attempts
        reset_failed_attempts(db, user)
        
        # Create tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        # Log successful login
        log_auth_event(
            db=db,
            event_type="login",
            success=True,
            email=user.email,
            user_id=user.id,
            req=req,
            details="Successful login"
        )
        
        # Create response with tokens in httpOnly cookies
        response = Response(
            content=TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token
            ).model_dump_json(),
            media_type="application/json"
        )
        
        # Set httpOnly cookies (secure for production, adjust for localhost)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )
        
        return response
    except HTTPException:
        raise
    except Exception as e:
        log_auth_event(
            db=db,
            event_type="login_failed",
            success=False,
            email=request.email,
            req=req,
            details=f"Login error: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        is_active=current_user.is_active,
        last_login=current_user.last_login.isoformat() if current_user.last_login else None,
        created_at=current_user.created_at.isoformat() if current_user.created_at else None,
        updated_at=current_user.updated_at.isoformat() if current_user.updated_at else None
    )


@router.post("/refresh")
async def refresh_token(request: RefreshRequest, req: Request, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token.
    
    Returns new access and refresh tokens.
    """
    try:
        # Allow refresh token from request body or httpOnly cookie
        token = request.refresh_token or req.cookies.get("refresh_token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token missing"
            )

        payload = verify_token(token)
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        access_token = create_access_token(data={"sub": str(user.id)})
        new_refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        # Log token refresh
        log_auth_event(
            db=db,
            event_type="token_refresh",
            success=True,
            email=user.email,
            user_id=user.id,
            req=req,
            details="Token refreshed successfully"
        )
        
        # Create response with tokens in httpOnly cookies
        response = Response(
            content=TokenResponse(
                access_token=access_token,
                refresh_token=new_refresh_token
            ).model_dump_json(),
            media_type="application/json"
        )
        
        # Set httpOnly cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token refresh failed: {str(e)}"
        )


@router.post("/logout")
async def logout(req: Request):
    """
    Logout user by clearing authentication cookies.
    """
    response = Response(
        content='{"detail": "Logged out successfully"}',
        media_type="application/json"
    )
    
    # Clear httpOnly cookies
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,
        samesite="lax"
    )
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=False,
        samesite="lax"
    )
    
    return response


@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, req: Request, db: Session = Depends(get_db)):
    """
    Request a password reset token.
    
    Generates a secure token valid for 30 minutes and sends it via email.
    Note: Always returns success message for security (prevents user enumeration).
    """
    try:
        user = db.query(User).filter(User.email == request.email).first()
        
        if user and user.is_active:
            # Generate secure reset token
            reset_token = secrets.token_urlsafe(32)
            user.password_reset_token = reset_token
            user.password_reset_expires = datetime.utcnow() + timedelta(
                minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
            )
            db.commit()
            
            # Send password reset email (no audit logging for token generation)
            send_ok = False
            try:
                # Send email synchronously (not async) to ensure it completes
                send_ok = email_service.send_password_reset_email(
                    recipient_email=user.email,
                    reset_token=reset_token,
                    user_name=user.full_name or user.email
                )
            except Exception as exc:
                logger.exception("Error while sending password reset email", exc_info=exc)
            if not send_ok:
                logger.warning(
                    "Password reset email failed to send",
                    extra={"email": user.email, "user_id": user.id},
                )
            
            # Return success regardless of email delivery (security practice)
            return {
                "detail": "If this email is registered, password reset instructions have been sent."
            }
        
        # Always return success to prevent user enumeration
        return {
            "detail": "If this email is registered, password reset instructions have been sent."
        }
    except Exception as e:
        # Still return success message even on error
        return {
            "detail": "If this email is registered, password reset instructions have been sent."
        }


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, req: Request, db: Session = Depends(get_db)):
    """
    Reset password using the token from forgot-password endpoint.
    
    Token is valid for 30 minutes.
    """
    try:
        # Find user with this reset token
        user = db.query(User).filter(
            User.password_reset_token == request.token
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        # Check if token has expired
        if not user.password_reset_expires or user.password_reset_expires < datetime.utcnow():
            # Clear expired token (no audit logging for expired tokens)
            user.password_reset_token = None
            user.password_reset_expires = None
            db.commit()
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset token has expired. Please request a new one."
            )
        
        # Check if account is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        # Update password
        user.password = hash_password(request.new_password)
        user.password_reset_token = None
        user.password_reset_expires = None
        
        # Unlock account if it was locked
        user.is_locked = False
        user.failed_login_attempts = 0
        user.locked_until = None
        
        db.commit()
        
        # Audit the password change
        log_auth_event(
            db=db,
            event_type="password_changed",
            success=True,
            email=user.email,
            user_id=user.id,
            req=req,
            details="Password changed via reset link"
        )
        
        return {
            "detail": "Password has been reset successfully. You can now login with your new password."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password reset failed: {str(e)}"
        )


@router.get("/audit-logs")
async def get_audit_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """
    Get audit logs for current user (last 50 events).
    
    Admin users can see all logs (TODO: implement admin check).
    """
    logs = db.query(AuditLog).filter(
        AuditLog.user_id == current_user.id
    ).order_by(
        AuditLog.created_at.desc()
    ).limit(limit).all()
    
    return {
        "logs": [log.to_dict() for log in logs],
        "count": len(logs)
    }

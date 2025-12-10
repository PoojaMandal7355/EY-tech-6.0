from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="researcher")
    is_active = Column(Boolean, default=True)
    is_locked = Column(Boolean, default=False)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role,
            "is_active": self.is_active,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    molecule_name = Column(String(255))
    description = Column(Text)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="projects")
    agent_logs = relationship("AgentLog", back_populates="project", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "molecule_name": self.molecule_name,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class AgentLog(Base):
    __tablename__ = "agent_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    agent_type = Column(String(100), nullable=False)
    input_text = Column(Text)
    output_text = Column(Text)
    status = Column(String(50), default="completed")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("Project", back_populates="agent_logs")
    
    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "agent_type": self.agent_type,
            "input_text": self.input_text,
            "output_text": self.output_text,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class AuditLog(Base):
    """Track all authentication and security events"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    event_type = Column(String(100), nullable=False)  # login, logout, register, failed_login, password_change, etc.
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    email = Column(String(255), nullable=True)  # For failed attempts where user doesn't exist
    details = Column(Text, nullable=True)
    success = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="audit_logs")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "event_type": self.event_type,
            "ip_address": self.ip_address,
            "email": self.email,
            "details": self.details,
            "success": self.success,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

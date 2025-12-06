"""Project and ResearchSession database models"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Project(Base):
    """Project model for pharmaceutical research projects"""
    
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    molecule_name = Column(String(255), nullable=True)
    indication = Column(String(255), nullable=True)
    status = Column(String(50), default="active", nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name={self.name}, molecule_name={self.molecule_name})>"


class ResearchSession(Base):
    """ResearchSession model for tracking AI agent sessions within projects"""
    
    __tablename__ = "research_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self) -> str:
        return f"<ResearchSession(id={self.id}, project_id={self.project_id}, name={self.name})>"

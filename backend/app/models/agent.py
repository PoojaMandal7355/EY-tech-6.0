"""Agent and AgentRequest database models"""
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from app.core.database import Base


class AgentType(str, Enum):
    """Enum for AI agent types"""
    
    RESEARCH = "research"
    MARKET_INTELLIGENCE = "market_intelligence"
    FORMULATION = "formulation"
    SAFETY = "safety"
    REGULATORY = "regulatory"
    COMPETITIVE_INTELLIGENCE = "competitive_intelligence"
    MEDICAL_WRITING = "medical_writing"
    PATENT_IP = "patent_ip"


class AgentRequest(Base):
    """AgentRequest model for tracking AI agent executions"""
    
    __tablename__ = "agent_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("research_sessions.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    agent_type = Column(SQLEnum(AgentType), nullable=False, index=True)
    input_data = Column(Text, nullable=False)
    output_data = Column(Text, nullable=True)
    status = Column(String(50), default="pending", nullable=False)
    tokens_used = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self) -> str:
        return f"<AgentRequest(id={self.id}, session_id={self.session_id}, agent_type={self.agent_type}, status={self.status})>"

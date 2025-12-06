"""Agent request/response schemas"""
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class AgentTypeEnum(str, Enum):
    """Agent type enumeration"""
    RESEARCH = "research"
    MARKET_INTELLIGENCE = "market_intelligence"
    FORMULATION = "formulation"
    SAFETY = "safety"
    REGULATORY = "regulatory"
    COMPETITIVE_INTELLIGENCE = "competitive_intelligence"
    MEDICAL_WRITING = "medical_writing"
    PATENT_IP = "patent_ip"


class AgentExecuteRequest(BaseModel):
    """Schema for executing an agent"""
    session_id: int = Field(..., description="Research session ID")
    input: dict = Field(..., description="Input data for the agent")


class AgentRequestResponse(BaseModel):
    """Schema for agent request response"""
    id: int = Field(..., description="Request ID")
    session_id: int = Field(..., description="Session ID")
    user_id: int = Field(..., description="User ID")
    agent_type: AgentTypeEnum = Field(..., description="Agent type")
    input_data: str = Field(..., description="Input data")
    output_data: str | None = Field(None, description="Output data")
    status: str = Field(..., description="Request status")
    tokens_used: int = Field(default=0, description="Tokens used")
    created_at: datetime = Field(..., description="Request creation timestamp")
    
    class Config:
        from_attributes = True


class AgentHistoryResponse(BaseModel):
    """Schema for agent request history"""
    total: int = Field(..., description="Total requests")
    requests: list[AgentRequestResponse] = Field(..., description="List of requests")

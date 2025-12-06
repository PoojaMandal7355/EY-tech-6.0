"""Project request/response schemas"""
from datetime import datetime
from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    """Base project schema"""
    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    description: str | None = Field(None, description="Project description")
    molecule_name: str | None = Field(None, max_length=255, description="Molecule name")
    indication: str | None = Field(None, max_length=255, description="Medical indication")
    status: str = Field(default="active", description="Project status")


class ProjectCreate(ProjectBase):
    """Schema for creating a project"""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project"""
    name: str | None = Field(None, max_length=255, description="Project name")
    description: str | None = Field(None, description="Project description")
    molecule_name: str | None = Field(None, max_length=255, description="Molecule name")
    indication: str | None = Field(None, max_length=255, description="Medical indication")
    status: str | None = Field(None, description="Project status")


class ProjectResponse(ProjectBase):
    """Schema for project response"""
    id: int = Field(..., description="Project ID")
    owner_id: int = Field(..., description="Project owner ID")
    created_at: datetime = Field(..., description="Project creation timestamp")
    updated_at: datetime = Field(..., description="Project update timestamp")
    
    class Config:
        from_attributes = True


class ResearchSessionResponse(BaseModel):
    """Schema for research session response"""
    id: int = Field(..., description="Session ID")
    project_id: int = Field(..., description="Project ID")
    name: str = Field(..., description="Session name")
    created_at: datetime = Field(..., description="Session creation timestamp")
    
    class Config:
        from_attributes = True

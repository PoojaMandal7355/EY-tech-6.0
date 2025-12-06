"""Document request/response schemas"""
from datetime import datetime
from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    """Schema for document response"""
    id: int = Field(..., description="Document ID")
    project_id: int = Field(..., description="Project ID")
    file_name: str = Field(..., description="File name")
    file_path: str = Field(..., description="File path")
    file_type: str = Field(..., description="File type")
    file_size: int = Field(..., description="File size in bytes")
    uploaded_by: int = Field(..., description="User ID who uploaded")
    created_at: datetime = Field(..., description="Upload timestamp")
    
    class Config:
        from_attributes = True


class DocumentUploadResponse(BaseModel):
    """Schema for document upload response"""
    id: int = Field(..., description="Document ID")
    message: str = Field(..., description="Success message")
    file_name: str = Field(..., description="File name")
    file_size: int = Field(..., description="File size")

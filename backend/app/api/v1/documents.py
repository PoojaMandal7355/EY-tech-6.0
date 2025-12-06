"""Documents API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db_session
from app.core.deps import get_current_user
from app.models.user import User
from app.models.document import Document
from app.models.project import Project
from app.schemas.document import DocumentResponse, DocumentUploadResponse
from app.services.project_service import ProjectService
from app.utils.file_handler import FileHandler

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    project_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Upload a document to a project.
    
    Args:
        project_id: Project ID
        file: File to upload
        current_user: Current authenticated user
        session: Database session
        
    Returns:
        Document upload response
        
    Raises:
        HTTPException: If project not found, file too large, or user not authorized
    """
    # Verify project exists and user is owner
    project = await ProjectService.get_project(session, project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to upload to this project",
        )
    
    try:
        # Save file to disk
        file_path, file_size = await FileHandler.save_upload_file(
            file,
            f"project_{project_id}",
        )
        
        file_type = FileHandler.get_file_type(file.filename)
        
        # Create document record
        document = Document(
            project_id=project_id,
            file_name=file.filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            uploaded_by=current_user.id,
        )
        
        session.add(document)
        await session.commit()
        await session.refresh(document)
        
        return DocumentUploadResponse(
            id=document.id,
            message="File uploaded successfully",
            file_name=document.file_name,
            file_size=document.file_size,
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}",
        )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Get document details.
    
    Args:
        document_id: Document ID
        current_user: Current authenticated user
        session: Database session
        
    Returns:
        Document details
        
    Raises:
        HTTPException: If document not found or user not authorized
    """
    result = await session.execute(
        select(Document).where(Document.id == document_id)
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    
    # Check if user has access to the project
    project = await ProjectService.get_project(session, document.project_id)
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this document",
        )
    
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Delete a document.
    
    Args:
        document_id: Document ID
        current_user: Current authenticated user
        session: Database session
        
    Raises:
        HTTPException: If document not found or user not authorized
    """
    result = await session.execute(
        select(Document).where(Document.id == document_id)
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    
    # Check if user has access
    project = await ProjectService.get_project(session, document.project_id)
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this document",
        )
    
    # Delete file from disk
    try:
        FileHandler.delete_file(document.file_path)
    except FileNotFoundError:
        pass  # File already deleted
    
    # Delete from database
    await session.delete(document)
    await session.commit()

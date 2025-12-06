"""Projects API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ResearchSessionResponse
from app.services.project_service import ProjectService

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_create: ProjectCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Create a new project.
    
    Args:
        project_create: Project creation data
        current_user: Current authenticated user
        session: Database session
        
    Returns:
        Created project
    """
    project = await ProjectService.create_project(
        session,
        project_create,
        current_user.id,
    )
    return project


@router.get("", response_model=list[ProjectResponse])
async def get_projects(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Get all projects for current user.
    
    Args:
        current_user: Current authenticated user
        session: Database session
        
    Returns:
        List of user's projects
    """
    projects = await ProjectService.get_user_projects(session, current_user.id)
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Get a specific project.
    
    Args:
        project_id: Project ID
        current_user: Current authenticated user
        session: Database session
        
    Returns:
        Project details
        
    Raises:
        HTTPException: If project not found or user not owner
    """
    project = await ProjectService.get_project(session, project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this project",
        )
    
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Update a project.
    
    Args:
        project_id: Project ID
        project_update: Project update data
        current_user: Current authenticated user
        session: Database session
        
    Returns:
        Updated project
        
    Raises:
        HTTPException: If project not found or user not owner
    """
    project = await ProjectService.get_project(session, project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this project",
        )
    
    updated_project = await ProjectService.update_project(
        session,
        project,
        project_update,
    )
    return updated_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Delete a project.
    
    Args:
        project_id: Project ID
        current_user: Current authenticated user
        session: Database session
        
    Raises:
        HTTPException: If project not found or user not owner
    """
    project = await ProjectService.get_project(session, project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this project",
        )
    
    await ProjectService.delete_project(session, project)


@router.post("/{project_id}/sessions", response_model=ResearchSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_research_session(
    project_id: int,
    session_name: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Create a research session for a project.
    
    Args:
        project_id: Project ID
        session_name: Session name
        current_user: Current authenticated user
        session: Database session
        
    Returns:
        Created research session
        
    Raises:
        HTTPException: If project not found or user not owner
    """
    project = await ProjectService.get_project(session, project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create sessions for this project",
        )
    
    research_session = await ProjectService.create_research_session(
        session,
        project_id,
        session_name,
    )
    return research_session

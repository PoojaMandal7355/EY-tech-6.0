"""Project service"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.project import Project, ResearchSession
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    """Service for handling project operations"""
    
    @staticmethod
    async def create_project(
        session: AsyncSession,
        project_create: ProjectCreate,
        owner_id: int,
    ) -> Project:
        """
        Create a new project.
        
        Args:
            session: Database session
            project_create: Project creation schema
            owner_id: ID of project owner
            
        Returns:
            Created project
        """
        db_project = Project(
            name=project_create.name,
            description=project_create.description,
            molecule_name=project_create.molecule_name,
            indication=project_create.indication,
            status=project_create.status,
            owner_id=owner_id,
        )
        
        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)
        
        return db_project
    
    @staticmethod
    async def get_project(session: AsyncSession, project_id: int) -> Project | None:
        """
        Get a project by ID.
        
        Args:
            session: Database session
            project_id: Project ID
            
        Returns:
            Project or None if not found
        """
        result = await session.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_projects(session: AsyncSession, owner_id: int) -> list[Project]:
        """
        Get all projects owned by a user.
        
        Args:
            session: Database session
            owner_id: User ID
            
        Returns:
            List of projects
        """
        result = await session.execute(
            select(Project).where(Project.owner_id == owner_id)
        )
        return result.scalars().all()
    
    @staticmethod
    async def update_project(
        session: AsyncSession,
        project: Project,
        project_update: ProjectUpdate,
    ) -> Project:
        """
        Update a project.
        
        Args:
            session: Database session
            project: Project to update
            project_update: Project update schema
            
        Returns:
            Updated project
        """
        update_data = project_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(project, field, value)
        
        await session.commit()
        await session.refresh(project)
        
        return project
    
    @staticmethod
    async def delete_project(session: AsyncSession, project: Project) -> None:
        """
        Delete a project.
        
        Args:
            session: Database session
            project: Project to delete
        """
        await session.delete(project)
        await session.commit()
    
    @staticmethod
    async def create_research_session(
        session: AsyncSession,
        project_id: int,
        name: str,
    ) -> ResearchSession:
        """
        Create a new research session.
        
        Args:
            session: Database session
            project_id: Project ID
            name: Session name
            
        Returns:
            Created research session
        """
        db_session = ResearchSession(
            project_id=project_id,
            name=name,
        )
        
        session.add(db_session)
        await session.commit()
        await session.refresh(db_session)
        
        return db_session

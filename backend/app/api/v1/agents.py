"""Agents API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.core.deps import get_current_user
from app.models.user import User
from app.models.agent import AgentType
from app.schemas.agent import AgentExecuteRequest, AgentRequestResponse, AgentHistoryResponse, AgentTypeEnum
from app.services.agent_service import AgentService

router = APIRouter(prefix="/api/v1/agents", tags=["agents"])


@router.post("/{agent_type}/execute", response_model=AgentRequestResponse, status_code=status.HTTP_201_CREATED)
async def execute_agent(
    agent_type: str,
    request: AgentExecuteRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Execute an AI agent for a research session.
    
    Args:
        agent_type: Type of agent to execute
        request: Agent execution request
        current_user: Current authenticated user
        session: Database session
        
    Returns:
        Agent request created
        
    Raises:
        HTTPException: If agent type invalid or session not found
    """
    # Validate agent type
    try:
        agent_type_enum = AgentType[agent_type.upper()]
    except KeyError:
        valid_types = [t.value for t in AgentType]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid agent type. Valid types: {valid_types}",
        )
    
    try:
        agent_request = await AgentService.execute_agent(
            session,
            agent_type_enum,
            request,
            current_user.id,
        )
        return agent_request
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/history", response_model=AgentHistoryResponse)
async def get_agent_history(
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Get agent execution history for current user.
    
    Args:
        limit: Maximum number of results
        offset: Pagination offset
        current_user: Current authenticated user
        session: Database session
        
    Returns:
        Agent request history
    """
    requests, total = await AgentService.get_user_agent_history(
        session,
        current_user.id,
        limit,
        offset,
    )
    
    return AgentHistoryResponse(
        total=total,
        requests=requests,
    )


@router.get("/{request_id}", response_model=AgentRequestResponse)
async def get_agent_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Get details of a specific agent request.
    
    Args:
        request_id: Agent request ID
        current_user: Current authenticated user
        session: Database session
        
    Returns:
        Agent request details
        
    Raises:
        HTTPException: If request not found or not authorized
    """
    agent_request = await AgentService.get_agent_request(session, request_id)
    
    if not agent_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent request not found",
        )
    
    if agent_request.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this request",
        )
    
    return agent_request

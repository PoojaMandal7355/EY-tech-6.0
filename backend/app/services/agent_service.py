"""Agent service"""
import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.agent import AgentRequest, AgentType
from app.models.project import ResearchSession
from app.schemas.agent import AgentExecuteRequest


class AgentService:
    """Service for handling agent operations"""
    
    @staticmethod
    async def execute_agent(
        session: AsyncSession,
        agent_type: AgentType,
        request: AgentExecuteRequest,
        user_id: int,
    ) -> AgentRequest:
        """
        Create an agent execution request.
        
        Args:
            session: Database session
            agent_type: Type of agent to execute
            request: Agent execution request
            user_id: User ID
            
        Returns:
            Created agent request
            
        Raises:
            ValueError: If session not found
        """
        # Verify session exists
        result = await session.execute(
            select(ResearchSession).where(ResearchSession.id == request.session_id)
        )
        research_session = result.scalar_one_or_none()
        
        if not research_session:
            raise ValueError(f"Research session {request.session_id} not found")
        
        # Create agent request
        db_request = AgentRequest(
            session_id=request.session_id,
            user_id=user_id,
            agent_type=agent_type,
            input_data=json.dumps(request.input),
            status="pending",
        )
        
        session.add(db_request)
        await session.commit()
        await session.refresh(db_request)
        
        return db_request
    
    @staticmethod
    async def get_agent_request(
        session: AsyncSession,
        request_id: int,
    ) -> AgentRequest | None:
        """
        Get an agent request by ID.
        
        Args:
            session: Database session
            request_id: Request ID
            
        Returns:
            Agent request or None if not found
        """
        result = await session.execute(
            select(AgentRequest).where(AgentRequest.id == request_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_agent_history(
        session: AsyncSession,
        user_id: int,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[AgentRequest], int]:
        """
        Get agent request history for a user.
        
        Args:
            session: Database session
            user_id: User ID
            limit: Maximum number of results
            offset: Pagination offset
            
        Returns:
            Tuple of (list of requests, total count)
        """
        # Get total count
        count_result = await session.execute(
            select(AgentRequest).where(AgentRequest.user_id == user_id)
        )
        total = len(count_result.scalars().all())
        
        # Get paginated results
        result = await session.execute(
            select(AgentRequest)
            .where(AgentRequest.user_id == user_id)
            .limit(limit)
            .offset(offset)
        )
        requests = result.scalars().all()
        
        return requests, total
    
    @staticmethod
    async def update_agent_request(
        session: AsyncSession,
        agent_request: AgentRequest,
        status: str,
        output_data: dict | None = None,
        tokens_used: int = 0,
    ) -> AgentRequest:
        """
        Update an agent request with results.
        
        Args:
            session: Database session
            agent_request: Agent request to update
            status: New status
            output_data: Output data from agent
            tokens_used: Tokens used
            
        Returns:
            Updated agent request
        """
        agent_request.status = status
        if output_data:
            agent_request.output_data = json.dumps(output_data)
        agent_request.tokens_used = tokens_used
        
        await session.commit()
        await session.refresh(agent_request)
        
        return agent_request

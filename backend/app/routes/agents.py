from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from ..database import get_db
from ..models import User, Project, AgentLog
from ..auth import get_current_user

router = APIRouter(prefix="/agents", tags=["AI Agents"])


class AgentExecuteRequest(BaseModel):
    project_id: int
    agent_type: str
    input_text: str

class AgentExecuteResponse(BaseModel):
    id: int
    project_id: int
    agent_type: str
    input_text: str
    output_text: str
    status: str
    created_at: str

class AgentLogResponse(BaseModel):
    id: int
    project_id: int
    agent_type: str
    input_text: str
    output_text: str
    status: str
    created_at: str


@router.post("/execute", response_model=AgentExecuteResponse)
async def execute_agent(
    request: AgentExecuteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(
        Project.id == request.project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    agent_log = AgentLog(
        project_id=request.project_id,
        agent_type=request.agent_type,
        input_text=request.input_text,
        output_text="Agent execution result will appear here",
        status="completed"
    )
    
    db.add(agent_log)
    db.commit()
    db.refresh(agent_log)
    
    return AgentExecuteResponse(**agent_log.to_dict())


@router.get("/logs", response_model=List[AgentLogResponse])
async def get_agent_logs(
    project_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(AgentLog).join(Project).filter(Project.user_id == current_user.id)
    
    if project_id:
        query = query.filter(AgentLog.project_id == project_id)
    
    logs = query.order_by(AgentLog.created_at.desc()).all()
    return [AgentLogResponse(**log.to_dict()) for log in logs]


@router.get("/logs/{log_id}", response_model=AgentLogResponse)
async def get_agent_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    log = db.query(AgentLog).join(Project).filter(
        AgentLog.id == log_id,
        Project.user_id == current_user.id
    ).first()
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent log not found"
        )
    
    return AgentLogResponse(**log.to_dict())

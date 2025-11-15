"""Test agents"""
import pytest
import asyncio


@pytest.mark.asyncio
async def test_partner_agent_initialization(partner_agent):
    """Test partner agent initialization"""
    assert partner_agent.name == "Alex"
    assert partner_agent.role == "partner"
    assert partner_agent.conversation_history == []


@pytest.mark.asyncio
async def test_partner_agent_think(partner_agent):
    """Test partner agent think method"""
    context = {
        "experiment_name": "Titration",
        "student_message": "I'm ready to start",
        "current_step": 1
    }
    response = await partner_agent.think(context)
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_mentor_agent_initialization(mentor_agent):
    """Test mentor agent initialization"""
    assert mentor_agent.name == "Dr. Silva"
    assert mentor_agent.role == "mentor"


@pytest.mark.asyncio
async def test_mentor_agent_think(mentor_agent):
    """Test mentor agent think method"""
    context = {
        "experiment_name": "Hooke's Law",
        "conversation_history": [
            {"sender": "Student", "content": "I measured the displacement"},
            {"sender": "Partner", "content": "Great!"}
        ],
        "student_progress": 0.5
    }
    response = await mentor_agent.think(context)
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_evaluator_agent_initialization(evaluator_agent):
    """Test evaluator agent initialization"""
    assert evaluator_agent.name == "Dr. Evaluator"
    assert evaluator_agent.role == "evaluator"


@pytest.mark.asyncio
async def test_agent_conversation_history(partner_agent):
    """Test agent conversation history"""
    from src.agents.base import AgentMessage
    
    msg = AgentMessage(
        sender="Test",
        content="Test message",
        role="test"
    )
    partner_agent.add_to_history(msg)
    assert len(partner_agent.conversation_history) == 1
    assert partner_agent.get_history()[0].content == "Test message"


@pytest.mark.asyncio
async def test_agent_clear_history(mentor_agent):
    """Test clearing agent history"""
    from src.agents.base import AgentMessage
    
    msg = AgentMessage(
        sender="Test",
        content="Message 1",
        role="test"
    )
    mentor_agent.add_to_history(msg)
    assert len(mentor_agent.conversation_history) == 1
    
    mentor_agent.clear_history()
    assert len(mentor_agent.conversation_history) == 0

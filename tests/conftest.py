"""Test fixtures and conftest"""
import pytest
from fastapi.testclient import TestClient
from src.agents import PartnerAgent, MentorAgent, EvaluatorAgent
from src.scenarios import get_scenario


@pytest.fixture
def client():
    """FastAPI test client"""
    from app import app
    return TestClient(app)


@pytest.fixture
def partner_agent():
    """Partner agent fixture"""
    return PartnerAgent()


@pytest.fixture
def mentor_agent():
    """Mentor agent fixture"""
    return MentorAgent()


@pytest.fixture
def evaluator_agent():
    """Evaluator agent fixture"""
    return EvaluatorAgent()


@pytest.fixture
def titration_scenario():
    """Titration scenario fixture"""
    return get_scenario("acid_base_titration")


@pytest.fixture
def hookes_law_scenario():
    """Hooke's law scenario fixture"""
    return get_scenario("hookes_law")


@pytest.fixture
def osmosis_scenario():
    """Osmosis scenario fixture"""
    return get_scenario("osmosis")

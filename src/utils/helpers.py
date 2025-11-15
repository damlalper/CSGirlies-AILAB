"""Utilities for CSGirlies-AILAB"""

from typing import Dict, Any
from datetime import datetime
import json


def format_experiment_data(experiment_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Format experiment data for storage/transmission"""
    return {
        "experiment_id": experiment_id,
        "timestamp": datetime.now().isoformat(),
        "data": data
    }


def parse_student_response(response_text: str) -> Dict[str, Any]:
    """Parse and validate student response"""
    return {
        "raw_response": response_text,
        "parsed": response_text,
        "valid": True
    }


def generate_session_id() -> str:
    """Generate unique session ID"""
    from uuid import uuid4
    return str(uuid4())

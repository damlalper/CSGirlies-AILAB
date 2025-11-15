"""Main FastAPI application for CSGirlies-AILAB"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from src.config import settings
from src.agents import PartnerAgent, MentorAgent, EvaluatorAgent
from src.scenarios import get_scenario, list_scenarios
from src.wolfram_engine import wolfram_engine
from src.integrations import gitbook_integration
from src.utils import generate_session_id
import logging

# Configure logging
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CSGirlies-AILAB",
    description="AI Simulated Lab Partner - Multi-agent educational experiment simulation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


# Initialize agents
partner_agent = PartnerAgent()
mentor_agent = MentorAgent()
evaluator_agent = EvaluatorAgent()

# Request/Response models
class StartExperimentRequest(BaseModel):
    """Request to start an experiment"""
    experiment_id: str
    level: Optional[str] = "beginner"
    student_name: Optional[str] = "Student"


class StudentInputRequest(BaseModel):
    """Student input during experiment"""
    session_id: str
    experiment_id: str
    student_message: str
    current_step: Optional[int] = 1


class ExperimentResponse(BaseModel):
    """Response for experiment interaction"""
    session_id: str
    experiment_id: str
    partner_message: str
    mentor_guidance: Optional[str] = None
    wolfram_result: Optional[Dict[str, Any]] = None
    current_step: int
    progress: float


# API Routes

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to CSGirlies-AILAB",
        "version": "1.0.0",
        "description": "AI Simulated Lab Partner - Educational Experiment Simulation System"
    }


@app.get("/experiments")
async def list_experiments():
    """List all available experiments"""
    scenarios = list_scenarios()
    return {
        "experiments": [
            {
                "id": exp_id,
                "title": scenario.title,
                "subject": scenario.subject,
                "level": scenario.level,
                "duration_minutes": scenario.duration_minutes,
                "description": scenario.description
            }
            for exp_id, scenario in scenarios.items()
        ]
    }


@app.get("/experiments/{experiment_id}")
async def get_experiment_details(experiment_id: str):
    """Get detailed information about a specific experiment"""
    scenario = get_scenario(experiment_id)
    
    if not scenario:
        raise HTTPException(status_code=404, detail=f"Experiment '{experiment_id}' not found")
    
    return {
        "experiment_id": experiment_id,
        "title": scenario.title,
        "description": scenario.description,
        "subject": scenario.subject,
        "level": scenario.level,
        "duration_minutes": scenario.duration_minutes,
        "learning_objectives": scenario.learning_objectives,
        "materials": scenario.materials,
        "safety_notes": scenario.safety_notes,
        "steps": [
            {
                "step_number": step.step_number,
                "title": step.title,
                "description": step.description,
                "instructions": step.instructions,
                "expected_observation": step.expected_observation,
                "learning_objectives": step.learning_objectives,
                "tips": step.tips
            }
            for step in scenario.steps
        ]
    }


@app.post("/simulate/start")
async def start_experiment(request: StartExperimentRequest):
    """Start a new experiment session"""
    
    # Validate experiment
    scenario = get_scenario(request.experiment_id)
    if not scenario:
        raise HTTPException(status_code=404, detail=f"Experiment '{request.experiment_id}' not found")
    
    # Generate session ID
    session_id = generate_session_id()
    
    # Clear agent histories for new session
    partner_agent.clear_history()
    mentor_agent.clear_history()
    evaluator_agent.clear_history()
    
    # Get partner's opening message
    context = {
        "experiment_name": scenario.title,
        "student_message": f"I want to start the {scenario.title} experiment",
        "current_step": 1
    }
    
    partner_message = await partner_agent.think(context)
    
    logger.info(f"Started experiment session: {session_id} - {request.experiment_id}")
    
    return {
        "session_id": session_id,
        "experiment_id": request.experiment_id,
        "experiment_title": scenario.title,
        "student_name": request.student_name,
        "partner_message": partner_message,
        "first_step": {
            "step_number": 1,
            "title": scenario.steps[0].title,
            "instructions": scenario.steps[0].instructions
        }
    }


@app.post("/simulate/interact")
async def interact_with_experiment(request: StudentInputRequest) -> ExperimentResponse:
    """
    Process student input and return partner/mentor responses and Wolfram computation.
    """
    
    # Validate experiment
    scenario = get_scenario(request.experiment_id)
    if not scenario:
        raise HTTPException(status_code=404, detail=f"Experiment '{request.experiment_id}' not found")
    
    try:
        # Get current step
        current_step = scenario.get_step(request.current_step)
        if not current_step:
            current_step = scenario.steps[0]
        
        # Process student input through agents
        context = {
            "experiment_name": scenario.title,
            "student_message": request.student_message,
            "current_step": request.current_step
        }
        
        # Partner responds
        partner_message = await partner_agent.think(context)
        
        # Mentor provides guidance
        mentor_context = {
            "experiment_name": scenario.title,
            "conversation_history": [
                {"sender": "Student", "content": request.student_message},
                {"sender": "Partner", "content": partner_message}
            ],
            "student_progress": request.current_step / len(scenario.steps)
        }
        mentor_message = await mentor_agent.think(mentor_context)
        
        # Generate Wolfram computation if applicable
        wolfram_result = None
        if request.current_step == len(scenario.steps):
            # On final step, generate computation
            if request.experiment_id == "chem_titration":
                wolfram_result = await wolfram_engine.compute_titration(0.1, 20, 0.1)
            elif request.experiment_id == "phys_hookes_law":
                wolfram_result = await wolfram_engine.compute_hookes_law(300, 0.1)
            elif request.experiment_id == "bio_osmosis":
                wolfram_result = await wolfram_engine.compute_osmosis(0.1, 298, 0.01)
        
        progress = (request.current_step / len(scenario.steps)) * 100
        
        logger.info(f"Session {request.session_id}: Step {request.current_step} completed")
        
        return ExperimentResponse(
            session_id=request.session_id,
            experiment_id=request.experiment_id,
            partner_message=partner_message,
            mentor_guidance=mentor_message,
            wolfram_result={
                "query": wolfram_result.query if wolfram_result else None,
                "result": wolfram_result.result if wolfram_result else None,
                "graph_svg": wolfram_result.graph_svg if wolfram_result else None
            } if wolfram_result else None,
            current_step=request.current_step,
            progress=progress
        )
        
    except Exception as e:
        logger.error(f"Error in experiment interaction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/simulate/complete")
async def complete_experiment(session_id: str, experiment_id: str):
    """
    Complete experiment session and generate documentation.
    """
    
    scenario = get_scenario(experiment_id)
    if not scenario:
        raise HTTPException(status_code=404, detail=f"Experiment '{experiment_id}' not found")
    
    # Generate evaluator feedback
    eval_context = {
        "experiment_name": scenario.title,
        "full_conversation": [],
        "results": {}
    }
    
    evaluator_message = await evaluator_agent.think(eval_context)
    
    # Create GitBook documentation
    gitbook_response = await gitbook_integration.create_experiment_page(
        experiment_name=scenario.title,
        scenario_data={
            "description": scenario.description,
            "learning_objectives": scenario.learning_objectives,
            "materials": scenario.materials,
            "steps": [
                {
                    "step_number": s.step_number,
                    "title": s.title,
                    "instructions": s.instructions
                }
                for s in scenario.steps
            ]
        },
        results={
            "summary": "Experiment completed successfully",
            "partner_message": "Great work!",
            "mentor_message": "Well done!",
            "wolfram_result": "Computation executed",
            "conclusions": evaluator_message,
            "timestamp": "2024"
        }
    )
    
    logger.info(f"Completed experiment session: {session_id} - {experiment_id}")
    
    return {
        "session_id": session_id,
        "experiment_id": experiment_id,
        "status": "completed",
        "evaluator_feedback": evaluator_message,
        "gitbook_status": gitbook_response.get("success", False),
        "message": "Experiment completed! Documentation has been generated."
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "CSGirlies-AILAB",
        "version": "1.0.0"
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port
    )

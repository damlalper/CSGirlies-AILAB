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
        
        # Increment step for next interaction
        next_step = min(request.current_step + 1, len(scenario.steps))
        progress = (next_step / len(scenario.steps)) * 100

        logger.info(f"Session {request.session_id}: Step {request.current_step} completed, moving to step {next_step}")

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
            current_step=next_step,
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

    # Collect conversation history from agents
    partner_history = partner_agent.get_history()
    mentor_history = mentor_agent.get_history()

    # Build full conversation log
    conversation_history = []
    for msg in partner_history:
        conversation_history.append({
            "role": msg.role,
            "sender": msg.sender,
            "content": msg.content
        })

    # Create comprehensive GitBook lab report with local file
    gitbook_response = await gitbook_integration.create_experiment_report(
        session_id=session_id,
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
        conversation_history=conversation_history,
        observations=partner_agent.experiment_memory if hasattr(partner_agent, 'experiment_memory') else {},
        wolfram_results=[],  # Could be enhanced to track all Wolfram results
        evaluation={
            "feedback": evaluator_message,
            "status": "completed"
        }
    )

    logger.info(f"Completed experiment session: {session_id} - {experiment_id}")
    logger.info(f"Lab report saved to: {gitbook_response.get('local_file', 'N/A')}")
    logger.info(f"GitBook status: {gitbook_response}")


    # Return the full GitBook response to the frontend
    return {
        "session_id": session_id,
        "experiment_id": experiment_id,
        "status": "completed",
        "evaluator_feedback": evaluator_message,
        "gitbook_response": gitbook_response,
        "message": gitbook_response.get("message", "Experiment completed.")
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "CSGirlies-AILAB",
        "version": "1.0.0"
    }


@app.post("/export/report")
async def export_report(
    session_id: str,
    experiment_id: str,
    format: str = "pdf"
):
    """
    Export lab report in requested format.

    Formats: pdf, markdown, html, csv, json, all
    """
    from src.utils.export import ReportExporter, quick_export_pdf, quick_export_all

    # Get session data
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = active_sessions[session_id]

    # Get experiment details
    experiment = await load_experiment(experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")

    # Prepare report data
    from src.integrations.gitbook import GitBookIntegration
    gitbook = GitBookIntegration()

    # Generate markdown content
    markdown_content = gitbook._generate_markdown_report(
        session["conversation"],
        session.get("observations", {}),
        experiment,
        session_id
    )

    # Prepare full data
    full_data = {
        "session_id": session_id,
        "experiment": experiment.dict(),
        "conversation": session["conversation"],
        "observations": session.get("observations", {}),
        "timestamp": session.get("timestamp", "")
    }

    exporter = ReportExporter()

    try:
        if format == "all":
            # Export all formats
            exports = exporter.export_all_formats(
                markdown_content,
                session["conversation"],
                session.get("observations", {}),
                full_data,
                f"{experiment.title.replace(' ', '_')}_{session_id}"
            )
            return {
                "success": True,
                "message": "Exported in all formats",
                "files": exports
            }

        elif format == "pdf":
            pdf_path = exporter.export_to_pdf(
                markdown_content,
                f"{experiment.title.replace(' ', '_')}_{session_id}"
            )
            return {
                "success": True,
                "format": "pdf",
                "file_path": pdf_path
            }

        elif format == "markdown":
            md_path = exporter.export_to_markdown(
                markdown_content,
                f"{experiment.title.replace(' ', '_')}_{session_id}"
            )
            return {
                "success": True,
                "format": "markdown",
                "file_path": md_path
            }

        elif format == "html":
            html_path = exporter.export_to_html(
                markdown_content,
                f"{experiment.title.replace(' ', '_')}_{session_id}"
            )
            return {
                "success": True,
                "format": "html",
                "file_path": html_path
            }

        elif format == "csv":
            csv_path = exporter.export_to_csv(
                session["conversation"],
                session.get("observations", {}),
                f"{experiment.title.replace(' ', '_')}_{session_id}"
            )
            return {
                "success": True,
                "format": "csv",
                "file_path": csv_path
            }

        elif format == "json":
            json_path = exporter.export_to_json(
                full_data,
                f"{experiment.title.replace(' ', '_')}_{session_id}"
            )
            return {
                "success": True,
                "format": "json",
                "file_path": json_path
            }

        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")

    except Exception as e:
        logger.error(f"Export error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


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

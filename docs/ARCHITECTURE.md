# Development Notes & Architecture

## System Architecture

### Request Flow
```
Client Request
    ↓
FastAPI Server (app.py)
    ↓
Route Handler
    ├→ Validate Request
    ├→ Load Scenario
    └→ Process through Multi-Agent System
         ├→ Partner Agent (OpenAI)
         ├→ Mentor Agent (OpenAI)
         └→ Evaluator Agent (OpenAI)
    ↓
Wolfram Engine
    ├→ Compute
    ├→ Generate Graphs
    └→ Return Results
    ↓
GitBook Integration
    └→ Auto-generate Documentation
    ↓
Return JSON Response
```

## Agent Decision Tree

### Partner Agent
```
User Input
    ↓
Extract Context (experiment, step, conversation history)
    ↓
Build Prompt with Personality
    ↓
Call OpenAI GPT-4
    ↓
Generate Conversational Response
    ↓
Add to History
    ↓
Return Message
```

### Mentor Agent
```
Monitor Conversation
    ↓
Analyze Student Statements
    ↓
Detect Potential Misconceptions
    ↓
Provide Guiding Questions
    ↓
Rate Understanding Level
    ↓
Return Guidance
```

## Scenario Data Model

```python
ExperimentScenario:
    experiment_id: str
    title: str
    description: str
    subject: str (physics|chemistry|biology)
    level: ExperimentLevel (beginner|intermediate|advanced)
    duration_minutes: int
    learning_objectives: List[str]
    materials: List[str]
    steps: List[ExperimentStep]
        └─ step_number: int
        └─ title: str
        └─ instructions: str
        └─ expected_observation: str
        └─ learning_objectives: List[str]
        └─ tips: List[str]
    safety_notes: List[str]
    wolfram_computations: Dict[str, str]
```

## Integration Points

### OpenAI Integration
- Model: GPT-4-turbo-preview
- Temperature: 0.7-0.8 (for natural variation)
- Max tokens: 100-150 per response
- Error handling: Fallback responses provided

### Wolfram Integration
- Computation: Real-time formulas
- Graphing: SVG output (base64 encoded)
- Fallback: Sample graphs provided
- Query format: Wolfram Language

### GitBook Integration
- API: GitBook API v1
- Content: Markdown formatted
- Automatic: Triggered on session completion
- Fallback: Local markdown export

## Data Flow Examples

### Start Experiment Flow
```
POST /simulate/start
├─ Validate experiment_id
├─ Create session_id
├─ Load scenario from SCENARIOS
├─ Clear agent histories
├─ Generate partner opening message
└─ Return start response

Response:
{
  session_id: uuid,
  experiment_title: string,
  partner_message: string,
  first_step: {...}
}
```

### Interact Flow
```
POST /simulate/interact
├─ Validate session_id & experiment_id
├─ Load scenario
├─ Process student message through:
│   ├─ Partner agent → generates response
│   ├─ Mentor agent → generates guidance
│   └─ [Optional] Wolfram → generates computation
├─ Add messages to history
└─ Return interaction response

Response:
{
  session_id: uuid,
  partner_message: string,
  mentor_guidance: string,
  wolfram_result: {...},
  progress: float
}
```

### Complete Flow
```
POST /simulate/complete
├─ Validate session_id & experiment_id
├─ Get evaluator feedback
├─ Build scenario data
├─ Generate markdown documentation
├─ Call GitBook API (or skip if no key)
└─ Return completion response

Response:
{
  status: "completed",
  evaluator_feedback: string,
  gitbook_status: boolean,
  message: string
}
```

## Error Handling Strategy

### Level 1: Input Validation
```
- Check experiment_id exists
- Validate step numbers
- Check session_id format
```

### Level 2: Agent Errors
```
- Catch OpenAI API errors
- Provide fallback responses
- Log to console
```

### Level 3: Integration Errors
```
- Gracefully handle Wolfram timeouts
- Skip GitBook if API key missing
- Return partial results
```

### Level 4: Server Errors
```
- Return 500 with error message
- Log full traceback
- Don't expose sensitive info
```

## Configuration Management

### Environment Variables (.env)
```
OPENAI_API_KEY=sk-...        # Required
WOLFRAM_APPID=...            # Optional (fallbacks available)
GITBOOK_API_KEY=...          # Optional
GITBOOK_SPACE_ID=...         # Optional
HOST=127.0.0.1               # Default
PORT=8000                    # Default
DEBUG=True                   # Default
LOG_LEVEL=INFO              # Default
```

### Settings Class
```python
class Settings:
    - Reads from .env
    - Provides defaults
    - Validates required vars
    - Used globally via `settings` instance
```

## Performance Considerations

### Optimization Techniques
1. **Conversation History Limiting**
   - Keep last 5 messages only
   - Reduces token count for API calls

2. **Graph Caching**
   - Sample graphs for common scenarios
   - Falls back to pre-generated SVGs

3. **Session Management**
   - Clear histories after completion
   - Prevent memory leaks

4. **Async/Await**
   - All agent calls are async-ready
   - Allows concurrent requests

### Bottlenecks
1. **OpenAI API latency** (2-3 seconds)
   - Solution: Parallel agent calls
2. **Wolfram computation** (1-2 seconds)
   - Solution: Pre-computed graphs
3. **Network I/O**
   - Solution: Connection pooling

## Testing Strategy

### Unit Tests (Planned)
```python
test_agents.py
  ├─ test_partner_agent()
  ├─ test_mentor_agent()
  └─ test_evaluator_agent()

test_scenarios.py
  ├─ test_load_titration()
  ├─ test_load_hookes_law()
  └─ test_load_osmosis()

test_wolfram.py
  ├─ test_titration_computation()
  ├─ test_hookes_law_computation()
  └─ test_osmosis_computation()
```

### Integration Tests (Planned)
```python
test_api.py
  ├─ test_start_experiment()
  ├─ test_student_interaction()
  ├─ test_complete_experiment()
  └─ test_end_to_end_workflow()
```

## Deployment Considerations

### Production Setup
1. Use environment variables for all secrets
2. Set DEBUG=False
3. Configure proper CORS origins
4. Set up logging aggregation
5. Use uvicorn with multiple workers
6. Add load balancer if needed

### Scaling Options
1. **Horizontal**: Multiple uvicorn workers
2. **Caching**: Redis for session data
3. **Queue**: Celery for async tasks
4. **Database**: PostgreSQL for persistence

### Monitoring
1. Error tracking (Sentry)
2. Performance monitoring (NewRelic)
3. Log aggregation (ELK stack)
4. API metrics (Prometheus)

## Code Quality

### Standards Followed
- PEP 8 style guide
- Type hints on all functions
- Docstrings for all classes/functions
- Error handling throughout
- Logging at key points

### Tools Used
- Black: Code formatting
- Flake8: Linting
- MyPy: Type checking
- Pytest: Testing

## Future Architecture Changes

1. **Database Integration**
   - Store sessions in PostgreSQL
   - Persist experiment results
   - Track student progress

2. **Caching Layer**
   - Redis for conversation cache
   - Pre-computed results
   - Session storage

3. **Message Queue**
   - Celery for background tasks
   - Async GitBook updates
   - Experiment result processing

4. **Web Frontend**
   - React/Vue UI
   - Real-time updates (WebSocket)
   - Student dashboard

5. **Analytics**
   - Learning analytics
   - Performance metrics
   - Engagement tracking

---

**Last Updated**: 2024
**Architecture Version**: 1.0

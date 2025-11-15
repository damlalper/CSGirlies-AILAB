# CSGirlies-AILAB - Setup and Execution Guide

## Quick Start (3 Steps)

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start Backend Server
```bash
python -m uvicorn app:app --reload
```
The backend will be available at: `http://localhost:8000`

### Step 3: Setup and Run Frontend
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at: `http://localhost:5173`

---

## Detailed Setup Instructions

### Prerequisites
- **Python 3.11+** - For backend
- **Node.js 16+** - For frontend (includes npm)
- **OpenAI API Key** - For AI agents
- **Wolfram App ID** (Optional) - For advanced computations

### Environment Configuration

Create a `.env` file in the project root:
```
# OpenAI Configuration
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# Wolfram Configuration
WOLFRAM_APPID=your-wolfram-app-id-here

# GitBook (Optional)
GITBOOK_API_KEY=your-gitbook-key
GITBOOK_SPACE_ID=your-space-id

# Server Configuration
HOST=127.0.0.1
PORT=8000
DEBUG=true
LOG_LEVEL=INFO
```

### Backend Setup

#### 1. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Start Development Server
```bash
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Frontend Setup

#### 1. Install Dependencies
```bash
cd frontend
npm install
```

#### 2. Start Development Server
```bash
npm run dev
```

**Expected Output:**
```
  VITE v5.0.0  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

#### 3. Build for Production
```bash
npm run build
npm run preview
```

---

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Suite
```bash
# Test API endpoints
pytest tests/test_api.py -v

# Test scenarios
pytest tests/test_scenarios.py -v

# Test agents
pytest tests/test_agents.py -v
```

### Run with Coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

### Expected Test Results
```
======================== 21 passed in 2.65s ========================

Test Breakdown:
- test_agents.py: 7 tests (agents initialization, methods, history management)
- test_api.py: 8 tests (endpoints, workflows, error handling)
- test_scenarios.py: 6 tests (scenario structure, materials, safety notes)
```

---

## API Endpoints

### Available Experiments
1. **Acid-Base Titration** (Chemistry)
   - ID: `acid_base_titration`
   - Duration: 45 minutes
   - Level: Beginner
   - Learning: Neutralization, molarity calculations

2. **Hooke's Law** (Physics)
   - ID: `hookes_law`
   - Duration: 40 minutes
   - Level: Intermediate
   - Learning: Spring constants, linear relationships

3. **Osmosis** (Biology)
   - ID: `osmosis`
   - Duration: 50 minutes
   - Level: Intermediate
   - Learning: Osmotic pressure, concentration effects

### Key Endpoints

**List Experiments**
```
GET /experiments
Returns: List of available experiments with metadata
```

**Get Experiment Details**
```
GET /experiments/{experiment_id}
Example: GET /experiments/acid_base_titration
Returns: Full experiment details, steps, materials, learning objectives
```

**Start Experiment Session**
```
POST /simulate/start
Body: {
  "experiment_id": "acid_base_titration",
  "level": "beginner",
  "student_name": "John Doe"
}
Returns: session_id, partner greeting message
```

**Interact with Experiment**
```
POST /simulate/interact
Body: {
  "session_id": "session-123",
  "experiment_id": "acid_base_titration",
  "student_message": "I've added 10mL of NaOH",
  "current_step": 1
}
Returns: Partner response, mentor guidance, Wolfram computation results
```

**Complete Experiment**
```
POST /simulate/complete
Params: session_id, experiment_id
Returns: Session summary, learning metrics, feedback
```

**Health Check**
```
GET /health
Returns: {"status": "healthy"}
```

---

## Multi-Agent System

### Agent Roles

1. **Partner Agent (Alex)** - Lab Companion
   - Friendly conversational support
   - Encouragement and motivation
   - Step-by-step guidance

2. **Mentor Agent (Dr. Silva)** - Learning Guide
   - Socratic questioning
   - Misconception detection
   - Conceptual understanding

3. **Evaluator Agent (Dr. Evaluator)** - Assessment
   - Learning outcome evaluation
   - Performance feedback
   - Progress tracking

### Interaction Flow
```
Student Input
    ↓
Partner Agent (Initial Response)
    ↓
Mentor Agent (Learning Guidance)
    ↓
Wolfram Engine (Scientific Computation)
    ↓
Evaluator Agent (Feedback)
    ↓
Response to Student
```

---

## Science Features

### Computations Supported

1. **Titration** (Acid-Base)
   - pH curve calculation
   - Equivalence point determination
   - Molarity calculations

2. **Hooke's Law** (Spring Physics)
   - Force-displacement relationships
   - Spring constant calculation
   - Linear regression analysis

3. **Osmosis** (Cell Biology)
   - Osmotic pressure (π = iMRT)
   - Solution tonicity analysis
   - Mass change predictions

### Data Visualization
- SVG graph generation for scientific results
- Real-time plotting of experimental data
- Integration with Wolfram Cloud (when available)

---

## Project Structure

```
CSGirlies-AILAB/
├── app.py                          # Main FastAPI application
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
├── src/
│   ├── agents/                     # AI agents (Partner, Mentor, Evaluator)
│   ├── scenarios/                  # Experiment definitions
│   ├── wolfram_engine/             # Scientific computations
│   ├── integrations/               # External API integrations
│   ├── config.py                   # Settings management
│   └── utils.py                    # Helper functions
├── tests/                          # Test suite
│   ├── test_api.py                 # API endpoint tests
│   ├── test_scenarios.py           # Scenario validation
│   ├── test_agents.py              # Agent functionality
│   └── conftest.py                 # Pytest fixtures
├── frontend/                       # React application
│   ├── src/
│   │   ├── App.jsx                 # Main React component
│   │   ├── App.css                 # Styling
│   │   └── main.jsx                # Entry point
│   ├── package.json                # Node dependencies
│   ├── vite.config.js              # Vite configuration
│   └── index.html                  # HTML template
└── docs/
    ├── README.md                   # Project overview
    ├── QUICKSTART.md               # Quick start guide
    └── prd.md                      # Product requirements
```

---

## Troubleshooting

### Backend Issues

**Port 8000 Already in Use**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID> /F

# Or use different port
uvicorn app:app --reload --port 8001
```

**OpenAI API Key Error**
```
ValidationError: openai_api_key
Field required
```
**Solution**: Ensure `.env` file exists with valid `OPENAI_API_KEY`

**Missing Dependencies**
```bash
# Reinstall all requirements
pip install -r requirements.txt --upgrade
```

### Frontend Issues

**npm Install Fails**
```bash
# Clear npm cache
npm cache clean --force

# Reinstall node_modules
rm -rf node_modules
npm install
```

**Port 5173 Already in Use**
```bash
# Vite will automatically use next available port
npm run dev
```

**Frontend Can't Connect to Backend**
- Ensure backend is running on `http://localhost:8000`
- Check CORS configuration in `app.py`
- Verify network connectivity

### Test Failures

**pytest Not Found**
```bash
pip install pytest pytest-asyncio
```

**Import Errors in Tests**
```bash
# Ensure dependencies are installed
pip install -r requirements.txt

# Run from project root directory
cd c:\Users\Lenovo\CSGirlies-AILAB
pytest tests/
```

---

## Performance Optimization

### Backend
- Uses async/await for concurrent agent processing
- Caches scenario definitions
- Optimized Wolfram computations

### Frontend
- Vite for fast development builds
- React lazy loading for experiments
- CSS animations optimized with GPU

---

## Next Steps

1. **Complete Full Workflow**: Start an experiment in the UI and go through all steps
2. **Customize Experiments**: Add more experiment scenarios in `src/scenarios/scenarios.py`
3. **Add Persistence**: Integrate database for student progress tracking
4. **Deploy**: Containerize with Docker for deployment

---

## Support & Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **React Documentation**: https://react.dev
- **OpenAI API**: https://platform.openai.com/docs
- **Wolfram Cloud**: https://www.wolframcloud.com

---

## Version Info

- **CSGirlies-AILAB**: v1.0.0
- **FastAPI**: 0.104.1+
- **Python**: 3.11+
- **Node.js**: 16+
- **React**: 18.2.0+


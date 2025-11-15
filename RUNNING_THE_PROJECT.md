# Running CSGirlies-AILAB - Complete Guide

## 🚀 Quick Start (5 Minutes)

### Terminal 1: Backend
```bash
cd c:\Users\Lenovo\CSGirlies-AILAB
python -m uvicorn app:app --reload
```
✅ Backend running at: http://localhost:8000

### Terminal 2: Frontend
```bash
cd c:\Users\Lenovo\CSGirlies-AILAB\frontend
npm run dev
```
✅ Frontend running at: http://localhost:5173

### Terminal 3: Tests (Optional)
```bash
cd c:\Users\Lenovo\CSGirlies-AILAB
pytest tests/ -v
```
✅ All 21 tests should pass

---

## 📋 Prerequisites

Before starting, ensure you have:

✅ **Python 3.11+**
```bash
python --version
```

✅ **Node.js 16+ with npm**
```bash
node --version
npm --version
```

✅ **.env file configured** in project root
```
OPENAI_API_KEY=your-key-here
WOLFRAM_APPID=your-app-id
```

✅ **Python dependencies installed**
```bash
pip install -r requirements.txt
```

✅ **Node dependencies installed**
```bash
cd frontend
npm install
cd ..
```

---

## 🏃 Step-by-Step Execution

### Step 1: Configure Environment (One-time Setup)

```bash
# Navigate to project root
cd c:\Users\Lenovo\CSGirlies-AILAB

# Create .env file if it doesn't exist
echo OPENAI_API_KEY=sk-your-key-here >> .env
echo WOLFRAM_APPID=your-app-id >> .env
```

### Step 2: Install Dependencies (One-time Setup)

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### Step 3: Start Services

**Open 3 Terminal Windows:**

**Terminal 1 - Backend:**
```bash
cd c:\Users\Lenovo\CSGirlies-AILAB
python -m uvicorn app:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Terminal 2 - Frontend:**
```bash
cd c:\Users\Lenovo\CSGirlies-AILAB\frontend
npm run dev
```

Expected output:
```
  VITE v5.0.0  ready in 234 ms

  ➜  Local:   http://localhost:5173/
```

**Terminal 3 - Tests (Optional):**
```bash
cd c:\Users\Lenovo\CSGirlies-AILAB
pytest tests/ -v
```

Expected output:
```
======================== 21 passed in 2.65s ========================
```

### Step 4: Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🎯 Using the Application

### 1. Load Frontend
Go to http://localhost:5173

You should see:
- Welcome page with CSGirlies-AILAB branding
- Three experiment cards (Titration, Hooke's Law, Osmosis)

### 2. Select an Experiment
Click on any experiment card to view details:
- **Acid-Base Titration** (Chemistry)
- **Hooke's Law** (Physics)
- **Osmosis** (Biology)

### 3. Start Experiment
1. Enter your name (Student Name)
2. Select difficulty level (Beginner/Intermediate/Advanced)
3. Click "Start Experiment"
4. Partner Agent (Alex) will greet you

### 4. Interact with Agents
1. Type your response in the chat input
2. See responses from:
   - **Partner** (Lab Companion - Friendly support)
   - **Mentor** (Learning Guide - Guidance & questions)
   - **Evaluator** (Assessment - Feedback)
3. Watch scientific graphs and calculations

### 5. Complete Experiment
After finishing all steps, get:
- Summary of learning outcomes
- Mentor feedback
- Performance metrics

---

## 🧪 Testing the System

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Category
```bash
# Agent tests
pytest tests/test_agents.py -v

# API endpoint tests
pytest tests/test_api.py -v

# Scenario tests
pytest tests/test_scenarios.py -v
```

### Expected Results
```
tests/test_agents.py::test_partner_agent_initialization PASSED
tests/test_agents.py::test_partner_agent_think PASSED
... (more tests)
======================== 21 passed in 2.65s ========================
```

---

## 🔌 API Testing (Without Frontend)

### Test Root Endpoint
```bash
curl http://localhost:8000
```

Response:
```json
{
  "message": "Welcome to CSGirlies-AILAB",
  "version": "1.0.0"
}
```

### List Experiments
```bash
curl http://localhost:8000/experiments
```

Response:
```json
{
  "experiments": [
    {
      "id": "acid_base_titration",
      "title": "Acid-Base Titration: Finding Molarity",
      "subject": "chemistry"
    },
    // ... more experiments
  ]
}
```

### Start an Experiment
```bash
curl -X POST http://localhost:8000/simulate/start \
  -H "Content-Type: application/json" \
  -d '{
    "experiment_id": "acid_base_titration",
    "student_name": "John Doe"
  }'
```

### View API Documentation
Navigate to: http://localhost:8000/docs

Interactive Swagger UI for all endpoints

---

## 📊 Monitoring & Debugging

### Backend Logs
The terminal running the backend will show:
```
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:root:Started experiment session: SESSION-123 - acid_base_titration
```

### Frontend Logs
Browser console (F12) will show:
```
API Call: GET http://localhost:8000/experiments
Response: 200 OK [3 experiments]
```

### Performance Metrics
- Backend startup: <1 second
- Experiment start: ~1-2 seconds (API call)
- Agent response: ~2-5 seconds (depends on OpenAI)
- Full workflow: ~15-20 seconds

---

## ⚠️ Troubleshooting

### Backend Won't Start

**Error**: `Address already in use`
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
uvicorn app:app --reload --port 8001
```

**Error**: `No module named 'openai'`
```bash
pip install -r requirements.txt --upgrade
```

**Error**: `ValidationError: openai_api_key`
```bash
# Ensure .env file exists with:
OPENAI_API_KEY=sk-xxx
```

### Frontend Won't Connect

**Issue**: Cannot reach backend
```bash
# Check backend is running
curl http://localhost:8000

# Check CORS settings in app.py
# Should have: allow_origins=["*"]
```

**Issue**: Port 5173 already in use
```bash
# Vite will use next available port
npm run dev
# Check output for actual port
```

### Tests Failing

**Error**: `ModuleNotFoundError`
```bash
# Install test dependencies
pip install pytest pytest-asyncio
```

**Error**: `Asyncio compatibility`
```bash
# Run from project root
cd c:\Users\Lenovo\CSGirlies-AILAB
pytest tests/ -v
```

---

## 📁 Project Structure Reference

```
c:\Users\Lenovo\CSGirlies-AILAB\
├── app.py                    # Main API server
├── requirements.txt          # Python dependencies
├── .env                      # Configuration file
├── src/
│   ├── agents/              # AI agents
│   ├── scenarios/           # Experiments
│   └── wolfram_engine/      # Computations
├── tests/
│   ├── test_api.py
│   ├── test_agents.py
│   ├── test_scenarios.py
│   └── conftest.py
├── frontend/                # React app
│   ├── src/App.jsx
│   ├── src/App.css
│   └── package.json
└── docs/
    ├── README.md
    ├── SETUP_GUIDE.md
    ├── TEST_REPORT.md
    └── prd.md
```

---

## 🎓 Learning Paths

### Path 1: Complete Student Experience
1. Start frontend → http://localhost:5173
2. Select "Acid-Base Titration"
3. Follow all 4 steps with partner guidance
4. See mentor feedback and scientific calculations
5. Get evaluation report

### Path 2: Developer Testing
1. Review test report: `TEST_REPORT.md`
2. Run all tests: `pytest tests/ -v`
3. Check API endpoints: `curl http://localhost:8000/docs`
4. Inspect network logs in browser (F12)

### Path 3: API Integration
1. Read API docs: http://localhost:8000/docs
2. Test endpoints with curl or Postman
3. Build custom client integration
4. Process agent responses

---

## 📈 Performance Tips

### Backend Optimization
```bash
# Production mode (no reload)
uvicorn app:app --host 0.0.0.0 --port 8000

# Multiple worker processes
uvicorn app:app --workers 4
```

### Frontend Optimization
```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

---

## ✅ Verification Checklist

Before considering setup complete, verify:

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:5173
- [ ] All 21 tests pass
- [ ] Can see 3 experiments in UI
- [ ] Can start an experiment
- [ ] Partner agent responds
- [ ] No console errors
- [ ] .env file configured

---

## 🆘 Getting Help

### Check Logs
```bash
# Backend logs in running terminal
# Frontend logs in browser console (F12)
# Test logs: pytest tests/ -v -s
```

### Debug Mode
```bash
# Backend debug logging
export LOG_LEVEL=DEBUG
uvicorn app:app --reload
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI schema: http://localhost:8000/openapi.json

---

## 📞 Support Resources

- **FastAPI**: https://fastapi.tiangolo.com
- **React**: https://react.dev
- **Pytest**: https://docs.pytest.org
- **Vite**: https://vitejs.dev

---

## ⏱️ Expected Startup Times

| Component | Time |
|-----------|------|
| Backend startup | <1s |
| Frontend startup | 1-2s |
| Load experiments | <1s |
| Start experiment | 1-2s |
| Agent response | 2-5s |
| Full workflow | 15-20s |

---

**Ready to start?** Run this command:
```bash
python -m uvicorn app:app --reload
```

Then open: http://localhost:5173

Happy Experimenting! 🧪🎓


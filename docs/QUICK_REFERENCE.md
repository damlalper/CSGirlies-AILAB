# CSGirlies-AILAB - Quick Reference Card

## 🚀 How to Run (Copy-Paste)

### Terminal 1: Backend
```bash
cd c:\Users\Lenovo\CSGirlies-AILAB
python -m uvicorn app:app --reload
```

### Terminal 2: Frontend
```bash
cd c:\Users\Lenovo\CSGirlies-AILAB\frontend
npm run dev
```

### Terminal 3: Tests
```bash
cd c:\Users\Lenovo\CSGirlies-AILAB
pytest tests/ -v
```

**Expected Result**: All 21 tests PASS ✅

---

## 🌐 Access URLs

| Component | URL | Purpose |
|-----------|-----|---------|
| Frontend | http://localhost:5173 | User interface |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Swagger UI |
| ReDoc | http://localhost:8000/redoc | API documentation |

---

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| Total Files | 37 |
| Python Files | 15+ |
| React Components | 1 main component |
| Test Files | 3 |
| Tests Passing | 21/21 (100%) |
| Backend Code | ~2,000 lines |
| Frontend Code | ~700 lines |
| Documentation | 7 guides |

---

## 🎯 Key Features

### ✅ Multi-Agent AI System
- **Partner Agent** - Conversational support
- **Mentor Agent** - Learning guidance  
- **Evaluator Agent** - Assessment & feedback

### ✅ Science Experiments (3)
- **Chemistry**: Acid-Base Titration
- **Physics**: Hooke's Law
- **Biology**: Osmosis

### ✅ Full Stack
- Backend: FastAPI + Python
- Frontend: React + Vite
- Testing: Pytest + 21 tests
- Documentation: 7 comprehensive guides

---

## 🔑 Environment Setup

Create `.env` file with:
```
OPENAI_API_KEY=your-api-key
WOLFRAM_APPID=your-app-id (optional)
```

---

## 📝 Experiment Workflow

```
1. Student selects experiment
2. Partner greets student
3. Follow 4 guided steps
4. Mentor provides guidance
5. Get AI-powered feedback
6. View scientific computations
7. Complete experiment
8. Get assessment report
```

---

## 🧪 Test Results

```
✅ test_agents.py: 7 tests PASSED
✅ test_api.py: 8 tests PASSED  
✅ test_scenarios.py: 6 tests PASSED

Total: 21/21 tests PASSED in 2.65s
Success Rate: 100%
```

---

## 🎨 Technologies

| Layer | Technology |
|-------|-----------|
| Frontend | React 18.2 + Vite + Axios |
| Backend | FastAPI + Uvicorn + Python 3.11 |
| AI | OpenAI GPT-4 |
| Testing | Pytest + pytest-asyncio |
| Computation | Wolfram Cloud (optional) |

---

## 📁 Project Structure

```
.
├── app.py                    # Main server
├── requirements.txt          # Dependencies
├── .env                      # Configuration
├── src/
│   ├── agents/              # AI agents
│   ├── scenarios/           # Experiments
│   └── wolfram_engine/      # Computations
├── tests/                   # Test suite (21 tests)
├── frontend/                # React app
└── docs/
    ├── RUNNING_THE_PROJECT.md
    ├── SETUP_GUIDE.md
    ├── TEST_REPORT.md
    ├── HACKATHON_SUBMISSION.md
    └── README.md
```

---

## ⚡ Quick Commands

```bash
# Install Python deps
pip install -r requirements.txt

# Install Node deps
cd frontend && npm install

# Run backend
python -m uvicorn app:app --reload

# Run frontend
cd frontend && npm run dev

# Run tests
pytest tests/ -v

# Build frontend
npm run build
```

---

## 🏆 Why This Project Stands Out

1. **Complete Solution** - Not just API, includes beautiful UI
2. **Production Quality** - Professional code with tests
3. **Real AI** - Uses OpenAI GPT-4 multi-agent system
4. **Education Focus** - 3 complete science experiments
5. **Well Tested** - 21 tests, 100% passing
6. **Well Documented** - 7 comprehensive guides
7. **Easy to Demo** - Works locally, no complex setup
8. **Scalable** - Async architecture, ready for production

---

## 💾 What to Show Judges

1. **Frontend Demo** (http://localhost:5173)
   - Select an experiment
   - Start the session
   - Chat with AI agents
   - See scientific computations

2. **Backend Demo** (http://localhost:8000/docs)
   - Show API endpoints
   - Try endpoint in Swagger UI
   - Show structured responses

3. **Test Results**
   - Run: `pytest tests/ -v`
   - Show all 21 tests passing
   - Highlight 100% success rate

4. **Code Quality**
   - Review `app.py` (well-structured)
   - Review `tests/` (comprehensive)
   - Show type hints and docstrings

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| README.md | Project overview |
| QUICKSTART.md | 5-minute start |
| SETUP_GUIDE.md | Detailed setup |
| RUNNING_THE_PROJECT.md | Full execution guide |
| TEST_REPORT.md | Test results |
| HACKATHON_SUBMISSION.md | Submission highlights |

---

## 🎓 Learning Features

- **Guided Experiments**: 4 steps per experiment
- **AI Mentoring**: Real-time feedback
- **Scientific Accuracy**: Real formulas (pH, F=kx, π=iMRT)
- **Progress Tracking**: Step-by-step feedback
- **Achievement Recognition**: Evaluation reports

---

## ✅ Pre-Demo Checklist

- [ ] Python 3.11+ installed
- [ ] Node.js 16+ installed  
- [ ] `pip install -r requirements.txt` run
- [ ] `cd frontend && npm install` run
- [ ] `.env` file with OPENAI_API_KEY configured
- [ ] Backend starts without errors
- [ ] Frontend loads at localhost:5173
- [ ] Tests pass: `pytest tests/ -v`

---

## ⏱️ Demo Timeline (10 minutes)

1. **Intro** (1 min) - Show what CSGirlies-AILAB is
2. **Frontend** (3 min) - Demo UI, select experiment
3. **Interaction** (3 min) - Show AI agents in action
4. **Backend** (2 min) - Show API docs
5. **Tests** (1 min) - Run pytest, show results

---

## 🚨 Troubleshooting

| Issue | Fix |
|-------|-----|
| Port 8000 in use | Use `--port 8001` |
| Port 5173 in use | Vite finds next port |
| Missing dependencies | Run `pip install -r requirements.txt` |
| No OpenAI key | Add to `.env` file |
| Tests fail | Ensure dependencies installed |

---

## 🎯 Success Criteria

- ✅ System runs without errors
- ✅ All 21 tests pass
- ✅ Frontend loads and is responsive
- ✅ Backend API responds to requests
- ✅ AI agents generate responses
- ✅ Experiments can be completed
- ✅ Scientific computations work
- ✅ Professional code quality

---

## 📊 Key Metrics

- **Code Size**: 2,700+ lines (backend) + 700 lines (frontend)
- **Test Coverage**: 21 tests covering critical paths
- **Test Success Rate**: 100% (21/21 passing)
- **Execution Time**: 2.65 seconds for full test suite
- **Documentation**: 7 comprehensive guides
- **Experiments**: 3 complete scenarios with 4 steps each
- **Agents**: 3 specialized AI agents with distinct roles
- **API Endpoints**: 7 RESTful endpoints

---

## 🌟 Standout Points for Judges

1. **Real AI Integration**: Uses OpenAI GPT-4, not mock responses
2. **Multiple Agents**: 3 agents with different pedagogical roles
3. **Science Content**: Real educational value, not just a demo
4. **Full Stack**: Complete app with UI, not just backend
5. **Production Ready**: Error handling, logging, configuration
6. **Test Driven**: 100% test pass rate shows quality
7. **Well Documented**: Judges can understand and run everything
8. **Hackathon Scope**: Complete project in available time

---

**CSGirlies-AILAB** - AI-Powered Lab Simulations Ready for Demo! 🚀


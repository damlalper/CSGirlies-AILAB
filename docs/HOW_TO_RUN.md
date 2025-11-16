# CSGirlies-AILAB - How to Run? 🚀

## 🎯 Quick Start (5 Minutes)

### Step 1: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Environment Variables
```bash
cp .env.example .env
# Open the .env file and add API keys
```

**API Keys you need:**
- **OPENAI_API_KEY**: https://platform.openai.com/api-keys
- **WOLFRAM_APPID**: https://www.wolfram.com/cloud/ (optional)
- **GITBOOK_API_KEY**: (optional)

### Step 4: Start the Server
```bash
uvicorn app:app --reload
```

The server will run at: `http://127.0.0.1:8000`

### Step 5: Run the Demo Script
Open a new terminal (with venv active):
```bash
python demo.py
```

### Step 6: Explore the API
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## 📋 Detailed Steps

### 1. Python and Dependencies
```bash
# Python 3.8+ required
python --version

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
# Create .env file
cp .env.example .env

# Open .env file with a text editor and add:
OPENAI_API_KEY=sk-your-key-here
WOLFRAM_APPID=your-app-id
```

### 3. Start the Server
```bash
# Development mode
uvicorn app:app --reload

# Or production mode
uvicorn app:app --host 0.0.0.0 --port 8000
```

### 4. Configure Test
```bash
# Run demo script
python demo.py

# Or test with curl
curl http://127.0.0.1:8000/

# List experiments
curl http://127.0.0.1:8000/experiments
```

---

## 🔧 API Tests

### Test in Terminal (Windows PowerShell)

**Start Experiment:**
```powershell
$body = @{
    experiment_id = "chem_titration"
    level = "beginner"
    student_name = "Student"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/simulate/start" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

**List Experiments:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/experiments" | ConvertFrom-Json
```

**Check Server Status:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/health"
```

---

## 🧪 Learn Available Experiments

### 1. Acid-Base Titration (Chemistry)
- **ID**: `chem_titration`
- **Level**: Beginner
- **Duration**: 45 minutes
- **Steps**: 4 steps
- **Topic**: Determining unknown acid concentration

### 2. Hooke's Law (Physics)
- **ID**: `phys_hookes_law`
- **Level**: Beginner
- **Duration**: 40 minutes
- **Steps**: 4 steps
- **Topic**: Determining spring constant (F = kx)

### 3. Osmosis (Biology)
- **ID**: `bio_osmosis`
- **Level**: Intermediate
- **Duration**: 50 minutes
- **Steps**: 4 steps
- **Topic**: Osmotic pressure (π = iMRT)

---

## 📊 API Endpoints

### GET Requests
```
GET /                          -> Welcome
GET /health                    -> Server status
GET /experiments               -> List all experiments
GET /experiments/{id}          -> Experiment details
```

### POST Requests
```
POST /simulate/start           -> Start experiment
POST /simulate/interact        -> Process student input
POST /simulate/complete        -> Complete experiment
```

---

## ⚠️ Troubleshooting

### "ModuleNotFoundError" error
```bash
pip install -r requirements.txt
```

### "OPENAI_API_KEY not set" error
- Did you create a `.env` file?
- Was the API key added to `.env`?
- Did you copy the key correctly?

### Server not starting
```bash
# Port 8000 might be in use
uvicorn app:app --port 8001 --reload

# Or kill the process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Wolfram error
- Optional - system uses fallback graphics
- Works even if you don't add WOLFRAM_APPID

### GitBook error
- Optional - system works without it

---

## 🎓 Understanding the System

### Flow
```
Student
  ↓
FastAPI Server
  ├→ Partner Agent (Chat)
  ├→ Mentor Agent (Guidance)
  └→ Evaluator Agent (Evaluation)
  ↓
Wolfram Engine (Calculations/Graphics)
  ↓
GitBook (Documentation)
  ↓
Response
```

### File Structure
```
CSGirlies-AILAB/
├── app.py              ← Main application
├── demo.py             ← Demo script
├── requirements.txt    ← Dependencies
├── .env.example        ← Environment template
├── src/
│   ├── agents/         ← AI Agents (3 of them)
│   ├── scenarios/      ← Experiment definitions (3 of them)
│   ├── wolfram_engine/ ← Calculation engine
│   ├── integrations/   ← API integrations
│   └── utils/          ← Helper functions
└── docs/               ← Documents
```

---

## 🔍 Environment Variables

Variables to be found in `.env` file:

```env
# OpenAI (Required)
OPENAI_API_KEY=sk-xxxxx

# Wolfram (Optional)
WOLFRAM_APPID=xxxxx

# GitBook (Optional)
GITBOOK_API_KEY=xxxxx
GITBOOK_SPACE_ID=xxxxx

# Server
HOST=127.0.0.1
PORT=8000
DEBUG=True
LOG_LEVEL=INFO
```

---

## 📦 Dependencies

```
fastapi==0.104.1           ← Web framework
uvicorn==0.24.0            ← ASGI server
openai==1.3.0              ← OpenAI API
pydantic==2.4.2            ← Data validation
python-dotenv==1.0.0       ← .env reading
aiohttp==3.9.0             ← HTTP requests
```

---

## 🚀 Advanced Usage

### Adding New Experiment
1. Open `src/scenarios/scenarios.py`
2. Create a new `ExperimentScenario`
3. Add it to the `SCENARIOS` dictionary
4. Restart the server

### Adding New Agent
1. Create a new file in `src/agents/`
2. Extend the `BaseAgent` class
3. Write `think()` and `evaluate()` methods
4. Add it to `app.py`

---

## ✅ Checklist

- [ ] Is Python 3.8+ installed?
- [ ] Is `venv` created?
- [ ] Are dependencies installed?
- [ ] Is `.env` file created?
- [ ] Is OpenAI API key added?
- [ ] Is server started?
- [ ] Is demo script run?
- [ ] Is http://127.0.0.1:8000/docs visited?

---

## 💡 Tips

- Use `--reload` flag during development
- Use Swagger UI for writing queries (easier)
- Examine demo.py to get examples
- Use LOG_LEVEL=DEBUG to see errors

---

**Ready? Type `uvicorn app:app --reload` and start! 🎉**
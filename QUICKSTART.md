"""
# CSGirlies-AILAB Quick Start Guide

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd CSGirlies-AILAB
```

### 2. Create Python Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\\Scripts\\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys:
# - OPENAI_API_KEY: Your OpenAI API key (from https://platform.openai.com/api-keys)
# - WOLFRAM_APPID: Your Wolfram API App ID (from https://www.wolfram.com/cloud/)
# - GITBOOK_API_KEY: Your GitBook API key (optional, for documentation)
```

## Running the Application

### Start the FastAPI Server
```bash
uvicorn app:app --reload
```

The server will start at `http://127.0.0.1:8000`

### Access the API Documentation
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Run the Demo
In a new terminal (with venv activated):
```bash
python demo.py
```

This will demonstrate the full workflow:
1. List available experiments
2. Get experiment details
3. Start an experiment session
4. Interact with the AI lab partner
5. Complete the experiment and generate documentation

## Project Structure

```
CSGirlies-AILAB/
├── app.py                      # Main FastAPI application
├── demo.py                     # Interactive demo script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── LICENSE                    # Project license
├── README.md                  # Main documentation
├── prd.md                     # Product Requirements Document
├── requirement_analysis.md    # Detailed requirements
│
├── src/
│   ├── __init__.py
│   ├── config.py             # Configuration management
│   │
│   ├── agents/               # Multi-agent system
│   │   ├── base.py          # Base agent class
│   │   ├── partner.py       # Lab partner agent
│   │   ├── mentor.py        # Mentor/guide agent
│   │   ├── evaluator.py     # Evaluator agent
│   │   └── __init__.py
│   │
│   ├── scenarios/            # Experiment scenarios
│   │   ├── scenarios.py     # Scenario definitions
│   │   └── __init__.py
│   │
│   ├── wolfram_engine/      # Wolfram computation
│   │   ├── engine.py        # Wolfram integration
│   │   └── __init__.py
│   │
│   ├── integrations/        # External service integrations
│   │   ├── gitbook.py       # GitBook documentation
│   │   └── __init__.py
│   │
│   └── utils/               # Utility functions
│       ├── helpers.py
│       └── __init__.py
│
├── experiments/             # Experiment scenario files
├── docs/                   # Documentation
└── .gitignore             # Git ignore file
```

## Key Features

### 🤖 Multi-Agent System
- **Partner Agent**: Interactive lab companion who discusses and collaborates
- **Mentor Agent**: Provides guidance, detects misconceptions
- **Evaluator Agent**: Assesses learning outcomes

### 🔬 Three Core Experiments
1. **Acid-Base Titration** (Chemistry) - Determine unknown acid concentration
2. **Hooke's Law** (Physics) - Determine spring constant experimentally
3. **Osmosis** (Biology) - Observe water movement across membranes

### 📊 Wolfram Integration
- Real-time graphing and computations
- pH curves, force-displacement graphs, osmotic pressure calculations
- Visual results for each experiment

### 📚 GitBook Integration
- Automatic documentation generation
- Experiment reports created automatically
- Learning outcomes tracked

## API Endpoints

### Experiment Management
- `GET /experiments` - List all experiments
- `GET /experiments/{experiment_id}` - Get experiment details

### Experiment Interaction
- `POST /simulate/start` - Start new experiment session
- `POST /simulate/interact` - Process student input and get responses
- `POST /simulate/complete` - Complete session and generate documentation

### System
- `GET /` - Welcome message
- `GET /health` - Health check

## Example API Usage

### 1. Start an Experiment
```bash
curl -X POST "http://localhost:8000/simulate/start" \\
  -H "Content-Type: application/json" \\
  -d '{
    "experiment_id": "chem_titration",
    "level": "beginner",
    "student_name": "Alex"
  }'
```

### 2. Student Interaction
```bash
curl -X POST "http://localhost:8000/simulate/interact" \\
  -H "Content-Type: application/json" \\
  -d '{
    "session_id": "<session_id>",
    "experiment_id": "chem_titration",
    "student_message": "I pipetted 20 mL of acid",
    "current_step": 2
  }'
```

### 3. Complete Experiment
```bash
curl -X POST "http://localhost:8000/simulate/complete" \\
  -H "Content-Type: application/json" \\
  -d '{
    "session_id": "<session_id>",
    "experiment_id": "chem_titration"
  }'
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here

# Wolfram Configuration
WOLFRAM_APPID=your-app-id-here

# GitBook Configuration (optional)
GITBOOK_API_KEY=your-gitbook-key
GITBOOK_SPACE_ID=your-space-id

# Server Configuration
HOST=127.0.0.1
PORT=8000
DEBUG=True
LOG_LEVEL=INFO
```

## Development

### Adding New Experiments
1. Create a new scenario in `src/scenarios/scenarios.py`
2. Define scenario structure with learning objectives, materials, steps
3. Add Wolfram computations for graphing/calculations
4. Register in the SCENARIOS dictionary

### Adding New Agents
1. Create agent class extending `BaseAgent`
2. Implement `think()` and `evaluate()` methods
3. Configure system prompt and personality
4. Register in main app.py

### Running Tests
```bash
pytest tests/
```

## Troubleshooting

### OpenAI API Error
- Check that OPENAI_API_KEY is set correctly
- Verify API key has sufficient credits
- Check API key permissions

### Wolfram Computation Error
- Verify WOLFRAM_APPID is correct
- Check Wolfram Cloud account status
- Sample graphs provided if API not available

### GitBook Documentation Missing
- GitBook integration is optional
- System works without GITBOOK_API_KEY
- Documentation preview still available in responses

## Performance & Limitations

- Response times: 2-5 seconds per interaction (API calls)
- Maximum conversation length: 5 messages per agent
- Wolfram computations: Pre-computed samples if API rate limited
- Concurrent sessions: Limited by API rate limits

## Future Enhancements

- [ ] Web-based UI for student interface
- [ ] Real-time collaboration features
- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] More experiment scenarios (50+)
- [ ] VR/AR lab simulation
- [ ] Learning management system (LMS) integration

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact & Support

For questions or support:
- GitHub Issues: Report bugs and request features
- Documentation: See README.md and prd.md
- Feedback: We welcome suggestions for improvements

---

**Built with ❤️ by CSGirlies Team**

*Making science education accessible, engaging, and fun!*
"""

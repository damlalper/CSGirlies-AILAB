#!/usr/bin/env python
"""
CSGirlies-AILAB Setup & Configuration Guide
This script helps you set up the project and validate all components
"""

import os
import sys
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def check_python_version():
    """Check Python version"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version OK (3.8+)")
        return True
    else:
        print("❌ Python 3.8+ required")
        return False


def check_virtual_environment():
    """Check if running in virtual environment"""
    print_header("Checking Virtual Environment")
    
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if in_venv:
        print("✅ Running in virtual environment")
        return True
    else:
        print("⚠️  Not in virtual environment")
        print("   Recommended: python -m venv venv")
        print("   Then: source venv/bin/activate (or venv\\Scripts\\activate on Windows)")
        return False


def check_project_structure():
    """Check if project structure is complete"""
    print_header("Checking Project Structure")
    
    required_dirs = [
        "src",
        "src/agents",
        "src/scenarios",
        "src/wolfram_engine",
        "src/integrations",
        "src/utils",
        "experiments",
        "docs"
    ]
    
    required_files = [
        "app.py",
        "demo.py",
        "requirements.txt",
        ".env.example",
        "README.md",
        "prd.md",
        "requirement_analysis.md"
    ]
    
    all_ok = True
    
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ❌ {dir_path}/ (missing)")
            all_ok = False
    
    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (missing)")
            all_ok = False
    
    return all_ok


def check_dependencies():
    """Check installed dependencies"""
    print_header("Checking Dependencies")
    
    required = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'openai',
        'python-dotenv'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (not installed)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    return True


def check_env_file():
    """Check .env file"""
    print_header("Checking Environment Configuration")
    
    if os.path.isfile('.env'):
        print("✅ .env file exists")
        
        with open('.env', 'r') as f:
            content = f.read()
            
        checks = {
            'OPENAI_API_KEY': 'OpenAI API Key' in content,
            'WOLFRAM_APPID': 'Wolfram App ID' in content,
        }
        
        for key, found in checks.items():
            if found and not key.endswith('=xxxx') and not key.endswith('=sk-xxxx'):
                print(f"  ✅ {key} configured")
            else:
                print(f"  ⚠️  {key} not fully configured")
        
        return True
    else:
        print("⚠️  .env file not found")
        print("   Run: cp .env.example .env")
        print("   Then edit .env with your API keys")
        return False


def print_setup_instructions():
    """Print setup instructions"""
    print_header("Setup Instructions")
    
    instructions = """
1. CREATE VIRTUAL ENVIRONMENT
   python -m venv venv
   
   Activate:
   - Windows: venv\\Scripts\\activate
   - macOS/Linux: source venv/bin/activate

2. INSTALL DEPENDENCIES
   pip install -r requirements.txt

3. CONFIGURE ENVIRONMENT
   cp .env.example .env
   
   Edit .env and add:
   - OPENAI_API_KEY (from https://platform.openai.com/api-keys)
   - WOLFRAM_APPID (from https://www.wolfram.com/cloud/)

4. START THE SERVER
   uvicorn app:app --reload
   
   Server will run at: http://127.0.0.1:8000

5. RUN THE DEMO
   In another terminal:
   python demo.py

6. EXPLORE THE API
   Visit: http://127.0.0.1:8000/docs (Swagger UI)
   Or: http://127.0.0.1:8000/redoc (ReDoc)
"""
    print(instructions)


def print_project_overview():
    """Print project overview"""
    print_header("CSGirlies-AILAB - Project Overview")
    
    overview = """
PROJECT: AI Simulated Lab Partner
PURPOSE: Interactive science education platform with AI agents

CORE COMPONENTS:
  🤖 Multi-Agent System
     - Partner Agent: Lab companion with natural conversation
     - Mentor Agent: Guide who detects misconceptions
     - Evaluator Agent: Assesses learning outcomes

  🔬 Three Science Experiments
     - Acid-Base Titration (Chemistry)
     - Hooke's Law (Physics)
     - Osmosis (Biology)

  📊 Wolfram Integration
     - Real-time computation
     - Graph generation
     - Scientific analysis

  📚 GitBook Integration
     - Automatic documentation
     - Learning outcome tracking

KEY FEATURES:
  ✅ Conversational AI interaction
  ✅ Real-time scientific computation
  ✅ Automatic documentation generation
  ✅ Multi-subject support
  ✅ Home-based learning accessibility
  ✅ Game-like engagement

API ENDPOINTS (7 total):
  GET  /                      - Welcome
  GET  /experiments           - List experiments
  GET  /experiments/{id}      - Get experiment details
  POST /simulate/start        - Start experiment
  POST /simulate/interact     - Student interaction
  POST /simulate/complete     - Complete & document
  GET  /health                - Health check

TECH STACK:
  Backend: FastAPI + Uvicorn
  AI: OpenAI GPT-4
  Computation: Wolfram Cloud
  Documentation: GitBook
  Language: Python 3.8+
"""
    print(overview)


def print_quick_start():
    """Print quick start guide"""
    print_header("Quick Start")
    
    quick_start = """
WINDOWS USERS:

1. Open PowerShell in project directory

2. Create virtual environment:
   python -m venv venv

3. Activate it:
   venv\\Scripts\\activate

4. Install dependencies:
   pip install -r requirements.txt

5. Configure environment:
   cp .env.example .env
   # Edit .env with your API keys

6. Run the server:
   uvicorn app:app --reload

7. In another PowerShell, run demo:
   python demo.py

8. Visit API docs:
   http://127.0.0.1:8000/docs

---

MACOS/LINUX USERS:

1. Open Terminal in project directory

2. Create virtual environment:
   python3 -m venv venv

3. Activate it:
   source venv/bin/activate

4. Install dependencies:
   pip install -r requirements.txt

5. Configure environment:
   cp .env.example .env
   # Edit .env with your API keys

6. Run the server:
   uvicorn app:app --reload

7. In another terminal, run demo:
   python demo.py

8. Visit API docs:
   http://127.0.0.1:8000/docs
"""
    print(quick_start)


def main():
    """Run all checks and display information"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  CSGirlies-AILAB - Setup & Configuration Guide  ".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    # Run checks
    py_ok = check_python_version()
    venv_ok = check_virtual_environment()
    struct_ok = check_project_structure()
    deps_ok = check_dependencies()
    env_ok = check_env_file()
    
    # Print guides
    print_project_overview()
    print_setup_instructions()
    print_quick_start()
    
    # Summary
    print_header("Setup Summary")
    
    all_checks = {
        "Python 3.8+": py_ok,
        "Virtual Environment": venv_ok,
        "Project Structure": struct_ok,
        "Dependencies": deps_ok,
        "Environment File": env_ok
    }
    
    passed = sum(1 for v in all_checks.values() if v)
    total = len(all_checks)
    
    for check, result in all_checks.items():
        status = "✅" if result else "⚠️"
        print(f"  {status} {check}")
    
    print(f"\nStatus: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✅ All checks passed! Ready to start:")
        print("   1. Configure your .env file with API keys")
        print("   2. Run: uvicorn app:app --reload")
        print("   3. Run: python demo.py")
    else:
        print("\n⚠️  Some checks failed. Please fix before starting.")
    
    print("\n📚 Documentation:")
    print("   - README.md: Main documentation")
    print("   - QUICKSTART.md: Detailed setup guide")
    print("   - PROJECT_SUMMARY.md: Project overview")
    print("   - docs/ARCHITECTURE.md: System architecture")
    print("\n")


if __name__ == "__main__":
    main()

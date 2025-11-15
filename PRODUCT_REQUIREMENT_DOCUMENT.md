# 📘 AI Simulated Lab Partner — Product Requirement Document (PRD)

## 🎯 Product Vision
An interactive experiment simulation system, multi-agent + Wolfram supported, where every student can experience physics/chemistry/biology experiments as if they were doing them with a real partner.

**Goal:** To recreate the experience of real laboratory learning at home, even with limited resources.

---

## 🧪 Core Features

### 1) AI Lab Partner (Primary Agent)
- Chats with the student, discusses, makes mistakes, and produces solutions together.
- Gives the feeling of a "human partner."
- **Personality:** curious, slightly impatient, motivating.
- Depending on the situation:
  - Gives ideas
  - Advocates for the wrong thing (for the student to realize mistakes)
  - Plans experiments together

### 2) Mentor Agent (Overseer)
- Evaluates the conversations of the Partner and the student.
- Detects misconceptions.
- Gives small hints to the student.
- Corrects when necessary.

### 3) Experiment Engine (Wolfram Core)
- For each experiment:
  - Calculations
  - Graphs (pH, velocity, energy, momentum, temperature, etc.)
  - Simulation results
  - Instant result generation when experiment parameters change

### 4) Scenario System
- Student selects an experiment → system creates a dynamic scenario.
- Example:
  - Chemistry: Acid-Base titration
  - Physics: Hooke's law measurement
  - Biology: Simulation of substance passage through cell membrane

---

## 🌍 Why This Project Wins?
- Educational impact: high
- Fun → draws the student in
- Technical depth: multi-agent + Wolfram computation
- UX: like a game
- Innovation: real partner simulation
- Accessibility: ideal for students without laboratory access at home

---

# 📘 README.md

## 🧪 AI Simulated Lab Partner
Your personal interactive science lab buddy — built with OpenAI, Wolfram, Cline CLI, GitBook

### 🚀 Overview
AI Simulated Lab Partner is an educational tool that allows you to interactively perform physics/chemistry/biology experiments as if you were working with a real partner. The system is built on a multi-agent architecture, Wolfram real-time computation, Cline CLI automation pipeline, and GitBook dynamic documentation.

### ✨ Features
- 🧍 **AI Lab Partner** – discusses, makes mistakes, generates ideas
- 🧠 **Mentor Agent** – guides, corrects mistakes
- 🔬 **Wolfram Simulation Engine** – graphs, calculations, experiment results
- 📚 **Dynamic GitBook** – each experiment is automatically created on GitBook
- 🔧 **Cline CLI Workflow** – generates content automatically from scenario files
- 🎮 **Interactive Experience** – system that reacts like a real partner

### 🛠 Tech Stack

| Technology | Usage |
|-----------|---------|
| OpenAI GPT-4.2/5 Agents | Partner, Mentor, Evaluator |
| Wolfram Cloud | Real-time experiment calculation & graph |
| Cline CLI | Scenario → Agents → GitBook pipeline |
| GitBook API | Dynamic documentation |
| FastAPI | Backend & agent routing |
| Claude / Gemini | Alternative reasoning agents |

### 🏗 Installation
```bash
git clone <repo>
cd ai-lab-partner
pip install -r requirements.txt
cp .env.example .env
# Fill in OPENAI_API_KEY, WOLFRAM_APPID
uvicorn app:server --reload
```
📐 System Architecture
             +--------------------+
             |   GitBook Client   |
             +--------------------+
                      |
                      v
------------------------------------------------------
|                     API Server                     |
|  (FastAPI + Router + Webhooks)                     |
------------------------------------------------------
   |                 |                   |
   v                 v                   v
Partner Agent   Mentor Agent       Evaluator Agent
   |                 |                   |
   ----------- Multi-Agent Layer ---------
                      |
                      v
             Wolfram Compute Engine
                      |
                      v
           Experiment Simulation Output


# 📘 Tech Stack & Why

### OpenAI Agents
- The system that best imitates human partner behavior

### Wolfram
- Numerical accuracy
- Graph generation
- Formula-based experiment simulation

### Cline CLI
- Run GitBook + scenario + agent pipeline with a single command

### GitBook
- Automatic documentation of student experiments
- Creating an educational platform

---

# 📘 API SPEC

## POST /simulate
Starts a scenario.

**Body:**
```json
{
  "experiment": "acid_base_titration",
  "level": "beginner"
}
```
Response:
```json
{
  "partner": "Today we are doing titration!",
  "mentor": "First, let's determine what we want to measure.",
  "wolfram_graph": "<base64 svg>"
}
```

📘 Multi-Agent Design
Partner Agent
Persona: fun, talkative, slightly competitive
Goal: to make decisions together with the student

Prompt:
You are an AI lab partner. You think like a human, talk like a student, and sometimes make mistakes to encourage discussion.

Mentor Agent
Analyzes every dialogue
Evaluates Partner + student interaction
Gives mini lessons when necessary
Evaluator Agent
Did the student understand?
Marks misconceptions if any

📘 Wolfram Module
Example: Titration
Plot[pH[x], {x,0,20}]

Example: Hooke’s Law
Plot[k x, {x,0,10}]

📘 GitBook Structure
/experiments
   /physics
      - hookes-law.md
   /chemistry
      - titration.md
   /biology
      - osmosis.md

Cline CLI automatically updates on each run:
cline build-experiment titration.scn

📘 Cline CLI Automation

Pipeline:
experiment.scn → agents → wolfram → markdown → GitBook push


Command:
cline run pipeline --scenario titration.scn

📘 Demo Script (For Judges)

Student: "I want to do acid-base titration."
Partner: "Great! Shall we prepare the solutions first?"
Mentor: "First, the objective: to find the molarity of the acid."
Student enters volume
Wolfram produces graph
Partner interprets graph
Experiment automatically created in GitBook
Judges: wow effect

📘 Roadmap
Day-1 Deliverables (Sufficient for Hackathon)
3 experiment scenarios
Partner + Mentor agent
Wolfram-supported graph
GitBook dynamic page
CLI pipeline

📘 Prompt Pack
Dev prompt for Claude/GPT
You are the "AI Lab Partner System". You receive experiment scenarios and generate partner dialogue, mentor guidance and Wolfram computation instructions. Maintain personality. Encourage discussion. Avoid giving full solutions immediately.
# 📄 Requirement Analysis — AI Simulated Lab Partner

## 🔍 1. Inputs

### 1.1 Business Goals
- Enable students to perform physics/chemistry/biology experiments at home, simulating a real laboratory experience.  
- Improve students' learning speed, comprehension quality, and experiential learning level.  
- Provide equal opportunities for schools and students without laboratory access.  
- With AI-supported interaction:  
  - Develop a “partner” behavior that can make mistakes, generate ideas, and engage in discussions.  
  - Make the learning process fun, curiosity-driven, and gamified.  
- Deliver an innovative, technically robust, and user-friendly demo that meets judging criteria.

### 1.2 Existing Processes and Systems
The project builds on existing technologies usable within the hackathon:  
- **OpenAI Agents:** Multi-agent framework, reasoning, role-based behavior  
- **Wolfram Cloud:** Scientific computation, graphics, simulation  
- **Cline CLI:** Build pipeline, GitBook automation, developer workflow  
- **GitBook:** Content management and dynamic documentation  
- **FastAPI:** Backend routing  

> These infrastructures exist and do not need to be rewritten for the project; integration is sufficient.

### 1.3 Stakeholders

| Stakeholder | Role | Expectations |
|------------|------|-------------|
| Students | End user | Support for experiential learning, interactive partner, ease of use |
| Teachers | Evaluator | Learning reports, error detection |
| Technical Team | Developer | Easy integration, API stability, modular architecture |
| Jury Members | Evaluator | Educational impact, innovation, technical depth, UX |
| Hackathon Organization | Sponsor/Admin | Functional demo, proper documentation |

### 1.4 Time and Budget Constraints
- **Time:** 1 day (hackathon duration)  
- **Budget:** Minimal, free, or low-cost API usage (OpenAI/Wolfram free tiers)  
- **Development Speed:** Should rely on ready-made frameworks and APIs  

> Due to time constraints:  
> - A functional prototype is preferred over a full UI  
> - 3 core experiments are sufficient initially  
> - Multi-agent system should be implemented at a minimal-viable level  

### 1.5 Success Criteria
- ✔ Demo must be fully operational  
- ✔ Realistic dialogue flow between student and partner  
- ✔ Mentor agent can detect mistakes  
- ✔ At least one Wolfram graph/calculation is shown during the demo  
- ✔ Automatic creation of the experiment page on GitBook  
- ✔ The system should convey “enhanced learning experience”  
- ✔ Jury should recognize technical challenges have been solved  

---

## 📤 2. Outputs

### 2.1 Scope Definition

**To Be Delivered:**  
- Multi-agent lab assistant simulation system  
- Partner + Mentor + Evaluator agents  
- Scenario files for 3 experiments  
- Wolfram computations (graphs + numeric outputs)  
- GitBook automatic update pipeline  
- Full automation via Cline CLI commands  
- Minimum demo endpoint on FastAPI  

**Not Included:**  
- Real 3D lab environment (future possibility)  
- Mobile application  
- Detailed user management  
- Large experiment library (>20)  
- Full-featured teacher panel  

### 2.2 Prioritized Requirements (MoSCoW)

**Must Have**  
- Partner agent  
- Mentor agent  
- 1 physics + 1 chemistry + 1 biology experiment scenario  
- Wolfram graph (at least 1)  
- FastAPI endpoint  
- GitBook integration  
- Cline CLI build pipeline  

**Should Have**  
- Evaluator agent  
- Misconception analysis  
- Automatic experiment report creation in GitBook  

**Could Have**  
- Simple web interface  
- Student performance metrics  
- Additional experiments  

**Won’t Have (This Version)**  
- VR/AR lab simulation  
- Multi-student collaboration  
- LMS integration  

### 2.3 Timebox Plan & Roadmap

| Time | Task |
|------|------|
| 0–2 hours | Create files, repo setup, environment, FastAPI skeleton |
| 2–5 hours | Develop Partner and Mentor agents |
| 5–7 hours | Wolfram integration, graph generation |
| 7–9 hours | GitBook integration + Cline CLI pipeline |
| 9–11 hours | Write three experiment scenarios |
| 11–13 hours | Demo flow, testing |
| 13–24 hours | Presentation and final documentation |

### 2.4 Risks & Dependencies

| Risk | Impact | Likelihood | Mitigation |
|------|-------|-----------|------------|
| Wolfram API rate limit | High | Medium | Pre-generate example graph cache |
| OpenAI agent errors | Medium | Medium | Prompt tweaking + role separation |
| GitBook API connection issues | Medium | Low | Manual fallback export |
| Time constraints | High | High | MVP approach, scope reduction |
| Scenarios too technical | Medium | Low | Start with simple experiments |

### 2.5 Key Success Metrics / KPIs
- 100% working demo  
- 3 experiments visible on GitBook  
- At least 3 graphs generated via Wolfram  
- Natural interaction from Partner and Mentor agents  
- Students follow experiment steps correctly  
- Demo completed without errors in jury test  
- “Wow effect” during demo (qualitative KPI)

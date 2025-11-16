# 📸 Screenshot Guide for CS Girlies Hackathon Submission

## 🎯 Required Screenshots

### For Cline CLI Track ($1,500 Prize)

#### Screenshot 1: Help Menu
```bash
python cline.py --help
```
**What to capture:** Full command output showing all 7 commands
**Filename:** `screenshot_1_cline_help.png`

---

#### Screenshot 2: Health Check
```bash
python cline.py health
```
**What to capture:** System health check with all green checkmarks
**Filename:** `screenshot_2_cline_health.png`

---

#### Screenshot 3: Start Command
```bash
python cline.py start
```
**What to capture:** Both servers starting (Backend + Frontend)
**Filename:** `screenshot_3_cline_start.png`
**Note:** Let it run for ~5 seconds to show both servers initialized

---

#### Screenshot 4: Test Results
```bash
python cline.py test
```
**What to capture:** Test summary showing 14 passed tests
**Filename:** `screenshot_4_cline_test.png`

---

### For Application Screenshots

#### Screenshot 5: Experiment Selection Screen
**URL:** http://localhost:3000
**What to capture:** Homepage showing 3 available experiments
**Filename:** `screenshot_5_home.png`

---

#### Screenshot 6: AI Conversation
**URL:** http://localhost:3000 (during experiment)
**Steps:**
1. Select "Acid-Base Titration"
2. Have a 2-3 message conversation
3. Capture showing Partner and Mentor responses

**What to capture:** Active experiment with AI messages visible
**Filename:** `screenshot_6_ai_conversation.png`

---

#### Screenshot 7: Wolfram Graph
**URL:** http://localhost:3000 (complete experiment)
**Steps:**
1. Complete an experiment
2. Wolfram graph should display

**What to capture:** Dynamic pH curve or force-displacement graph
**Filename:** `screenshot_7_wolfram_graph.png`

---

#### Screenshot 8: Lab Report
**Path:** Open file in `lab_reports/` folder
**What to capture:** Generated markdown lab report in text editor
**Filename:** `screenshot_8_lab_report.png`

---

## 🖥️ How to Take Screenshots

### Windows:
1. **Snipping Tool:** `Win + Shift + S` → Select area → Auto-copies to clipboard
2. **Full Screen:** `PrtScn` → Opens in Paint → Save
3. **Active Window:** `Alt + PrtScn` → Paste in Paint → Save

### Mac:
1. **Selected Area:** `Cmd + Shift + 4` → Drag to select
2. **Full Screen:** `Cmd + Shift + 3`
3. **Window:** `Cmd + Shift + 4` then `Space` → Click window

### Linux:
1. **Gnome:** `Shift + PrtScn` for area selection
2. **KDE:** Use Spectacle (`Shift + PrtScn`)

---

## 📝 Quick Capture Workflow

### Step 1: Prepare Terminal
```bash
# Clear terminal for clean screenshots
clear

# Run each command and capture
python cline.py --help          # Screenshot 1
python cline.py health          # Screenshot 2
python cline.py start           # Screenshot 3 (let run 5 sec)
# Ctrl+C to stop
python cline.py test            # Screenshot 4
```

### Step 2: Prepare Application
```bash
# Start servers (in separate terminal)
python cline.py start

# Wait for both to start, then:
# Open browser: http://localhost:3000
```

### Step 3: Capture Application Flow
1. Home page → Screenshot 5
2. Select experiment → Chat with AI → Screenshot 6
3. Complete experiment → Show graph → Screenshot 7
4. Open `lab_reports/` folder → Open .md file → Screenshot 8

---

## 🎨 Screenshot Quality Tips

### DO:
✅ Use full resolution (don't resize before capturing)
✅ Ensure text is readable
✅ Capture full terminal output
✅ Use clean, professional setup
✅ Include relevant parts (avoid excess whitespace)

### DON'T:
❌ Don't show personal info (emails, API keys visible)
❌ Don't have cluttered desktop in background
❌ Don't use low resolution
❌ Don't crop important information
❌ Don't show errors unless explaining fixes

---

## 📊 DevPost Upload Order

**In "Project Media" section, upload in this order:**

1. `screenshot_1_cline_help.png` - CLI Help Menu
2. `screenshot_2_cline_health.png` - Health Check
3. `screenshot_3_cline_start.png` - Server Start
4. `screenshot_4_cline_test.png` - Test Results
5. `screenshot_5_home.png` - Experiment Selection
6. `screenshot_6_ai_conversation.png` - AI Interaction
7. `screenshot_7_wolfram_graph.png` - Wolfram Computation
8. `screenshot_8_lab_report.png` - Generated Report

**Add captions for each:**
1. "Cline CLI - 7 automation commands for complete project lifecycle"
2. "Health check validating all API keys and dependencies"
3. "Concurrent server startup - Backend + Frontend in parallel"
4. "Comprehensive test suite - 14/21 tests passing"
5. "Interactive experiment selection - 3 complete scenarios"
6. "Multi-agent AI collaboration - Partner + Mentor guidance"
7. "Dynamic Wolfram computation - Real-time scientific graphs"
8. "Automatic lab report generation - Complete session documentation"

---

## 🎬 Demo Video Script (5 minutes)

### 0:00-1:00 - Problem & Solution
**Show:** Title slide + Problem statistics
**Say:** "700M students lack lab access. CSGirlies-AILAB makes science accessible."

### 1:00-2:30 - Experiment Walkthrough
**Show:** Select experiment → AI conversation → Complete
**Say:** "Interactive AI partner guides students through real experiments."

### 2:30-3:30 - AI Agents Showcase
**Show:** Partner asking "What if" → Mentor guidance → Evaluator feedback
**Say:** "3 specialized agents create authentic learning experience."

### 3:30-4:15 - Wolfram Integration
**Show:** Input parameters → Graph generation → Results
**Say:** "Real-time scientific computation with dynamic visualizations."

### 4:15-4:45 - GitBook Reports
**Show:** Complete experiment → Report generated → Open file
**Say:** "Automatic documentation captures entire learning session."

### 4:45-5:00 - Cline CLI Demo
**Show:** `python cline.py --help` → `python cline.py start`
**Say:** "Professional CLI automation - setup to deployment in one command."

---

## ✅ Final Checklist

Before submission:

- [ ] All 8 screenshots captured
- [ ] Screenshots are high quality (readable text)
- [ ] No sensitive information visible (API keys, emails)
- [ ] Filenames are clear and numbered
- [ ] Captions prepared for each image
- [ ] Demo video recorded (5 minutes)
- [ ] Video uploaded to YouTube/Vimeo
- [ ] GitHub repository is public
- [ ] README.md is complete

---

## 🚀 Pro Tips

**Make it stand out:**
- Use consistent window sizes across screenshots
- Ensure good contrast (light text on dark terminal or vice versa)
- Capture at peak moments (graph fully rendered, AI mid-response)
- Show real data and conversations (not placeholders)

**For CLI screenshots:**
- Use a clean terminal (no previous errors visible)
- Maximize terminal window for full output
- Let colorized output show clearly

**For app screenshots:**
- Show real experiment data
- Capture during active conversation (more engaging)
- Include progress bar showing >50% for visual interest

---

**You've got this! Your project is amazing - let the screenshots show it! 📸🚀**

*CSGirlies-AILAB Team*
*CS Girlies Hackathon 2024*

# 📊 Lab Reports - CSGirlies-AILAB

This directory contains automatically generated lab reports from completed experiment sessions.

## 🎯 What Are These Reports?

Every time a student completes an experiment using CSGirlies-AILAB, the system **automatically generates a comprehensive lab report** that includes:

- ✅ Complete conversation transcript with all AI agents (Partner, Mentor, Evaluator)
- ✅ Student observations recorded during the experiment
- ✅ Wolfram computational results with dynamic graphs
- ✅ Mentor guidance and learning insights
- ✅ Evaluator feedback and assessment
- ✅ Learning outcomes tracking
- ✅ "What if" questions explored during the session

## 📁 Sample Reports

### Available Sample Reports:

1. **[SAMPLE_Acid_Base_Titration_20241116.md](SAMPLE_Acid_Base_Titration_20241116.md)**
   - Complete titration experiment with pH curve
   - Shows dynamic Wolfram computation
   - Demonstrates proactive AI questioning
   - Includes detailed evaluation feedback

## 🔬 Report Structure

Each lab report follows this professional format:

```markdown
# Lab Report: [Experiment Name]

## Experiment Overview
- Learning objectives
- Materials used
- Procedure steps

## Session Transcript
- Complete conversation with Partner Agent
- Mentor guidance throughout
- Student responses and questions

## Student Observations
- Key insights captured by AI memory
- Important observations noted

## Wolfram Computational Results
- Real-time scientific calculations
- Dynamic graphs (pH curves, force-displacement, etc.)
- Mathematical analysis

## Evaluation & Feedback
- Overall performance assessment
- What went well
- Areas for improvement
- Next steps and recommendations

## Session Statistics
- Duration, messages, engagement metrics

## Learning Outcomes Achieved
- Mastery level tracking
```

## 🤖 How Reports Are Generated

**Automatic Generation Process:**

1. **Student completes experiment** through web interface
2. **System collects all data:**
   - Partner Agent conversation history
   - Mentor Agent guidance messages
   - Student observations and inputs
   - Wolfram computation results
   - Evaluator feedback
3. **GitBook integration creates comprehensive markdown report**
4. **Dual-save system:**
   - Local file saved to `lab_reports/` directory
   - Optionally published to GitBook documentation site

**Code Reference:** `src/integrations/gitbook.py` - `create_experiment_report()` method

## 📝 Report Naming Convention

```
[Experiment_Name]_[Session_ID]_[Timestamp].md

Examples:
- Acid_Base_Titration_abc123xyz_20241116_153042.md
- Hookes_Law_def456uvw_20241116_161520.md
- Osmosis_ghi789rst_20241116_174308.md
```

## 🎓 Educational Value

These reports serve multiple purposes:

### For Students:
- **Review:** Revisit experiment steps and insights
- **Study:** Prepare for exams with complete documentation
- **Portfolio:** Showcase lab work in applications
- **Learning:** See where they struggled and succeeded

### For Teachers:
- **Assessment:** Evaluate student understanding
- **Progress Tracking:** Monitor learning over time
- **Intervention:** Identify misconceptions early
- **Evidence:** Document hands-on learning

### For Researchers:
- **Analysis:** Study how students learn science
- **AI Evaluation:** Assess multi-agent effectiveness
- **Improvement:** Identify areas to enhance system

## 🔗 GitBook Integration

**Local + Cloud Documentation:**

- **Local Backup:** All reports saved in `lab_reports/` folder
- **GitBook Publish:** Optional automatic upload to GitBook documentation site
- **No API Key Required:** System works without GitBook API (local-only mode)
- **With API Key:** Reports automatically published and versioned

**Configuration:** See `.env` file for `GITBOOK_API_KEY` and `GITBOOK_SPACE_ID`

## 💻 Generating Your Own Reports

**Prerequisites:**
```bash
# 1. Start the application
python cline.py start

# 2. Open browser
# Navigate to http://localhost:3000
```

**Steps:**
1. Select an experiment (Acid-Base Titration, Hooke's Law, or Osmosis)
2. Complete all experiment steps by chatting with AI lab partner
3. Click "Complete Experiment" button
4. Report is automatically generated!

**Find Your Report:**
```bash
# Reports are saved here:
ls lab_reports/

# Example output:
# Acid_Base_Titration_session123_20241116_153042.md
# Hookes_Law_session456_20241116_161520.md
```

## 📊 Statistics

**What's Captured:**
- Total messages exchanged
- Session duration
- Steps completed
- Wolfram queries executed
- Observations recorded
- "What if" questions asked
- Misconceptions corrected
- Overall engagement level

## 🏆 Bonus Track: GitBook Documentation Prize

This automatic lab report generation system competes for the **GitBook Best Documentation Prize ($500)** at CS Girlies Hackathon.

**Why It Qualifies:**
- ✅ Automatic generation (zero effort for students)
- ✅ Comprehensive content (full session capture)
- ✅ Professional formatting (markdown with structure)
- ✅ GitBook API integration
- ✅ Local backup system
- ✅ Educational value (real learning documentation)

## 📚 Technology Stack

**Report Generation:**
- Python markdown templating
- Pydantic data models for structure
- GitBook API for publishing
- Local file system for backup

**Data Sources:**
- Partner Agent conversation history
- Mentor Agent guidance logs
- Evaluator Agent feedback
- Wolfram Engine computation results
- Session state management

## 🔮 Future Enhancements

Planned improvements for lab reports:

- [ ] PDF export option
- [ ] Interactive graphs (Plotly.js)
- [ ] Comparison with past sessions
- [ ] Teacher annotations
- [ ] Peer review features
- [ ] Grade tracking integration

## 📞 Support

**Questions about lab reports?**

- Check main documentation: [README.md](../README.md)
- Review GitBook integration code: [src/integrations/gitbook.py](../src/integrations/gitbook.py)
- Open GitHub issue: [Issues](https://github.com/your-username/CSGirlies-AILAB/issues)

---

**Built with ❤️ by CSGirlies Team**
*Making Science Education Accessible Through AI*
**CS Girlies Hackathon 2024**

---

## 📖 Related Documentation

- **Main README:** [../README.md](../README.md)
- **Submission Materials:** [../SUBMISSION_MATERIALS.md](../SUBMISSION_MATERIALS.md)
- **Screenshot Guide:** [../SCREENSHOT_GUIDE.md](../SCREENSHOT_GUIDE.md)
- **Product Requirements:** [../docs/PRODUCT_REQUIREMENT_DOCUMENT.md](../docs/PRODUCT_REQUIREMENT_DOCUMENT.md)

---

*Last Updated: 2024-11-16*

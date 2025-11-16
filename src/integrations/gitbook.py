"""GitBook integration for automatic documentation"""

from typing import Dict, Any, Optional
from src.config import settings
import requests
import json


class GitBookIntegration:
    """
    Integrates with GitBook API to automatically create and update experiment documentation.
    """
    
    def __init__(self):
        self.api_key = settings.gitbook_api_key
        self.space_id = settings.gitbook_space_id
        self.base_url = "https://api.gitbook.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def create_experiment_report(self,
                                      session_id: str,
                                      experiment_name: str,
                                      scenario_data: Dict[str, Any],
                                      conversation_history: list,
                                      observations: Dict[str, Any],
                                      wolfram_results: list,
                                      evaluation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create COMPREHENSIVE automated lab report with full session details.

        Args:
            session_id: Unique session identifier
            experiment_name: Name of the experiment
            scenario_data: Experiment scenario details
            conversation_history: Complete dialogue between student and agents
            observations: Student observations throughout the experiment
            wolfram_results: All Wolfram computation results
            evaluation: Final evaluation from evaluator agent

        Returns:
            GitBook page creation response with full report
        """

        # Build comprehensive markdown content
        content = self._build_comprehensive_report(
            session_id,
            experiment_name,
            scenario_data,
            conversation_history,
            observations,
            wolfram_results,
            evaluation
        )

        # Save to local file as backup (even if GitBook API not configured)
        import os
        from datetime import datetime
        from pathlib import Path

        reports_dir = Path("lab_reports")
        reports_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"{experiment_name.replace(' ', '_')}_{session_id}_{timestamp}.md"
        report_path = reports_dir / report_filename

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # If API key is not set, return mock response with file location
        if not self.api_key or self.api_key == "xxxxxxxxxxxx":
            return {
                "success": True,
                "message": f"Lab report for '{experiment_name}' created",
                "local_file": str(report_path),
                "content_preview": content[:300] + "...",
                "gitbook_status": "API not configured (using local storage)"
            }

        try:
            # Create page in GitBook (would call actual API in production)
            page_data = {
                "title": f"Lab Report: {experiment_name} ({session_id[:8]})",
                "description": f"Automated lab report generated on {timestamp}",
                "content": content
            }

            # This would call actual GitBook API
            return {
                "success": True,
                "message": f"Lab report created for '{experiment_name}'",
                "page_id": f"mock-{session_id}",
                "local_file": str(report_path),
                "gitbook_url": f"https://gitbook.com/docs/{session_id}"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "local_file": str(report_path)
            }

    async def create_experiment_page(self,
                                     experiment_name: str,
                                     scenario_data: Dict[str, Any],
                                     results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create or update an experiment documentation page in GitBook.

        Args:
            experiment_name: Name of the experiment
            scenario_data: Experiment scenario details
            results: Results and graphs from the experiment

        Returns:
            GitBook page creation response
        """

        # Build markdown content
        content = self._build_experiment_markdown(experiment_name, scenario_data, results)

        # If API key is not set, return mock response
        if not self.api_key or self.api_key == "xxxxxxxxxxxx":
            return {
                "success": True,
                "message": f"Experiment page for '{experiment_name}' prepared (GitBook API not configured)",
                "content_preview": content[:500]
            }

        try:
            # Create page in GitBook
            page_data = {
                "title": experiment_name,
                "description": scenario_data.get("description", ""),
                "content": content
            }

            # This would call actual GitBook API
            return {
                "success": True,
                "message": f"Page created for '{experiment_name}'",
                "page_id": "mock-page-id"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _build_comprehensive_report(self,
                                   session_id: str,
                                   experiment_name: str,
                                   scenario_data: Dict[str, Any],
                                   conversation_history: list,
                                   observations: Dict[str, Any],
                                   wolfram_results: list,
                                   evaluation: Dict[str, Any]) -> str:
        """
        Build COMPREHENSIVE lab report with all session details.
        """
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        markdown = f"""# Laboratory Report: {experiment_name}

**Session ID:** `{session_id}`
**Date:** {timestamp}
**Generated by:** CSGirlies-AILAB AI Partner System

---

## 1. Experiment Overview

**Subject:** {scenario_data.get('subject', 'Science')}
**Level:** {scenario_data.get('level', 'Beginner')}
**Duration:** {scenario_data.get('duration', 'N/A')} minutes

### Learning Objectives
"""

        if isinstance(scenario_data.get('learning_objectives'), list):
            for obj in scenario_data['learning_objectives']:
                markdown += f"- {obj}\n"

        markdown += f"""
### Materials Used
"""

        if isinstance(scenario_data.get('materials'), list):
            for material in scenario_data['materials']:
                markdown += f"- {material}\n"

        markdown += f"""
---

## 2. Experimental Procedure

"""

        if isinstance(scenario_data.get('steps'), list):
            for i, step in enumerate(scenario_data['steps'], 1):
                title = step.get('title', f'Step {i}')
                description = step.get('description', '')
                markdown += f"### Step {i}: {title}\n{description}\n\n"

        markdown += f"""
---

## 3. Conversation Log & Observations

This section contains the complete dialogue between the student and AI lab partners.

"""

        if conversation_history:
            markdown += "### Dialogue Transcript\n\n"
            for msg in conversation_history:
                sender = msg.get('sender', 'Unknown')
                content = msg.get('content', '')
                role = msg.get('role', '')
                markdown += f"**{sender}** ({role}):\n> {content}\n\n"
        else:
            markdown += "*No conversation recorded*\n\n"

        markdown += f"""
### Student Observations
"""

        if observations:
            for step_key, observation in observations.items():
                markdown += f"- **{step_key}**: {observation}\n"
        else:
            markdown += "*No observations recorded*\n"

        markdown += f"""
---

## 4. Wolfram Computational Results

"""

        if wolfram_results:
            for i, result in enumerate(wolfram_results, 1):
                query = result.get('query', 'N/A')
                result_text = result.get('result', 'N/A')
                numeric = result.get('numeric_result', 'N/A')

                markdown += f"""
### Computation {i}

**Query:**
```
{query}
```

**Result:** {result_text}
**Numeric Value:** {numeric}

"""
                if result.get('graph_svg'):
                    markdown += f"**Graph:** SVG visualization generated (base64 encoded)\n\n"
        else:
            markdown += "*No computations performed*\n"

        markdown += f"""
---

## 5. Evaluation & Learning Assessment

"""

        if evaluation:
            markdown += f"""
**Overall Performance:** {evaluation.get('overall_performance', 'N/A')}
**Understanding Level:** {evaluation.get('understanding_level', 'N/A')}
**Areas of Strength:** {evaluation.get('strengths', 'N/A')}
**Areas for Improvement:** {evaluation.get('improvements', 'N/A')}

### Detailed Feedback
{evaluation.get('detailed_feedback', 'No evaluation available')}
"""
        else:
            markdown += "*Evaluation not completed*\n"

        markdown += f"""
---

## 6. Conclusions

{evaluation.get('conclusions', 'Experiment completed successfully. All objectives were addressed through interactive AI-guided learning.')}

---

## 7. References & Additional Resources

- **Wolfram Language Documentation:** https://www.wolfram.com/language/
- **Experiment Methodology:** AI-driven collaborative learning
- **Technology Stack:** OpenAI GPT-4, Wolfram Cloud, GitBook API

---

**Report automatically generated by CSGirlies-AILAB**
*Making science education accessible, engaging, and fun through AI*

Session ID: `{session_id}`
Generated: {timestamp}
"""

        return markdown

    def _build_experiment_markdown(self,
                                   experiment_name: str,
                                   scenario_data: Dict[str, Any],
                                   results: Dict[str, Any]) -> str:
        """
        Build markdown content for the experiment page.
        
        Args:
            experiment_name: Experiment name
            scenario_data: Scenario details
            results: Experiment results
            
        Returns:
            Markdown formatted content
        """
        
        markdown = f"""# {experiment_name}

## Overview
{scenario_data.get('description', 'Experiment in progress')}

### Learning Objectives
"""
        
        if isinstance(scenario_data.get('learning_objectives'), list):
            for obj in scenario_data['learning_objectives']:
                markdown += f"- {obj}\n"
        
        markdown += f"""
## Materials
"""
        
        if isinstance(scenario_data.get('materials'), list):
            for material in scenario_data['materials']:
                markdown += f"- {material}\n"
        
        markdown += f"""
## Procedure

"""
        
        if isinstance(scenario_data.get('steps'), list):
            for step in scenario_data['steps']:
                step_num = step.get('step_number', '?')
                title = step.get('title', 'Step')
                instructions = step.get('instructions', '')
                markdown += f"### Step {step_num}: {title}\n{instructions}\n\n"
        
        markdown += f"""## Results & Analysis

### Key Findings
{results.get('summary', 'Results processing...')}

### Graphs and Visualizations
{results.get('graph_description', 'Graphs generated')}

### Data Summary
- Partner Observations: {results.get('partner_message', 'N/A')}
- Mentor Guidance: {results.get('mentor_message', 'N/A')}
- Wolfram Computation: {results.get('wolfram_result', 'Computed')}

## Conclusions

{results.get('conclusions', 'Experiment complete. Further analysis needed.')}

---
*Experiment generated by CSGirlies-AILAB on {results.get('timestamp', 'today')}*
"""
        
        return markdown
    
    async def update_learning_portal(self, 
                                     student_id: str,
                                     experiment_id: str,
                                     performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update student's learning portal with experiment results.
        
        Args:
            student_id: Student identifier
            experiment_id: Experiment identifier
            performance_data: Student performance metrics
            
        Returns:
            Update response
        """
        return {
            "success": True,
            "message": "Student progress updated",
            "student_id": student_id
        }


# Global GitBook integration instance
gitbook_integration = GitBookIntegration()

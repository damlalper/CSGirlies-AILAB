"""Example usage and demo of CSGirlies-AILAB system"""

import asyncio
import json
from app import app
from fastapi.testclient import TestClient

client = TestClient(app)


def demo_list_experiments():
    """Demo: List all available experiments"""
    print("\n" + "="*60)
    print("DEMO 1: List Available Experiments")
    print("="*60)
    
    response = client.get("/experiments")
    experiments = response.json()
    
    print(f"\nFound {len(experiments['experiments'])} experiments:")
    for exp in experiments['experiments']:
        print(f"\n  📚 {exp['title']}")
        print(f"     ID: {exp['id']}")
        print(f"     Subject: {exp['subject']}")
        print(f"     Level: {exp['level']}")
        print(f"     Duration: {exp['duration_minutes']} minutes")


def demo_get_experiment_details():
    """Demo: Get details of a specific experiment"""
    print("\n" + "="*60)
    print("DEMO 2: Get Experiment Details (Acid-Base Titration)")
    print("="*60)
    
    response = client.get("/experiments/chem_titration")
    experiment = response.json()
    
    print(f"\n📖 {experiment['title']}")
    print(f"\nDescription: {experiment['description']}")
    print(f"\nLearning Objectives:")
    for obj in experiment['learning_objectives'][:3]:
        print(f"  ✓ {obj}")
    
    print(f"\nMaterials Needed:")
    for material in experiment['materials'][:5]:
        print(f"  • {material}")
    
    print(f"\nExperiment Steps: {len(experiment['steps'])} total steps")
    for step in experiment['steps'][:2]:
        print(f"\n  Step {step['step_number']}: {step['title']}")


def demo_start_experiment():
    """Demo: Start an experiment session"""
    print("\n" + "="*60)
    print("DEMO 3: Start Experiment Session")
    print("="*60)
    
    request_data = {
        "experiment_id": "chem_titration",
        "level": "beginner",
        "student_name": "Alex"
    }
    
    response = client.post("/simulate/start", json=request_data)
    result = response.json()
    
    print(f"\n✨ Experiment Started!")
    print(f"   Session ID: {result['session_id']}")
    print(f"   Experiment: {result['experiment_title']}")
    print(f"   Student: {result['student_name']}")
    
    print(f"\n🤖 Partner (Alex) says:")
    print(f"   \"{result['partner_message']}\"")
    
    print(f"\n📝 First Step: {result['first_step']['title']}")
    
    return result['session_id']


def demo_student_interaction(session_id: str):
    """Demo: Student interacts with the experiment"""
    print("\n" + "="*60)
    print("DEMO 4: Student Interaction During Experiment")
    print("="*60)
    
    student_inputs = [
        "I'm ready to start. What should I do first?",
        "I pipetted 20 mL of the acid into the flask and added the indicator.",
        "The solution turned pink after adding 23.5 mL of NaOH.",
        "Is the experiment complete? Should I calculate the molarity?"
    ]
    
    for i, user_input in enumerate(student_inputs, 1):
        print(f"\n--- Step {i} ---")
        print(f"Student: \"{user_input}\"")
        
        request_data = {
            "session_id": session_id,
            "experiment_id": "chem_titration",
            "student_message": user_input,
            "current_step": i
        }
        
        response = client.post("/simulate/interact", json=request_data)
        result = response.json()
        
        print(f"\n🤖 Partner: {result['partner_message']}")
        
        if result['mentor_guidance']:
            print(f"\n👨‍🏫 Mentor: {result['mentor_guidance']}")
        
        print(f"   Progress: {result['progress']:.0f}%")
        
        # Show Wolfram result on final step
        if result['wolfram_result']:
            print(f"\n📊 Wolfram Computation:")
            print(f"   Result: {result['wolfram_result'].get('result', 'Computed')}")
        
        if i < len(student_inputs):
            print("-" * 40)


def demo_complete_experiment(session_id: str):
    """Demo: Complete the experiment and generate documentation"""
    print("\n" + "="*60)
    print("DEMO 5: Complete Experiment & Generate Documentation")
    print("="*60)
    
    response = client.post(
        "/simulate/complete",
        params={
            "session_id": session_id,
            "experiment_id": "chem_titration"
        }
    )
    
    result = response.json()
    
    print(f"\n✅ {result['status'].upper()}")
    print(f"\nEvaluator Feedback:")
    print(f"{result['evaluator_feedback']}")
    
    print(f"\nGitBook Documentation: {'✓ Generated' if result['gitbook_status'] else '✗ Skipped'}")
    print(f"\nMessage: {result['message']}")


def run_full_demo():
    """Run complete demonstration"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🧪 CSGirlies-AILAB - Interactive Lab Partner Demo  ".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        # Run demos in sequence
        demo_list_experiments()
        demo_get_experiment_details()
        session_id = demo_start_experiment()
        demo_student_interaction(session_id)
        demo_complete_experiment(session_id)
        
        print("\n" + "="*60)
        print("🎉 Demo Complete!")
        print("="*60)
        print("\nThe system successfully demonstrated:")
        print("  ✓ Multi-agent lab partner system")
        print("  ✓ Dynamic scenario loading")
        print("  ✓ Natural AI conversations")
        print("  ✓ Mentor guidance and feedback")
        print("  ✓ Wolfram computation integration")
        print("  ✓ Automatic documentation generation")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\nStarting CSGirlies-AILAB Demo...")
    print("Make sure the FastAPI server is running on http://127.0.0.1:8000")
    print("\nTo start the server, run: uvicorn app:app --reload\n")
    
    try:
        run_full_demo()
    except Exception as e:
        print(f"Demo failed: {e}")
        print("\nMake sure the server is running!")

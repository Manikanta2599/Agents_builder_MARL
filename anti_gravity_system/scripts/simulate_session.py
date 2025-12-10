import sys
import os
import time
import requests
import json
import random

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

API_URL = "http://localhost:8000"

def simulate_session():
    print("🚀 Starting Anti-Gravity Simulation: 'Analyze AI Stock Trends'")
    
    # 1. Start a Session
    session_id = f"sim_{int(time.time())}"
    query = "Analyze current trends in AI stock performance and write a python script to visualize them."
    
    print(f"📡 Sending Query: '{query}' (Session: {session_id})")
    
    try:
        # Initial Request (This would trigger the Orchestrator)
        # In a real run, this would block. For simulation, if we want to populate the frontend 
        # with "fake" events while the backend processes, OR if we are just testing the frontend's
        # ability to render standard API responses, we can hit the actual API.
        # However, since we might be in Mock Mode, let's hit the actual API to demonstrate the system.
        
        response = requests.post(f"{API_URL}/chat/turn", json={"message": query, "session_id": session_id})
        res_data = response.json()
        
        print("\n✅ System Response Received:")
        print(f"Response: {res_data.get('response')}")
        
        steps = res_data.get('steps', [])
        print(f"\n📊 Steps Generated ({len(steps)}):")
        for s in steps:
            step_info = s.get('step', {})
            print(f"  - [{step_info.get('worker', 'Orchestrator')}] {step_info.get('task')} -> {s.get('review', {}).get('approved')}")
            
        print("\n✨ Simulation Complete. Check the UI!")
        
    except Exception as e:
        print(f"❌ Simulation Failed: {e}")
        print("Ensure the backend is running: ./bin/uvicorn app.main:app --reload --port 8000")

if __name__ == "__main__":
    simulate_session()

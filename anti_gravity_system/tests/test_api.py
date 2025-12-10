from fastapi.testclient import TestClient
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from anti_gravity_system.app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "system": "Anti-Gravity"}

def test_chat_turn():
    # This will use the Mock LLM
    response = client.post("/chat/turn", json={"message": "Research Python news"})
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert len(data["steps"]) > 0
    print("Chat API verification successful:", data["response"][:50] + "...")

def test_agent_run():
    # Test direct worker access
    response = client.post("/agent/worker_research/run", json={"task": "Find X"})
    assert response.status_code == 200
    assert "output" in response.json()
    print("Agent Run verification successful")

if __name__ == "__main__":
    test_health()
    test_chat_turn()
    test_agent_run()
    print("All API tests passed!")

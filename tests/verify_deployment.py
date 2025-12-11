from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import os

# Set dummy key for auth bypass in tests if needed, or we test with keys
os.environ["REQUIRE_AUTH"] = "true"

from anti_gravity_system.app.main import app, get_orchestrator
from anti_gravity_system.src.core.security import API_KEYS

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "agent_requests_total" in response.text

def test_rbac_admin_route():
    # 1. No Key -> 401
    response = client.post("/agent/worker_research/run", json={"task": "test"})
    assert response.status_code == 401
    
    # 2. User Key -> 403 (Forbidden for this route)
    headers = {"x-api-key": "sk-user"}
    response = client.post("/agent/worker_research/run", json={"task": "test"}, headers=headers)
    assert response.status_code == 403
    
    # 3. Admin Key -> 200 (Success, assuming agent exists)
    # Mock orchestrator behavior
    app.dependency_overrides[get_orchestrator] = lambda: MagicMock()
    
    headers = {"x-api-key": "sk-admin"}
    # We expect 404 or 500 depending on mock, but definitely NOT 401/403
    # Actually, let's just check it passes auth
    try:
        response = client.post("/agent/worker_research/run", json={"task": "test"}, headers=headers)
        assert response.status_code != 401
        assert response.status_code != 403
    finally:
        app.dependency_overrides = {}

if __name__ == "__main__":
    print("Verifying Health...")
    test_health()
    print("Verifying Metrics...")
    test_metrics()
    print("Verifying RBAC...")
    test_rbac_admin_route()
    print("All Deployment Tests Passed!")

import sys
import os
import yaml

sys.path.append(os.getcwd())

from anti_gravity_system.src.agents.orchestrator import OrchestratorAgent

def load_config():
    config_path = os.path.join(os.getcwd(), 'anti_gravity_system', 'config', 'agents.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def test_system():
    print("\n--- Initializing System ---")
    config = load_config()
    agents_conf = config.get('agents', [])
    orch_conf = next((a for a in agents_conf if a['id'] == 'orchestrator'), {})
    
    orchestrator = OrchestratorAgent(orch_conf, agents_conf)
    
    print("\n--- Running Orchestrator ---")
    user_request = "Find python trends and write a script to print them."
    final_result = orchestrator.run(user_request)
    
    print("\n--- Final System Output ---")
    print(f"Session: {final_result['session_id']}")
    print(final_result['final_response'])
    
    print("\n--- Detailed Steps ---")
    for step in final_result['steps']:
        print(f"Worker: {step['step'].get('worker', step['step'].get('worker_id'))}")
        print(f"Result: {step['result']['status']}")
        print(f"Critic: {step['review']['approved']}")

if __name__ == "__main__":
    test_system()

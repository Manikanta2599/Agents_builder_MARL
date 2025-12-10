import json
import os
from typing import Dict

def load_system_prompts() -> Dict[str, str]:
    # Assuming config is in ../../../config relative to this file? 
    # Or rely on project root being in sys.path and config being in anti_gravity_system/config
    # Better to find it relative to the file.
    
    # Try multiple paths to be robust
    possible_paths = [
        os.path.join(os.getcwd(), 'anti_gravity_system', 'config', 'system_prompts.json'),
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'system_prompts.json')
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
                
    return {}

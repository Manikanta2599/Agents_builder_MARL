from typing import Dict, Any, List
from anti_gravity_system.src.utils.logger import logger

class UIAgent:
    def __init__(self, config: Dict[str, Any], orchestrator):
        self.config = config
        self.orchestrator = orchestrator
        self.name = config.get('name', 'UI Agent')
        logger.info(f"UI Agent initialized: {self.name}")

    def process_user_input(self, user_input: str) -> str:
        """
        Takes raw user input, sends to Orchestrator, and formats response.
        """
        logger.info(f"[{self.name}] User Input: {user_input}")
        
        # In a real system, checks for clarification needs or simple chit-chat here.
        # For now, pass through to Orchestrator.
        
        result = self.orchestrator.run(user_input)
        
        return self._format_response(result)

    def _format_response(self, result: Dict[str, Any]) -> str:
        steps = result.get('steps', [])
        final_text = "\n[bold green]Processing Complete![/bold green]\n"
        final_text += f"Session ID: {result.get('session_id')}\n\n"
        
        final_text += "[bold]Execution Summary:[/bold]\n"
        for step in steps:
            task = step['step']['task']
            status = step['result'].get('status')
            feedback = step['review'].get('feedback')
            
            icon = "✅" if status == "success" else "❌"
            final_text += f"{icon} Task: {task}\n"
            if feedback and "APPROVED" not in feedback:
                final_text += f"   ⚠️ Critic: {feedback}\n"
        
        return final_text

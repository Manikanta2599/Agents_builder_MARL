import yaml
import os
import sys
from rich.console import Console
from rich.panel import Panel

# Add project root to path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

console = Console()

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'agents.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def main():
    console.print(Panel.fit("[bold blue]Anti-Gravity Multi-Agent System[/bold blue]", subtitle="Initializing..."))
    
    try:
        config = load_config()
        agents_conf = config.get('agents', [])
        
        orch_conf = next((a for a in agents_conf if a['id'] == 'orchestrator'), {})
        ui_conf = next((a for a in agents_conf if a['id'] == 'ui_agent'), {})
        
        from anti_gravity_system.src.agents.orchestrator import OrchestratorAgent
        from anti_gravity_system.src.agents.ui_agent import UIAgent
        
        orchestrator = OrchestratorAgent(orch_conf, agents_conf)
        ui_agent = UIAgent(ui_conf, orchestrator)
        
        console.print(f"[green]System Ready![/green] (Type 'exit' to quit)")
        
        while True:
            user_input = console.input("\n[bold cyan]User > [/bold cyan]")
            if user_input.lower() in ['exit', 'quit']:
                console.print("[yellow]Shutting down...[/yellow]")
                break
                
            if not user_input.strip():
                continue
                
            with console.status("[bold green]Processing...[/bold green]", spinner="dots"):
                response = ui_agent.process_user_input(user_input)
            
            console.print(Panel(response, title="System Response", border_style="green"))

    except Exception as e:
        console.print(f"[bold red]System Error:[/bold red] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

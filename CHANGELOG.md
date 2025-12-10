# Changelog 📜

## [v1.1.0] - 2025-12-10
### Added
- **Planner Agent**: A specialized worker (`src/agents/planner.py`) capable of decomposing high-level goals into Directed Acyclic Graphs (DAGs) of subtasks.
- **Voice Interface**: Added microphone support to the "Magic Window" UI (`ChatInterface.tsx`) using the Web Speech API. Users can now speak to the Orchestrator.
- **Worker Refactoring**: Unified `WorkerFactory` to support specialized agent instantiation.

## [v1.0.0] - 2025-12-10
### Initial Release
- **Core System**: Orchestrator, Memory, Critic, Research, Code, and Data Agents.
- **Frontend**: Next.js Dashboard with Real-time Chat and Agent Visualizer.
- **Backend**: FastAPI system with SQLite/ChromaDB memory.
- **Deployment**: Docker and Docker Compose configuration.

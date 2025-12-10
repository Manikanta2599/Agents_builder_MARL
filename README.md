# Anti-Gravity System 🌌🧠

> Autonomous Multi-Agent Orchestration Engine with "Magic Window" UI.

**Anti-Gravity** is a sophisticated AI system that decomposes complex user goals into atomic tasks, delegates them to specialized agents (Research, Code, Data), and attempts to self-correct using a Critic agent.

## 🚀 Quick Start (Docker)

The easiest way to run the full system.

1.  **Set API Key**:
    ```bash
    export OPENAI_API_KEY=sk-...
    ```
2.  **Run Containers**:
    ```bash
    docker-compose up --build
    ```
3.  **Access UI**: Open [http://localhost:3000](http://localhost:3000)

## 🛠️ Manual Installation

### Backend (FastAPI)
```bash
cd anti_gravity_system
pip install -r requirements.txt
./bin/uvicorn app.main:app --reload --port 8000
```

### Frontend (Next.js)
```bash
cd anti_gravity_frontend
npm install
npm run dev
```
Access UI at [http://localhost:3000](http://localhost:3000).

## 🧪 Testing & Simulation

**Run Q/A Suite:**
```bash
python anti_gravity_system/tests/run_all.py
```

**Run End-to-End Simulation:**
(Requires Backend running)
```bash
python anti_gravity_system/scripts/simulate_session.py
```

## 🏗️ Architecture
- **Orchestrator**: Controls the OODA loop (Observe-Think-Plan-Act).
- **Workers**: Specialized agents (Researcher, Coder, Data Scientist).
- **Critic**: Safety & quality filter.
- **Memory**: Vector-based context storage (ChromaDB).
- **Frontend**: Next.js + Tailwind "Glassmorphism" UI.

---
*Built with ❤️ by the Anti-Gravity Team.*

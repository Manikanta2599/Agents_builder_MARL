# 🌌 Anti-Gravity System: Enterprise Multi-Agent Architecture

> **Orchestrating Autonomous Intelligence with MARL-Driven Optimizations.**

[![CI Status](https://github.com/Manikanta2599/Agents_builder_MARL/actions/workflows/ci.yml/badge.svg)](https://github.com/Manikanta2599/Agents_builder_MARL/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

---

## 📖 Executive Summary

**Anti-Gravity** is a production-ready, cloud-native framework for building, deploying, and orchestrating autonomous AI agents. Unlike simple agent scripts, Anti-Gravity enforces a **Domain-Driven Design (DDD)** enterprise architecture, leveraging **Multi-Agent Reinforcement Learning (MARL)** to continuously optimize agent performance through critic-driven reward signals.

The system is designed for scalability, featuring a microservices architecture with **Redis** for message brokering, **ChromaDB** for vector memory, and **Prometheus** for real-time observability.

---

## 🏗 System Architecture

The system follows a strict **Orchestrator-Worker-Critic** pattern, governed by a Finite State Machine (FSM) to ensure deterministic lifecycles.

```mermaid
graph TD
    User[User Request] -->|REST API| API[FastAPI Gateway]
    API -->|Session| Orch[Orchestrator Agent]
    
    subgraph "Cognitive Core"
        Orch -->|Observe| Memory[Memory Agent / ChromaDB]
        Orch -->|Think/Plan| LLM[LLM Provider]
        Orch -->|Delegate| Workers[Worker Swarm]
    end
    
    subgraph "Worker Swarm"
        Workers -->|Research| W_Res[Research Agent]
        Workers -->|Code| W_Code[Coding Agent]
    end
    
    subgraph "MARL Optimization Loop"
        W_Res & W_Code -->|Output| Critic[Critic & Safety Agent]
        Critic -->|Reward Signal (+/-)| Orch
        Orch -->|Policy Update| Policy[Orchestrator Policy]
    end
```

### Key Components

1.  **Orchestrator Engine (`/orchestrator`)**:
    *   **State Machine**: Enforces `IDLE` → `OBSERVING` → `PLANNING` → `DELEGATING` → `CRITIQUING` lifecycle.
    *   **Planner**: Decomposes high-level goals into atomic DAG (Directed Acyclic Graph) tasks using externalized YAML prompts.

2.  **Specialized Agents (`/agents`)**:
    *   **Research Worker**: Autonomous web searching and summarization using `WebSearchTool`.
    *   **Coding Worker**: Generates, executes, and validates Python code using `FileIOTool`.
    *   **Critic/Safety**: A dual-purpose agent that validates safety (hallucinations, PII) and calculates **MARL Reward Signals** for reinforcement learning.

3.  **Memory Layer (`/memory`)**:
    *   **Hybrid Storage**: Combines Relational (SQLite) for session metadata and Vector (ChromaDB) for semantic context.
    *   **Memory Agent**: Abstract interface for `store`, `search`, and `get_history` operations.

---

## 🧠 MARL Integration (Multi-Agent Reinforcement Learning)

Anti-Gravity implements a specialized feedback loop to improve orchestration efficiency over time:

*   **Observation**: The Orchestrator observes the output of a Worker.
*   **Critique**: The `CriticSafetyAgent` verifies the output against the original task.
*   **Reward Signal**:
    *   **+1.0**: Task completed successfully and approved.
    *   **-0.5**: Task rejected due to safety or correctness violations.
    *   **-1.0**: Critical failure or hallucination.
*   **Policy Update**: The Orchestrator adjusts its worker selection weights based on the accumulated reward signal (Q-Learning stub implemented).

---

## 🚀 Features

*   ✅ **Enterprise Pylint Compliant**: Modular Python package structure.
*   ✅ **Security First**: RBAC (Role-Based Access Control) and Safety Layers for input/output validation.
*   ✅ **Observability**: Prometheus metrics (`/metrics`) for latency, token usage, and error rates.
*   ✅ **Infrastructure as Code**: Kubernetes manifests (`k8s/`) and Docker Compose stacks.
*   ✅ **Modern UI**: Next.js Dashboard with real-time system metrics.

---

## 📂 Folder Structure

```p
anti_gravity_system/
├── orchestrator/          # Core Logic Control
│   ├── orchestrator.py    # Main Agent Class
│   └── state_machine.py   # Finite State Machine
├── agents/                # Domain-Specific Agents
│   ├── worker_research.py
│   ├── worker_code.py
│   └── critic_safety.py
├── tools/                 # Tool Abstractions
│   ├── vector_db.py       # ChromaDB Wrapper
│   └── web_search.py
├── memory/                # Persistence Layer
│   └── memory_store.py
├── prompts/               # Externalized YAML Prompts
├── app/                   # FastAPI Gateway
└── src/core/              # Shared Utilities (Metrics, Security)
```

---

## ⚡ Getting Started

### Prerequisites
*   Docker & Docker Compose
*   Python 3.10+
*   Node.js (for Frontend)

### 1. Installation

Clone the repository:
```bash
git clone https://github.com/Manikanta2599/Agents_builder_MARL.git
cd Agents_builder_MARL
```

Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r anti_gravity_system/requirements.txt
```

### 2. Configuration

Set your environment variables:
```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 3. Running Locally (Docker Stack)

Launch the full stack (API, Frontend, Redis, Chroma, Prometheus):
```bash
docker-compose up --build
```

Access the services:
*   **Frontend UI**: [http://localhost:3000](http://localhost:3000)
*   **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
*   **Prometheus**: [http://localhost:9090](http://localhost:9090)

---

## 🧪 CI/CD & Testing

The project includes a comprehensive CI pipeline using GitHub Actions.

**Run Unit Tests:**
```bash
python -m pytest anti_gravity_system/tests/verify_enterprise_arch.py
```

**Run Deployment Verification:**
```bash
python tests/verify_deployment.py
```

---

## 🔮 Roadmap

*   [ ] **Phase 2**: Full PPO (Proximal Policy Optimization) implementation for Orchestrator training.
*   [ ] **Phase 3**: Distributed worker nodes using Celery/RabbitMQ.
*   [ ] **Phase 4**: Multi-Tenant SaaS support with Clerk/Auth0 integration.

---

## 🤝 Contribution

We welcome contributions! Please see `CONTRIBUTING.md` for details.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

© 2025 Anti-Gravity Systems. Built by Manikanta.

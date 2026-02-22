
# 🧠 Hybrid LLM Agent-to-Agent (A2A) Node  
### Cloud Intelligence × Local Execution × On-Chain Settlement
### Local Python Agent connected to Virtuals GAME SDK + Base Sepolia

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Web3](https://img.shields.io/badge/Web3-Base%20Sepolia-purple)
![LLM](https://img.shields.io/badge/LLM-Virtuals%20GAME-orange)
![Architecture](https://img.shields.io/badge/Architecture-Hybrid%20Cloud%20%2B%20Local-black)

This repository demonstrates a **hybrid autonomous agent architecture** in which:

- A **local Python agent** provides real execution capabilities
- A **cloud-based LLM (Virtuals GAME)** performs reasoning and routing
- The agent can trigger blockchain actions on **Base Sepolia**

It showcases a hybrid architecture:

- 🧠 Reasoning is performed by a cloud-hosted LLM (Virtuals GAME)
- 💻 Execution capabilities remain local in Python
- ⛓️ Final state transitions settle on Base Sepolia

The project illustrates how to safely combine:

- Tool-based LLM orchestration
- Local private key isolation
- Structured agent memory handling
- On-chain transaction execution

This is a minimal but extensible blueprint for building autonomous Web3 agents.
---

# 🏗 Architecture Overview

## System-Level Overview

```mermaid
flowchart TB
    subgraph Local["💻 Your Local Machine (The Muscle / Bridge)"]
        direction TB
        AgentScript["agent.py<br>(Game Loop)"]
        Worker["Python Worker<br>(action_space)"]
        LocalTools["Local Functions<br>- analyze_crypto_data()<br>- execute_transaction()"]
        Env[".env<br>(Private Key stored securely)"]
        
        AgentScript <--> Worker
        Worker <--> LocalTools
        Env -.->|Signs Payloads| LocalTools
    end

    subgraph Cloud["🧠 Virtuals G.A.M.E. (The Brain)"]
        direction TB
        GameAPI["GAME API Endpoint"]
        LLM["LLM Routing Engine"]
        Memory["Agent State & Memory<br>(HLP, LLP, Logs)"]
        
        GameAPI <--> LLM
        LLM <--> Memory
    end

    subgraph Web3["⛓️ Base Sepolia (The Bank / State Machine)"]
        direction TB
        RPC["RPC Node<br>(https://sepolia.base.org)"]
        EVM["Ethereum Virtual Machine"]
        Ledger["State Ledger<br>(Balances, Smart Contracts)"]
        
        RPC <--> EVM
        EVM <--> Ledger
    end

    AgentScript <=="HTTP / JSON-RPC<br>(Prompts & Tool Calls)"==> GameAPI
    LocalTools =="Signed JSON-RPC<br>(Transactions)"==> RPC
    
    classDef local fill:#eef7ee,stroke:#4CAF50,stroke-width:2px,color:#000;
    classDef cloud fill:#eef5fb,stroke:#2196F3,stroke-width:2px,color:#000;
    classDef web3 fill:#f5eefb,stroke:#9C27B0,stroke-width:2px,color:#000;
    
    class Local local;
    class Cloud cloud;
    class Web3 web3;
```

---

# 🔄 Agentic Execution Flow

```mermaid
sequenceDiagram
    autonumber
    participant Terminal as Your Terminal
    participant Python as Local Python Script
    participant Cloud as Virtuals Cloud (LLM)
    participant Base as Base Blockchain (RPC)

    Terminal->>Python: python agent.py
    Python->>Cloud: agent.compile()<br>(Register tools & sandbox)
    
    rect rgb(240, 245, 255)
        Note over Terminal,Cloud: --- TICK 1: Analysis Phase ---
        Python->>Cloud: agent.step()
        Cloud-->>Cloud: Read Goal<br>"Analyze data..."
        Cloud->>Python: Trigger analyze_crypto_data
        Python-->>Cloud: DONE<br>"Tx recommended"
        Cloud-->>Cloud: Update Memory
        Python->>Terminal: Display Goal & Reasoning
    end

    rect rgb(240, 255, 245)
        Note over Terminal,Base: --- TICK 2: Blockchain Action ---
        Python->>Cloud: agent.step()
        Cloud-->>Cloud: Read Memory<br>"Tx recommended"
        Cloud->>Python: Trigger execute_transaction
        Python->>Base: eth_sendRawTransaction
        Base-->>Python: Tx Hash
        Python-->>Cloud: DONE<br>"Transaction sent"
        Cloud-->>Cloud: Update Memory
        Python->>Terminal: Display Success
    end
```
---

# 🧪 Architectural Properties

### Deterministic Execution Boundary
LLM reasoning is non-deterministic.  
Local tool execution remains deterministic and auditable.

### Secure Key Isolation
Private keys never leave the local machine.  
The cloud LLM only decides *what* to do — not *how to sign*.

### Agent Memory as State Machine
The agent’s HLP/LLP memory logs function as a soft state machine, enabling:

- Multi-step reasoning
- Emergent goal transitions
- Conditional tool routing

### Extensibility
Additional workers can be attached to expand capability:

- Market execution
- DAO governance interaction
- Cross-agent payment settlement
- Oracle data ingestion

---

# 🧩 What This Project Demonstrates

### ✅ Cloud-Local Hybrid Agent Architecture  
LLM reasoning lives in the cloud.  
Execution power lives locally.

### ✅ Tool Registration via GAME SDK  
Local Python functions are exposed as structured callable tools.

### ✅ State & Memory Handling  
Agent state is extracted robustly from `agent.step()` responses.

### ✅ Secure Private Key Handling  
Private keys remain local inside `.env` and never leave your machine.

### ✅ A2A Decision Loop  
Agent analyzes → recommends → executes → updates memory.

---

# 📂 Project Structure

```
.
├── agent.py
├── .env
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

## 2️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate     # Windows
```

## 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file:

```
GAME_API_KEY=your_virtuals_api_key
PRIVATE_KEY=your_wallet_private_key
```

Add this to `.gitignore`:

```
.env
```

---

# ▶️ Run the Agent

```bash
python agent.py
```

You will see:

- Agent goal
- LLM reasoning
- Tool execution
- Memory updates
- Function results

---

# 🚀 Why This Matters

This architecture enables:

- Autonomous agents with real-world execution
- Secure key isolation
- Composable AI + Web3 workflows
- Agent-to-Agent economies

It’s a minimal but powerful demonstration of **LLM-driven blockchain agents**.

---

# 📜 License

MIT License

---

# 👤 Author

Built as an experimental A2A prototype combining:

- Python execution
- Virtuals GAME SDK
- Base Sepolia network
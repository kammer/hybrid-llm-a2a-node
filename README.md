# 🧠 Hybrid LLM Agent-to-Agent (A2A) Node
### Cloud Intelligence × Local Execution × On-Chain Settlement

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Web3](https://img.shields.io/badge/Web3-Base%20Sepolia-purple)
![LLM](https://img.shields.io/badge/LLM-Virtuals%20GAME-orange)
![Architecture](https://img.shields.io/badge/Architecture-Hybrid%20Cloud%20%2B%20Local-black)

A minimal but extensible blueprint for building **autonomous Web3 agents**, combining cloud LLM reasoning with local Python execution and on-chain settlement on Base Sepolia.

- 🧠 **Reasoning** — Cloud-hosted LLM via [Virtuals G.A.M.E.](https://console.game.virtuals.io/)
- 💻 **Execution** — Local Python with private key isolation
- ⛓️ **Settlement** — Final state transitions on Base Sepolia

---

## 🏗 Architecture

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

## 🔄 Agentic Execution Flow

```mermaid
sequenceDiagram
    autonumber
    participant Terminal as Your Terminal
    participant Python as Local Python Script
    participant Cloud as Virtuals G.A.M.E. (LLM)
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

## 🧪 Architectural Properties

**Deterministic Execution Boundary** — LLM reasoning is non-deterministic; local tool execution remains deterministic and auditable.

**Secure Key Isolation** — Private keys never leave the local machine. The cloud LLM only decides *what* to do — not *how to sign*.

**Agent Memory as State Machine** — The agent's HLP/LLP memory logs function as a soft state machine, enabling multi-step reasoning, emergent goal transitions, and conditional tool routing.

**Extensibility** — Additional workers can be attached to expand capability: market execution, DAO governance interaction, cross-agent payment settlement, oracle data ingestion.

---

## 📂 Project Structure

```
.
├── agents/
│   └── agent.py              # Main A2A game loop
│
├── tools/
│   ├── analyze.py            # analyze_crypto_data() and similar
│   └── transactions.py       # execute_transaction() logic
│
├── workers/
│   └── action_space.py       # Tool registration / worker wiring for GAME SDK
│
├── scripts/
│   ├── app.py                # Early prototype / REST entry point
│   └── send_tx.py            # Standalone transaction utility
│
├── .env
├── requirements.txt
└── README.md
```

The structure separates **what the agent does** (`tools/`) from **how it's orchestrated** (`agents/`) and **how tools are exposed** to the G.A.M.E. SDK (`workers/`). The `scripts/` folder preserves the original prototype files for reference.

As the project grows, new capabilities slot in cleanly — e.g. `agents/market_agent.py`, `tools/oracle.py`, or `workers/dao_worker.py`.

---

## ⚙️ Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

**2. Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate     # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```
GAME_API_KEY=your_virtuals_game_api_key   # Get yours at https://console.game.virtuals.io/
PRIVATE_KEY=your_wallet_private_key
```

Add `.env` to your `.gitignore` to ensure your private key is never committed.

---

## ▶️ Running the Agent

```bash
python agent.py
```

The terminal will display the agent's goal, LLM reasoning, tool execution steps, memory updates, and function results in real time.

---

## 📜 License

MIT License

---

## 👤 Author

**Raimund Kammering**

Experimental A2A prototype combining Python execution, [Virtuals G.A.M.E. SDK](https://console.game.virtuals.io/), and Base Sepolia.

Public wallet: `0x072C12957983104891DCEB9C1C90dD94eda7Ca8C`

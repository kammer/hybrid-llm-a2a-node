import sys
import os
from dotenv import load_dotenv
from game_sdk.game.custom_types import FunctionResultStatus
from game_sdk.game.agent import Agent, WorkerConfig
from game_sdk.game.custom_types import Function, Argument

load_dotenv()

# ---------------------------------------------------------
# 1. Define your local capability
# ---------------------------------------------------------
import sys

def analyze_crypto_data(data_string: str):
    if isinstance(data_string, dict):
        data_string = data_string.get("value", str(data_string))
        
    # We write directly to __stdout__ to bypass our log silencer!
    sys.__stdout__.write(f"\n⚡ [LOCAL EXECUTION WAKING UP] -> Analyzing data: {data_string}\n")
    
    return (
        FunctionResultStatus.DONE, 
        "Analysis complete: Agent-to-Agent transaction recommended.", 
        {}
    )

# ---------------------------------------------------------
# 2. Map the capability to the GAME SDK
# ---------------------------------------------------------
analyze_func = Function(
    fn_name="analyze_crypto_data",
    fn_description="Analyzes market data and returns a recommendation.",
    args=[
        Argument(name="data_string", type="string", description="The raw data to analyze")
    ],
    executable=analyze_crypto_data
)

# ---------------------------------------------------------
# 3. Define State Management (New Requirement)
# ---------------------------------------------------------
def get_state(function_result, current_state):
    """Tells the agent how to update its memory after a function runs."""
    return {}

# ---------------------------------------------------------
# 4. Create the Worker Configuration
# ---------------------------------------------------------
data_worker_config = WorkerConfig(
    id="data_analyst_worker",
    worker_description="You are a data analyst. When asked to look at data, use the analyze_crypto_data tool.",
    get_state_fn=get_state,
    action_space=[analyze_func] # Previously 'functions'
)

# ---------------------------------------------------------
# 5. Initialize the Autonomous Agent
# ---------------------------------------------------------
print("Booting up Virtuals Protocol Agent...")
agent = Agent(
    api_key=os.getenv("GAME_API_KEY"),
    name="Raimunds_A2A_Node",
    # We now embed the task directly into the agent's core goal:
    agent_goal="Analyze this exact data string using your data analyst worker: 'Base Sepolia network traffic spiking 400%'",
    agent_description="A gateway agent connecting Web3 to a local Python environment.",
    get_agent_state_fn=get_state,
    workers=[data_worker_config]
)

# Context manager to temporarily hide the SDK's massive logs
class SuppressSDKLogs:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

# ---------------------------------------------------------
# 6. Trigger the Agentic Game Loop (Clean UI)
# ---------------------------------------------------------
print("Compiling agent and fetching sandbox environment from Virtuals...")
agent.compile()

print("\n==================================================")
print("🤖 AUTONOMOUS AGENT LOOP STARTED")
print("==================================================")

for tick in range(3):
    print(f"\n⏳ [TICK {tick + 1}] Agent is thinking (waiting for LLM routing)...")
    
    # Run the step quietly and CAPTURE the response!
    with SuppressSDKLogs():
        step_response = agent.step()
    
    # --- ROBUST STATE EXTRACTION ---
        current_state = None
        function_result = None

        if isinstance(step_response, tuple):
            for item in step_response:
                # 1. Catch the ActionResponse (which HOLDS the agent_state)
                if hasattr(item, 'agent_state'):
                    current_state = item.agent_state
                
                # 2. Catch the FunctionResult
                elif hasattr(item, 'action_status') and hasattr(item, 'feedback_message'):
                    function_result = item
        else:
            # Fallback if it's a direct object
            current_state = getattr(step_response, 'agent_state', None)

    # --- IMPROVED UI UPDATES ---
    if current_state and hasattr(current_state, 'current_task'):
        task = current_state.current_task.task
        reasoning = current_state.current_task.task_reasoning
        
        print(f"🎯 Current Goal: {task}")
        print(f"🧠 Reasoning:   {reasoning.split('.')[0]}.")
        
        # Display function result if available
        if function_result:
            print(f"⚡ Function Result: {function_result.feedback_message}")
        
        # Check the agent's memory logs
        if current_state.hlp.log:
            last_log = current_state.hlp.log[-1]
            if 'result' in last_log:
                print(f"✅ Memory Updated: {last_log['result']}")
    else:
        print(f"⚠️ Could not parse state object. Available attributes: {dir(step_response) if hasattr(step_response, '__dict__') else 'N/A'}")

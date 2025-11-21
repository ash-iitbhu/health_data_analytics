from typing import TypedDict, Annotated, Sequence
import operator
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, AIMessage
from pydantic import BaseModel

from config.config import Config
from data_generator.data_loader import data_manager
from orchestrator.prompts import get_analyst_prompt, get_supervisor_prompt
from orchestrator.tools import python_repl_tool
from logger import get_logger

logger = get_logger(__name__)

# --- State Definition (Simplified) ---
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str

# --- Global LLM Initialization ---
PRIMARY_LLM: ChatGroq | None = None

# Initialize Primary LLM
if Config.GROQ_API_KEY:
    try:
        PRIMARY_LLM = ChatGroq(
            model=Config.PRIMARY_MODEL_NAME, 
            api_key=Config.GROQ_API_KEY, 
            temperature=0
        )
        logger.info(f"Primary LLM initialized: {Config.PRIMARY_MODEL_NAME} (Groq).")
    except Exception as e:
        logger.error(f"Primary LLM (Groq) initialization failed: {e}")

if not PRIMARY_LLM:
    # Raise a critical error if the primary LLM cannot be configured at startup
    raise RuntimeError("System startup failed: Groq LLM could not be initialized. Check API key.")

# --- Helper function for agent invocation (Simplified) ---
def _get_llm_chain(is_analyst: bool):
    """Creates the appropriate agent chain using the PRIMARY_LLM."""
    
    if is_analyst:
        # Analyst chain: Tool calling
        analyst_prompt = get_analyst_prompt(data_manager.get_schema_context())
        return analyst_prompt | PRIMARY_LLM.bind_tools([python_repl_tool])
    else:
        # Supervisor chain: Structured output
        supervisor_prompt = get_supervisor_prompt()
        class RouterOutput(BaseModel):
            next_actor: str
        return supervisor_prompt | PRIMARY_LLM.with_structured_output(RouterOutput)

# --- Node Functions (Simplified) ---

def supervisor_node(state):
    """Invokes the Supervisor."""
    
    supervisor_chain = _get_llm_chain(is_analyst=False)
    
    logger.info("Supervisor invoked (using Groq).")
    # Errors (like 401 Invalid Key) will now propagate from here
    result = supervisor_chain.invoke(state)
    
    return {
        "sender": "Supervisor", 
        "messages": [AIMessage(content=f"Routing to: {result.next_actor}")]
    }

def analyst_node(state):
    """Invokes the Analyst Agent."""
    
    analyst_agent_chain = _get_llm_chain(is_analyst=True)
    
    logger.info("Analyst Agent invoked (using Groq).")
    # Errors (like Rate Limit) will now propagate from here
    result = analyst_agent_chain.invoke(state)
    
    return {"messages": [result], "sender": "Data_Analyst"}
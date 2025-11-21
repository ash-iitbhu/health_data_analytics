from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from orchestrator.agents import AgentState, analyst_node, supervisor_node 
from orchestrator.tools import python_repl_tool

# --- Conditional Logic (remains the same) ---
def should_continue(state):
    """Determine whether to continue analysis."""
    messages = state["messages"]
    last_message = messages[-1]
    
    if "tool_calls" in last_message.additional_kwargs:
        # The LLM decided to call a tool
        return "tools"
    # The LLM produced a final answer
    return "Supervisor"

# --- Graph Construction ---

workflow = StateGraph(AgentState)

# Nodes
workflow.add_node("Supervisor", supervisor_node)
workflow.add_node("Data_Analyst", analyst_node)
workflow.add_node("tools", ToolNode([python_repl_tool]))

# Edges
workflow.add_edge(START, "Supervisor")

# Conditional Edges
workflow.add_conditional_edges(
    "Supervisor",
    lambda x: x["messages"][-1].content.split("Routing to: ")[-1],
    {
        "Data_Analyst": "Data_Analyst",
        "FINISH": END,
    },
)
workflow.add_conditional_edges("Data_Analyst", should_continue, {"tools": "tools", "Supervisor": "Supervisor"})

# Loop Edge
workflow.add_edge("tools", "Data_Analyst")

app_graph = workflow.compile()
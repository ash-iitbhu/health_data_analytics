import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from orchestrator.graph import app_graph
from logger import get_logger
import json

logger = get_logger("API_Gateway")

app = FastAPI(title="Health GenAI Microservice")

class QueryRequest(BaseModel):
    query: str

@app.post("/analyze")
async def analyze_data(request: QueryRequest):
    logger.info(f"Received query: {request.query}")
    initial_state = {
        "messages": [HumanMessage(content=request.query)],
        "sender": "User"
    }
    
    events = app_graph.stream(initial_state, {"recursion_limit": 25})
    
    final_response = "No response generated."
    execution_log = []

    for event in events:
        for node_name, value in event.items():
            if "messages" in value:
                msg = value["messages"][-1]
                if node_name == "Data_Analyst" and msg.content and not msg.tool_calls:
                    final_response = msg.content
                
                content = msg.content if msg.content else "[Tool Call]"
                execution_log.append(f"{node_name}: {content}")
    logger.info("Analysis complete. Sending response.")
    return {
        "response": final_response,
        "trace": execution_log
    }

if __name__ == "__main__":
    logger.info("Starting Health GenAI Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
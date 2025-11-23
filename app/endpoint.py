from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from typing import List
from langchain_core.messages import HumanMessage
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from workflow import app as agent_graph 
except ImportError:
    agent_graph = None


    
router = APIRouter()


class ResearchRequest(BaseModel):
    topic: str  
    
class ResearchResponse(BaseModel):
    status: str
    message: str
    file_path: str | None = None

def research_stream_generator(topic: str):
    """
    It triggers the LangGraph structure. Because this process takes a long time, 
    it is generally recommended to perform it with BackgroundTasks or asynchronously.
    """
    print(f"🚀 Agent started to work: {topic}")
    
    query = HumanMessage(content= topic)
    inputs = {"messages": [query]}
    
    for event in agent_graph.stream(inputs):
        for node_name, _ in event.items():
            yield json.dumps({"current_agent": node_name}) + "\n"
            
    yield json.dumps({"status": "completed", "file_path": "output/student_number_homeworkname.docx"}) + "\n"

# --- API (Endpoint) ---

@router.post("/start-research-stream", summary="Starts a new academic research")
async def start_research_stream(request: ResearchRequest):
    """
    This endpoint initiates the complex Agent workflow. 
    The Agent searches, writes, checks, and produces a .docx file.r.
    """
    if not agent_graph:
        raise HTTPException(status_code=500, detail="Agent workflow failed to load.")

    return StreamingResponse(research_stream_generator(request.topic), media_type = "application/x-ndjson")
        
        
from pydantic import BaseModel
from typing import List, Dict, Any

class GraphState(BaseModel):
    user_query: str
    agent_type: str = ""
    sql_query: str = ""
    
    query_result: List[Dict[str, Any]] = []
    
    summary: str = ""
    
    messages: List[Any] = []


class Chatting(BaseModel):
    question: str



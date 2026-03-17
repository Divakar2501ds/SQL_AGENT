from fastapi import HTTPException, APIRouter, Depends, status

from schemas.chat_schema import Chatting, GraphState
from utilities.graph import langflow

from utilities.chat_history import upload_chat_in_db, retrieve_chat_in_db


import traceback
router = APIRouter()

@router.post("/chat")
def chat(chat: Chatting):
    try:
        result = langflow(chat.question)

        upload_result = upload_chat_in_db([
            {
                "role": "user",
                "content": chat.question
            },
            {
                "role": "system",  
                "content": result["summary"]
            }
        ])
        
        print(f"Upload result: {upload_result}")
        
        return {
            "message": "Data fetched successfully",
            "llm_response": result["summary"]
        }
    
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )
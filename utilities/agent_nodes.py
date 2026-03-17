from langgraph.graph import StateGraph

from database.database import run_sql, create_connection
from schemas.chat_schema import GraphState
from utilities.llm_setup import novita_client
from utilities.prompting import SYSTEM_PROMPT, SYSTEM_PROMPT_1
from utilities.chat_history import retrieve_chat_in_db

def decide_agent_node(state: GraphState) -> dict:
    response = novita_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
You are an agent router.

Decide which agent should handle the user question.

Database-related questions usually involve:
- template, templates
- section, sections
- document, documents, uploaded
- count, how many
- user, users
- role, roles
- policy

Rules:
- If the question requires database querying → respond with: sql
- Otherwise → respond with: general

IMPORTANT:
If the question is about a real-world person, place, history, science, sports, or general knowledge,
it is ALWAYS "general" — even if words like "who", "how many", or names appear.
Return ONLY ONE WORD:
sql
or
general
"""
            },
            {
                "role": "user",
                "content": f"User Question:\n{state.user_query}"
            }
        ]
    )

    agent = response.choices[0].message.content.strip().lower()

    if agent not in ["sql", "general"]:
        agent = "general"

    print("Decided agent:", agent)

    return {
        "agent_type": agent
    }

def route_agent(state: GraphState) -> str:
    return "sql_agent" if state.agent_type == "sql" else "general_agent"



def sql_agent_node(state: GraphState):
    messages = []

    messages.append({
        "role": "system",
        "content": SYSTEM_PROMPT
    })
    messages.append({
        "role": "system",
        "content": (
            "You are also given the last 10 messages of a conversation.\n"
            "Use them only to resolve context, references, and follow-up questions "
            "(for example: pronouns like 'his', 'that', 'those').\n"
            "Do NOT explain anything. Output only valid SQL."
        )
    })

    for msg_group in state.messages:
        if "chat" in msg_group:
            for chat_msg in msg_group["chat"]:
                role = chat_msg.get("role", "user")

                if role == "system":
                    role = "assistant"

                messages.append({
                    "role": role,
                    "content": chat_msg.get("content", "")
                })
        else:
            role = msg_group.get("role", "user")
            if role == "system":
                role = "assistant"

            messages.append({
                "role": role,
                "content": msg_group.get("content", "")
            })

    messages.append({
        "role": "user",
        "content": state.user_query
    })

    response = novita_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        temperature=0,
        messages=messages
    )

    sql = response.choices[0].message.content.strip()

    return {
        "sql_query": sql
    }

def run_query_node(state: GraphState) -> dict:
    query = state.sql_query
    conn = create_connection()
    result = run_sql(conn=conn, sql=query)
    conn.close()
    return {"query_result": [dict(row) for row in result]}


def summarise_data_node(state: GraphState) -> dict:
    retrieved_data = state.query_result
    response = novita_client.chat.completions.create(
     model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_1},
            {"role": "user", "content": f"User Question: {state.user_query}\nDatabase Result: {retrieved_data}"}
        ]
    )

    summarised_result = response.choices[0].message.content.strip()
    return {"summary": summarised_result} 

def general_agent_node(state: GraphState):
    messages = []

    messages.append({
  "role": "system",
  "content": """
You are a helpful and context-aware assistant.

- Always prioritize the most recent messages at the top of the conversation history when answering.
- Use the conversation history to answer the user's current question.
- Resolve references (like "he", "she", "it", "their", "its") based on the most recent relevant context first.
- Only provide information relevant to the inferred subject; ignore unrelated earlier topics.
- If the user's question is ambiguous or cannot be linked to previous context, ask a concise clarification question.
- Be concise, clear, and accurate. Do not assume facts not present in the history.
- When the answer is a negative fact (e.g., "does not exist" or "has no X"), clearly state it.
"""
})

    for msg_group in state.messages:
        if isinstance(msg_group, dict) and "chat" in msg_group:
            for chat_msg in msg_group["chat"]:
                role = chat_msg.get("role", "user")
                if role == "system":
                    role = "assistant"
                messages.append({
                    "role": role,
                    "content": chat_msg.get("content", "")
                })
        elif isinstance(msg_group, dict) and "role" in msg_group:
            messages.append({
                "role": msg_group.get("role", "user"),
                "content": msg_group.get("content", "")
            })

    messages.append({
        "role": "user",
        "content": state.user_query
    })

    response = novita_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        temperature=0,
        messages=messages
    )

    answer = response.choices[0].message.content.strip()



    return {"summary": answer} 
from langgraph.graph import StateGraph, START, END
from schemas.chat_schema import GraphState
import json
from utilities.agent_nodes import sql_agent_node, run_query_node, summarise_data_node, decide_agent_node, general_agent_node, route_agent
from utilities.chat_history import retrieve_chat_in_db

from langgraph.graph import StateGraph, START, END

def langflow(question: str):

    history = retrieve_chat_in_db()
    state_input = GraphState(
        user_query=question,
        messages=history
    )

    graph = StateGraph(GraphState)

    graph.add_node("decider", decide_agent_node)
    graph.add_node("sql_agent", sql_agent_node)
    graph.add_node("execute_sql", run_query_node)
    graph.add_node("summarised_data", summarise_data_node)
    graph.add_node("general_agent", general_agent_node)

    graph.add_edge(START, "decider")

    graph.add_conditional_edges(
        "decider",
        route_agent,
        {
            "sql_agent": "sql_agent",
            "general_agent": "general_agent",
        }
    )

    graph.add_edge("sql_agent", "execute_sql")
    graph.add_edge("execute_sql", "summarised_data")
    graph.add_edge("summarised_data", END)

    graph.add_edge("general_agent", END)

    app = graph.compile()
    return app.invoke(state_input)

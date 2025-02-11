from nodes.graph_state import ChatbotState
from nodes.feature_extractor import feature_extractor
from nodes.response_generator import response_generator

from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

def get_chatbot_engine() -> CompiledStateGraph:

    workflow = StateGraph(ChatbotState)

    # workflow.add_node(query_checker)
    workflow.add_node(feature_extractor)
    workflow.add_node(response_generator)
    # workflow.add_node(invalid_query)

    # workflow.set_conditional_entry_point(
    #     path=lambda state: {
    #         "valid query" if state["is_valid_query"] else "invalid query"
    #     },
    #     path_map = {
    #         "valid_query": "feature_extractor",
    #         "invalid_query": "unhandled_query"
    #     }
    # )
    workflow.set_entry_point("feature_extractor")
    workflow.add_edge("feature_extractor", "response_generator")
    workflow.set_finish_point("response_generator")

    graph: CompiledStateGraph = workflow.compile()
    graph.get_graph().draw_mermaid_png(output_file_path="graph_arch.png")
    return graph
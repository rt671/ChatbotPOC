from langchain_core.messages import SystemMessage, HumanMessage
from nodes.graph_state import ChatbotState
from langchain_anthropic import ChatAnthropic
import json

feature_extractor_system_prompt = """
Extract keywords from the user query regarding services
"""

feature_extractor_user_prompt = """\
User Query:  `{user_query}`
"""

def feature_extractor(state: ChatbotState) -> ChatbotState:
    user_query = state["messages"][-1].content
    llm = ChatAnthropic(model='claude-3-opus-20240229')

    response = llm.invoke(
        input=[
            SystemMessage(content=feature_extractor_system_prompt),
            HumanMessage(content=feature_extractor_user_prompt.format(user_query=user_query))
        ]
    )


    try:
        extracted_attributes = json.loads(response.content.strip())
    except json.JSONDecodeError:
        extracted_attributes = {"service_name": None, "service_location": None}

    state.query_attributes["service_name"] = extracted_attributes.get("service_name")
    state.query_attributes["service_location"] = extracted_attributes.get("service_location")

    return state
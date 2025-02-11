from langchain_core.messages import SystemMessage, HumanMessage
from nodes.graph_state import ChatbotState
from langchain_anthropic import ChatAnthropic

response_generator_system_prompt = """
Based on the extracted query attributes, generate a response as per asked in the query.
If no attributes are extracted, ask the user for more details.
"""

response_generator_user_prompt = """\
Extracted Attributes:
- Service Name: {service_name}
- Service Location: {service_location}
"""

def response_generator(state: ChatbotState) -> ChatbotState:
    service_name = state.query_attributes.get("service_name", "Unknown")
    service_location = state.query_attributes.get("service_location", "Unknown")

    response = ChatAnthropic.invoke(
        [
            SystemMessage(content=response_generator_system_prompt),
            HumanMessage(content=response_generator_user_prompt.format(
                service_name=service_name,
                service_location=service_location
            ))
        ]
    )

    state.messages.append({"role": "assistant", "content": response.content.strip()})
    return state 

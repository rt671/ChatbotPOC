from langgraph.graph import MessagesState
from pydantic import BaseModel, Field
from typing import Optional, Union, Dict

class ChatbotState(MessagesState):
    query_attributes: Dict[str, Union[str, float, None]]
    is_valid_query: bool

def get_empty_state() -> ChatbotState:
    state = ChatbotState(
        messages= [],
        query_attributes={
            "service_name":None,
            "service_location": None
        },
        is_valid_query=None,
    )
    print("RETURNING TYPE AS: ", type(state))
    return state

class QueryAttributes(BaseModel):
    service_name: Optional[str] = Field(
        None, description="fetch the service name mentioned in the query if present"
    )

    service_location: Optional[str] = Field(
        None, description="fetch the location of the service, the place where this service is."
    )
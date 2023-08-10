import openai
from abc import ABC, abstractmethod
from typing import Any, Literal

class LLM(ABC):
    @abstractmethod
    def call_llm(self, conversation: Any) -> str:
        pass

    def message_loop(self, conversation: Any, user_message: str) -> None:
        # Perhaps add this in convo instead?
        conversation.add_message("user", user_message)
        llm_response = self.call_llm(conversation)
        conversation.add_message("assistant", llm_response, extract=True)
        return llm_response

class OpenaiGpt(LLM):
    def __init__(self, model: Literal["gpt-3.5-turbo-0613", "gpt-4"] = "gpt-3.5-turbo-0613"):
        self.model = model

    def call_llm(self, conversation: Any) -> dict:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=conversation.conversation_history,
        )
        return response

    def call_llm_functions(self, conversation) -> dict:
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo-0613",
        #     messages=conversation.conversation_history,
        #     functions=orchestrator.create_function_descriptions(),
        #     function_call="auto",
        # )
        # return response
        raise NotImplementedError


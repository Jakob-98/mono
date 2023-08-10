import openai
from abc import ABC, abstractmethod
from typing import Any, Literal

class LLM(ABC):
    @abstractmethod
    def call_llm(self, conversation: Any) -> dict:
        pass

class OpenaiGpt(LLM):
    def __init__(self, model: Literal["gpt-3.5-turbo-0613", "gpt-4"] = "gpt-3.5-turbo-0613"):
        self.model = model

    def call_llm(self, conversation: Any) -> dict:
        response = openai.ChatCompletion.create(
            model=self.model,  # Use the model property here
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


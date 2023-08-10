"""Personas module"""

from abc import ABC, abstractmethod

class Persona(ABC):
    def __init___(self):
        self.system_message: str

    def get_system_message(self):
        return self.system_message


class IntentRecognizer(Persona):
    def __init__(self):
        self.system_message = """
        You are an AI agent working in a chat context. Your purpose is to recognize the intent of the user's message.
        """

class Assistant(Persona):
    def __init__(self):
        self.system_message = """
        You are an AI agent working in a chat context. Your purpose is to assist the user.
        """



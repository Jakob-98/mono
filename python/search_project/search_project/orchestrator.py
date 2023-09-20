from search_project.context import Context

class Orchestrator:
    def __init__(self, llm: "LLM", context):
        self.llm = llm
        self.context = context

    def user_message(self, message: str):
        # Check for special commands before interacting with the LLM
        if message.startswith("/"):
            self.context.run_command(message)
            return

        # Proceed with regular interaction
        response = self.message_loop(message)

        # Assuming you want to display the conversation after a user message
        if self.context.display_conversation:
            self.context.conversation.display_last_message()
        return response

    def message_loop(self, user_message: str) -> None:
        # Add the user message to the conversation
        self.context.conversation.add_message("user", user_message)

        # Get the response from the LLM
        llm_response = self.llm.call_llm(self.context.conversation)

        # Add the LLM's response to the conversation
        self.context.conversation.add_message("assistant", llm_response, extract=True)

        return llm_response

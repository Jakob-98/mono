import uuid

class Context():
    def __init__(self, persona, display_conversation=True):
        self.persona = persona
        self.display_conversation = display_conversation
        self.id = uuid.uuid4()
        self.conversation = Conversation()
        self.conversation.add_message("assistant", self.persona.get_system_message())

    def run_command(self, message):
        if message == "/help":
            # Implementation for help command
            raise NotImplementedError
        if message == "/clear":
            self.conversation = Conversation()
            self.conversation.add_message("assistant", self.persona.get_system_message())


class Conversation:
    def __init__(self, max_tokens=1024, max_messages=10):
        self.conversation_history = []
        self.max_tokens = max_tokens
        self.max_messages = max_messages
        self.current_token_count = 0

    def approximate_tokens(self, message):
        """Returns an approximation of token count for a given message."""
        return len(message.split())

    def truncate_conversation(self, new_token_count):
        # Retrieve and modify the original system message
        system_message = self.conversation_history[0]
        
        # Remove earlier messages until within limits
        while len(self.conversation_history) > self.max_messages or (self.current_token_count + new_token_count) > self.max_tokens:
            removed_message = self.conversation_history.pop(1)  # remove the next message after the system message
            self.current_token_count -= self.approximate_tokens(removed_message["content"])

        # Re-add the modified system message
        self.conversation_history[0] = system_message

    def add_message(self, role, content, extract=False, function_name=None):
        if extract:
            content = content["choices"][0]["message"]["content"]

        new_token_count = self.approximate_tokens(content)
        
        # Check if the new message exceeds the token or message limit and truncate if necessary
        if (new_token_count + self.current_token_count > self.max_tokens) or (len(self.conversation_history) >= self.max_messages):
            self.truncate_conversation(new_token_count)

        # Create and add the new message
        if function_name is None:
            message = {"role": role, "content": content}
        else:
            message = {
                "role": role,
                "content": content,
                "name": function_name,
            }
        self.conversation_history.append(message)
        self.current_token_count += new_token_count

    def display_conversation(self):
        for message in self.conversation_history:
            print(f"{message['role']}: {message['content']}\n\n")

    def display_last_message(self):
        last_message = self.conversation_history[-1]
        print(f"{last_message['role']}: {last_message['content']}\n\n")


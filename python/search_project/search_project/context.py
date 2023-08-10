class Context():
    def __init__(self, persona, display_conversation=True):
        self.persona = persona
        self.display_conversation = display_conversation
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
    def __init__(self):
        self.conversation_history = []

    def add_message(self, role, content, extract=False, function_name=None):

        # TODO tightly coupled to openai.ChatCompletion.create
        if extract:
            content = content["choices"][0]["message"]["content"]

        # conditionally build message:
        if function_name is None:
            message = {"role": role, "content": content}
        else:
            message = {
                "role": role,
                "content": content,
                "name": function_name,
            }
        self.conversation_history.append(message)

    def display_conversation(self):
        for message in self.conversation_history:
            print(f"{message['role']}: {message['content']}\n\n")

    def display_last_message(self):
        last_message = self.conversation_history[-1]
        print(f"{last_message['role']}: {last_message['content']}\n\n")


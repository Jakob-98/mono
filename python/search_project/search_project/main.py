from search_project.context import Context
from search_project.persistence import ContextDB
from search_project.llm import OpenaiGpt
from search_project.personas import Assistant
from search_project.orchestrator import Orchestrator

def display_contexts(db):
    contexts = db.list_last_contexts(limit=10)
    if not contexts:
        print("No previous conversations found.")
        return None

    print("\nPrevious Conversations:\n")
    for idx, (id, convo) in enumerate(contexts):
        print(f"{idx + 1}. Conversation {id}: {convo[:50]}...")  # Displaying first 50 chars
    
    return contexts

def select_context(db):
    contexts = display_contexts(db)

    if contexts:
        while True:
            choice = input("\nEnter number to select a context, 'n' to start a new one, or 'q' to quit: ").strip().lower()

            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(contexts):
                    selected_context = Context(Assistant())
                    selected_context.conversation.conversation_history = eval(contexts[idx][1])
                    return selected_context
                else:
                    print("Invalid choice. Please select a valid conversation number.")
            elif choice == 'n':
                return Context(Assistant())
            elif choice == 'q':
                print("Goodbye!")
                exit()
            else:
                print("Invalid input. Please try again.")
    else:
        return Context(Assistant())

def user_interact_with_orchestrator(orchestrator, db):
    print("\nStart the conversation (type 'exit' to end the session):")
    while True:
        user_msg = input("You: ").strip()
        if user_msg.lower() == 'exit':
            print("Ending conversation. Goodbye!")
            break
        orchestrator.user_message(user_msg)
        db.save_context(orchestrator.context)  # Save context after each message

# def main():
#     db = ContextDB()
    
#     selected_context = select_context(db)
    
#     # Assuming you have defined your LLM and persona
#     llm = OpenaiGpt()
    
#     orchestrator = Orchestrator(llm, selected_context)

#     user_interact_with_orchestrator(orchestrator, db)
    
#     # Save the current conversation to the database when finished
#     db.save_context(selected_context)

# if __name__ == "__main__":
#     main()

import sys

def main():
    db = ContextDB()

    # If a message is passed as a CLI argument
    if len(sys.argv) > 1:
        msg = sys.argv[1]
        # Assuming you always want to use the last context for CLI messages
        last_context = db.load_last_context()
        llm = OpenaiGpt()
        orchestrator = Orchestrator(llm, last_context)
        orchestrator.user_message(msg)
        return  # Exit after processing the single CLI message

    # Otherwise, the interactive mode:
    selected_context = select_context(db)
    llm = OpenaiGpt()
    orchestrator = Orchestrator(llm, selected_context)
    user_interact_with_orchestrator(orchestrator, db)  # Note the added db parameter

if __name__ == "__main__":
    main()

# main.py
from agent import create_agent_executor
import sys # To exit the script

def main():
    """Main function to run the agent chat loop."""
    print("Setting up the agent...")
    try:
        agent_executor = create_agent_executor()
        print("\nAgent setup complete. You can now chat with the agent.")
        print("Type 'quit', 'exit', or 'bye' to end the conversation.")
        print("-" * 50)

        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() in ["quit", "exit", "bye"]:
                    print("Agent: Goodbye!")
                    sys.exit() # Exit the script cleanly

                if not user_input:
                    continue # Skip empty input

                # Invoke the agent with the user's input
                # The input is passed as a dictionary, matching the prompt's expected variable name ('input')
                response = agent_executor.invoke({"input": user_input})

                # Print the final answer from the agent
                print(f"Agent: {response.get('output', 'Sorry, I could not process that.')}") # Safely get the output

            except KeyboardInterrupt:
                 print("\nAgent: Goodbye! (Interrupted by user)")
                 sys.exit()
            except Exception as e:
                print(f"An error occurred: {e}")
                # Optionally, decide if you want to break the loop on error or continue
                # break

    except Exception as e:
        print(f"Failed to initialize the agent: {e}")
        sys.exit(1) # Exit with an error code

if __name__ == "__main__":
    main()
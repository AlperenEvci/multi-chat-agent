import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables (specifically GROQ_API_KEY)
load_dotenv()

print("Testing Groq API connection...")

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("Error: GROQ_API_KEY not found in .env file.")
else:
    try:
        client = Groq(api_key=api_key)
        print("Groq client created successfully.")

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Explain the importance of low-latency LLMs",
                }
            ],
            model="llama3-8b-8192",
        )

        print("API call successful!")
        print("Response:")
        print(chat_completion.choices[0].message.content)

    except Exception as e:
        print("\n--- An Error Occurred ---")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Details: {e}")
        import traceback
        print("\n--- Traceback ---")
        traceback.print_exc() # Print the full traceback

print("\nTest complete.") 
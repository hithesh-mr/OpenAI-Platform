from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv
from colorama import Fore, Style, init

init()

# Load environment variables from .env at project root
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)

# Initialize OpenAI client
api_key = os.getenv("API_KEY")
if not api_key:
    print(f"{Fore.RED}Error: API_KEY not found in .env file.{Style.RESET_ALL}")
    print("Please ensure you have a .env file in the project root with your OpenAI API key.")
    exit(1)

client = OpenAI(api_key=api_key)

def get_chat_response(messages, model="gpt-4.1"):
    """Get a chat response from OpenAI API"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print(f"{Fore.CYAN}=== GPT-4.1 Chatbot ==={Style.RESET_ALL}")
    print("Type 'exit' or 'quit' to end the conversation.")
    print(f"{Fore.YELLOW}You are now chatting with GPT-4.1. How can I help you today?{Style.RESET_ALL}")

    conversation = [
        {"role": "system", "content": "You are a helpful AI assistant named GPT-4.1."}
    ]

    while True:
        try:
            user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}")
            if user_input.lower() in ('exit', 'quit'):
                print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                break

            conversation.append({"role": "user", "content": user_input})
            print(f"{Fore.BLUE}GPT-4.1: {Style.RESET_ALL}", end="", flush=True)
            response = get_chat_response(conversation)
            print(response)
            conversation.append({"role": "assistant", "content": response})
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    main()
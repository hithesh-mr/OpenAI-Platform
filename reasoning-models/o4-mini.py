from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored terminal text
init()

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)

# Initialize the OpenAI client
api_key = os.getenv("OPENAI_API_KEY")

# Check if API key is set
if not api_key:
    print(f"{Fore.RED}Error: OPENAI_API_KEY not found in .env file.{Style.RESET_ALL}")
    print(f"Please make sure you have a .env file in the project root with your OpenAI API key.")
    exit(1)

client = OpenAI(api_key=api_key)

def get_chat_response(messages, model="gpt-4o-mini"):
    """Get a response from the OpenAI API"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print(f"{Fore.CYAN}=== O4-Mini Chatbot ==={Style.RESET_ALL}")
    print("Type 'exit' or 'quit' to end the conversation.")
    print(f"{Fore.YELLOW}You are now chatting with O4-Mini. How can I help you today?{Style.RESET_ALL}")
    
    # Initialize conversation history
    conversation = [
        {"role": "system", "content": "You are a helpful AI assistant named O4-Mini. "
                              "You provide clear, concise, and helpful responses."}
    ]
    
    while True:
        try:
            # Get user input
            user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}")
            
            # Check for exit command
            if user_input.lower() in ('exit', 'quit'):
                print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                break
                
            # Add user message to conversation history
            conversation.append({"role": "user", "content": user_input})
            
            # Get AI response
            print(f"{Fore.BLUE}O4-Mini: {Style.RESET_ALL}", end="", flush=True)
            response = get_chat_response(conversation)
            print(f"{response}")
            
            # Add AI response to conversation history
            conversation.append({"role": "assistant", "content": response})
            
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    main()

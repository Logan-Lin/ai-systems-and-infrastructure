#!/usr/bin/env python3
"""
Example implementation for API Fundamentals course.
Demonstrates HTTP request/response, REST principles, and API security.
"""

import os
import sys
import json
import requests  # Using requests library for transparency into HTTP mechanics
from typing import List, Dict
from dotenv import load_dotenv

# Load API key from .env file - Security best practice: Never hardcode API keys!
load_dotenv()


class ClaudeChatbot:
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key
        # API URL structure: protocol (https) + domain (api.anthropic.com) + path (/v1/messages)
        # The 'v1' indicates API version - following REST uniform interface principle
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.model = model
        # Store conversation history to demonstrate REST statelessness principle
        # Each request must contain complete context
        self.messages: List[Dict[str, str]] = []
        self.system_message = "You are a helpful assistant."
        
    def set_system_message(self, message: str):
        self.system_message = message
        
    def clear_conversation(self):
        self.messages = []
        print("Conversation cleared.")
        
    def chat(self, user_input: str) -> str:
        # Add user message to history for stateless communication
        self.messages.append({"role": "user", "content": user_input})
        
        try:
            # HTTP Request Headers - metadata about the request
            headers = {
                "x-api-key": self.api_key,          # Authorization header for API authentication
                "anthropic-version": "2023-06-01",  # API version specification
                "content-type": "application/json"  # Tells server we're sending JSON data
            }
            
            # HTTP Request Body - the actual data we're sending
            # JSON format as specified by Content-Type header
            payload = {
                "model": self.model,
                "max_tokens": 4096,
                "system": self.system_message,
                "messages": self.messages  # Full history = REST statelessness
            }
            
            # HTTP POST method - used for sending data and expecting a response
            # (vs GET which only retrieves data)
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30  # Network timeout for resilience
            )
            
            # Check HTTP Status Code (part of HTTP Response Status Line)
            # 200 = OK/Success, 4xx = Client errors, 5xx = Server errors
            if response.status_code != 200:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', f'API Error: {response.status_code}')
                raise Exception(error_msg)
            
            # Parse HTTP Response Body - contains the actual AI response
            response_data = response.json()
            # Extract text from Claude's response structure
            assistant_message = response_data['content'][0]['text']
            # Store response for conversation continuity
            self.messages.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
            
        except requests.exceptions.Timeout:
            error_msg = "Request timed out"
            print(f"Error: {error_msg}")
            self.messages.pop()
            return error_msg
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            print(f"Error: {error_msg}")
            self.messages.pop()
            return error_msg
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"Error: {error_msg}")
            self.messages.pop()
            return error_msg


def main():
    # Security: Load API key from environment variable, not hardcoded!
    # This follows the Authorization best practices from the course
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key:")
        print("ANTHROPIC_API_KEY=your-api-key-here")
        sys.exit(1)
    
    chatbot = ClaudeChatbot(api_key)
    
    print("="*50)
    print("Claude Command Line Chatbot")
    print("="*50)
    print("Commands:")
    print("  • Type 'quit' or 'exit' to end")
    print("  • Type 'clear' to reset conversation")
    print("  • Type 'system' to change system message")
    print("="*50)
    
    while True:
        try:
            user_input = input("\nYou: ")
            
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
                
            elif user_input.lower() == 'clear':
                chatbot.clear_conversation()
                continue
                
            elif user_input.lower() == 'system':
                new_system = input("Enter new system message: ")
                chatbot.set_system_message(new_system)
                print("System message updated.")
                continue
                
            print("\nClaude:")
            response = chatbot.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()

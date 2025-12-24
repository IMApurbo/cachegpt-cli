import requests
import json
import sys
from datetime import datetime

# API endpoint
URL = "https://cachegpt.app/api/v2/unified-chat-stream"

# Headers copied from your example (some may be optional, but keeping them for compatibility)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/json",
    "x-user-timezone": "America/New_York",  # Change if you're in a different timezone
    "x-timezone-offset": "300",
    "Origin": "https://cachegpt.app",
    "Referer": "https://cachegpt.app/chat",
    "Connection": "close",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=4"
}

def chat():
    print("CacheGPT Chatbot (using Llama-3.3-70B via cachegpt.app)")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    
    # Conversation history (optional, but improves context if you send previous messages)
    history = []
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Add user message to history
        user_message = {
            "role": "user",
            "content": user_input,
            "created_at": datetime.utcnow().isoformat() + "Z"  # Optional timestamp
        }
        history.append(user_message)
        
        # Payload
        payload = {
            "messages": history,
            "qualityMode": "fast"  # You can change to "best" if available
        }
        
        try:
            # Stream the response
            response = requests.post(
                URL,
                headers=HEADERS,
                json=payload,
                stream=True,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"Error: HTTP {response.status_code} - {response.text}")
                history.pop()  # Remove failed message
                continue
            
            print("Bot: ", end="", flush=True)
            full_response = ""
            
            for line in response.iter_lines():
                if line:
                    line = line.decode("utf-8").strip()
                    if line.startswith("data: "):
                        data = line[6:].strip()
                        if data == "[DONE]":  # Sometimes APIs send this
                            break
                        try:
                            json_data = json.loads(data)
                            content = json_data.get("content", "")
                            done = json_data.get("done", False)
                            
                            # Print only the new part
                            new_text = content[len(full_response):]
                            print(new_text, end="", flush=True)
                            full_response = content
                            
                            if done:
                                # Optionally extract model info
                                model = json_data.get("model", "unknown")
                                # print(f"\n[Model: {model}]")
                                break
                        except json.JSONDecodeError:
                            pass  # Ignore invalid lines
            
            print("\n")  # New line after response
            
            # Add assistant response to history for context in next turns
            if full_response:
                assistant_message = {
                    "role": "assistant",
                    "content": full_response,
                    "created_at": datetime.utcnow().isoformat() + "Z"
                }
                history.append(assistant_message)
        
        except requests.exceptions.RequestException as e:
            print(f"\nConnection error: {e}")
        except Exception as e:
            print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    chat()

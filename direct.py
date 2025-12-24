import requests
import json
from datetime import datetime, timezone

# API endpoint
URL = "https://cachegpt.app/api/v2/unified-chat-stream"

# Minimal headers (these work fine)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Content-Type": "application/json",
    "Origin": "https://cachegpt.app",
    "Referer": "https://cachegpt.app/chat",
}

def get_utc_now_iso():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def chat():
    print("CacheGPT Chatbot (Llama-3.3-70B) - Full response at once")
    print("Type 'exit', 'quit', or 'bye' to end.\n")
    
    history = []
    
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Add user message
        history.append({
            "role": "user",
            "content": user_input,
            "created_at": get_utc_now_iso()
        })
        
        payload = {
            "messages": history,
            "qualityMode": "fast"
        }
        
        try:
            with requests.post(URL, headers=HEADERS, json=payload, stream=True, timeout=60) as response:
                if response.status_code != 200:
                    print(f"\nError: HTTP {response.status_code}")
                    print(response.text[:500])
                    history.pop()
                    continue
                
                full_response = ""
                
                # Collect all chunks until "done": true
                for line in response.iter_lines():
                    if not line:
                        continue
                    line = line.decode("utf-8").strip()
                    
                    if not line.startswith("data: "):
                        continue
                    
                    data_str = line[6:].strip()
                    if data_str == "[DONE]":
                        break
                    
                    try:
                        data = json.loads(data_str)
                        content = data.get("content", "")
                        done = data.get("done", False)
                        
                        full_response = content  # Always take the latest full content
                        
                        if done:
                            break
                    except json.JSONDecodeError:
                        continue
                
                # Print the complete response all at once
                if full_response.strip():
                    print("Bot:", full_response.strip())
                    print()  # Empty line for readability
                    
                    # Save assistant message to history
                    history.append({
                        "role": "assistant",
                        "content": full_response,
                        "created_at": get_utc_now_iso()
                    })
                else:
                    print("Bot: (No response received)")
                    history.pop()  # Remove user message if no reply
                
        except requests.exceptions.Timeout:
            print("\nTimeout: Request took too long.")
            history.pop()
        except requests.exceptions.ConnectionError:
            print("\nConnection error. Check your internet.")
            history.pop()
        except requests.exceptions.RequestException as e:
            print(f"\nRequest failed: {e}")
            history.pop()

if __name__ == "__main__":
    chat()

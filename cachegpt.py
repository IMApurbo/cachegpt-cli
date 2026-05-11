#!/usr/bin/env python3

import requests
import json
import argparse
import sys
from datetime import datetime, timezone

# ====================== CONFIG ======================
URL = "https://cachegpt.app/api/v2/unified-chat-stream"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "*/*",
    "Content-Type": "application/json",
    "Origin": "https://cachegpt.app",
    "Referer": "https://cachegpt.app/chat",
}

QUALITY_MODE = "fast"  # Change to "best" if desired
# ===================================================

def get_utc_now_iso():
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds') + "Z"

def send_message(history):
    payload = {
        "messages": history,
        "qualityMode": QUALITY_MODE
    }

    try:
        with requests.post(URL, headers=HEADERS, json=payload, stream=True, timeout=60) as response:
            if response.status_code != 200:
                return None, f"HTTP {response.status_code}: {response.text[:200]}"

            full_response = ""
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
                    full_response = content
                    if done:
                        break
                except json.JSONDecodeError:
                    continue

            return full_response.strip(), None

    except requests.exceptions.Timeout:
        return None, "Timeout: Request took too long"
    except requests.exceptions.ConnectionError:
        return None, "Connection error"
    except Exception as e:
        return None, f"Error: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="CacheGPT Chatbot with per-conversation message limit")
    parser.add_argument("--limit", type=int, default=50, help="Max user messages per conversation (default: 50)")
    args = parser.parse_args()

    if args.limit < 1:
        print("Limit must be at least 1")
        sys.exit(1)

    print(f"=== CacheGPT Chatbot (Llama-3.3-70B) ===")
    print(f"Message limit per conversation: {args.limit}")
    print("Type 'exit', 'quit', or 'bye' to quit.\n")

    conversation_count = 1
    message_count = 0
    history = []

    print(f"--- Conversation #{conversation_count} started ---")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye!")
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
        message_count += 1

        print("Bot: ", end="", flush=True)

        response, error = send_message(history)

        if error:
            print(f"\nError: {error}")
            # Don't count this as a successful message, remove last user input
            history.pop()
            message_count -= 1
            continue

        if response:
            print(response)
            # Add assistant response to history
            history.append({
                "role": "assistant",
                "content": response,
                "created_at": get_utc_now_iso()
            })
        else:
            print("(No response)")
            history.pop()
            message_count -= 1

        print()  # Empty line

        # Check if limit reached
        if message_count >= args.limit:
            print(f"\n{'='*50}")
            print(f"LIMIT REACHED ({args.limit} messages)")
            print(f"Starting new conversation...")
            print(f"{'='*50}\n")

            # Reset for new conversation
            conversation_count += 1
            message_count = 0
            history = []  # Clear history
            print(f"--- Conversation #{conversation_count} started ---")

if __name__ == "__main__":
    main()

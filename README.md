# 🤖 CacheGPT CLI

A minimal command-line chatbot powered by [CacheGPT](https://cachegpt.app) running **Llama-3.3-70B**. Supports streaming responses, full conversation history, and automatic session resets when a message limit is reached.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow)
![requests](https://img.shields.io/badge/requests-latest-lightgrey)

---

## ✨ Features

- Chat with **Llama-3.3-70B** directly from your terminal
- Streaming responses with full conversation history
- Configurable per-conversation message limit
- Auto-resets to a fresh conversation when the limit is reached
- Timestamps on every message (`UTC`)
- Graceful error handling for timeouts and connection issues
- `Ctrl+C` or `exit`/`quit`/`bye` to quit cleanly

---

## 🚀 Installation

```bash
git clone https://github.com/IMApurbo/cachegpt-cli.git
cd cachegpt-cli
pip install requests
```

---

## ▶️ Usage

```bash
python cachegpt.py
```

**With a custom message limit:**

```bash
python cachegpt.py --limit 20
```

### Arguments

| Argument | Description | Default |
|---|---|---|
| `--limit` | Max user messages before starting a new conversation | `50` |

---

## 💡 Examples

**Default — 50 messages per conversation:**
```bash
python cachegpt.py
```

**Short sessions of 10 messages:**
```bash
python cachegpt.py --limit 10
```

**In-chat commands:**

| Input | Action |
|---|---|
| `exit` / `quit` / `bye` | End the session |
| `Ctrl+C` | Force quit |

---

## ⚙️ Configuration

At the top of `cachegpt.py` you can change the quality mode:

```python
QUALITY_MODE = "fast"   # Change to "best" for higher quality responses
```

---

## 📋 Requirements

```
requests
```

```bash
pip install requests
```

---

## 📁 Project Structure

```
cachegpt-cli/
├── cachegpt.py    # Main script
└── README.md
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**IMApurbo**  
GitHub: [@IMApurbo](https://github.com/IMApurbo)

---

> No API key needed. Just run and chat.

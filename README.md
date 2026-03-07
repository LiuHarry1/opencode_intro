# Python CLI Chatbot (OpenAI-compatible)

Tiny interactive CLI chatbot that talks to an OpenAI API-compatible server.
Stdlib-only (no dependencies).

## Requirements

- Python 3.x (any reasonably recent version)

## Defaults + Configuration

Environment variables:

- `OPENAI_BASE_URL` (default: `http://localhost:4141`)
- `OPENAI_API_KEY` (default: `dummy`)
- `OPENAI_MODEL` (default: `gpt-4`)

Notes:

- The script accepts either `http://host:port` or `http://host:port/v1`.
  If `/v1` is missing, it is added automatically.

## Run

```bash
python3 chatbot.py
```

or (alias entrypoint):

```bash
python3 main.py
```

Override settings:

```bash
OPENAI_BASE_URL="http://localhost:4141" \
OPENAI_API_KEY="dummy" \
OPENAI_MODEL="gpt-4" \
python3 chatbot.py
```

Example (OpenAI API):

```bash
OPENAI_BASE_URL="https://api.openai.com/v1" \
OPENAI_API_KEY="$OPENAI_API_KEY" \
OPENAI_MODEL="gpt-4" \
python3 chatbot.py
```

## Commands

- `/help` show help
- `/reset` clear conversation
- `/system TEXT` set the system prompt (replaces existing)
- `/exit` quit
- `/quit` quit

## Equivalent curl (example)

If your server is OpenAI-compatible, this should work:

```bash
curl http://localhost:4141/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dummy" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Say hello."}
    ],
    "temperature": 0.7,
    "stream": false
  }'
```

## Troubleshooting

- Seeing `HTTP 401`/`403`: check `OPENAI_API_KEY` and whether your server expects a different auth scheme.
- Seeing `HTTP 404`: check `OPENAI_BASE_URL` (the script posts to `.../v1/chat/completions`).
- Seeing `Network error`: verify the host/port is reachable and the server is running.

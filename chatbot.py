#!/usr/bin/env python3
"""Simple CLI chatbot for an OpenAI-compatible endpoint.

Defaults:
- Base URL: http://localhost:4141/v1
- Model: gpt-4
- API key: dummy

Environment variables:
- OPENAI_BASE_URL (e.g. http://localhost:4141/v1)
- OPENAI_API_KEY
- OPENAI_MODEL
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional


def _env(name: str, default: str) -> str:
    val = os.environ.get(name)
    return val if val else default


def _normalize_base_url(base_url: str) -> str:
    base_url = base_url.strip()
    if base_url.endswith("/"):
        base_url = base_url[:-1]
    # Accept either http://host:port or http://host:port/v1
    if not base_url.endswith("/v1"):
        base_url = base_url + "/v1"
    return base_url


def chat_completion(
    *,
    base_url: str,
    api_key: str,
    model: str,
    messages: List[Dict[str, str]],
    timeout_s: int = 120,
) -> str:
    url = _normalize_base_url(base_url) + "/chat/completions"
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "stream": False,
    }
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url=url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        raise RuntimeError(
            f"HTTP {e.code} calling {url}: {body.strip() or e.reason}"
        ) from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error calling {url}: {e.reason}") from e

    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Non-JSON response from server: {raw[:500]}") from e

    # OpenAI-compatible format: choices[0].message.content
    try:
        choices = obj["choices"]
        if not choices:
            raise KeyError("choices is empty")
        msg = choices[0]["message"]
        content = msg.get("content")
        if content is None:
            raise KeyError("message.content missing")
        return str(content)
    except Exception as e:
        raise RuntimeError(f"Unexpected response schema: {obj}") from e


def _print_help() -> None:
    print(
        "Commands:\n"
        "  /help         Show this help\n"
        "  /reset        Clear conversation\n"
        "  /system TEXT  Set system prompt (replaces existing)\n"
        "  /exit         Quit\n"
    )


def main(argv: List[str]) -> int:
    base_url = _env("OPENAI_BASE_URL", "http://localhost:4141")
    api_key = _env("OPENAI_API_KEY", "dummy")
    model = _env("OPENAI_MODEL", "gpt-4")

    system_prompt: Optional[str] = "You are a helpful assistant."
    messages: List[Dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    print("CLI Chatbot (OpenAI-compatible)")
    print(f"Base URL: {_normalize_base_url(base_url)}")
    print(f"Model: {model}")
    print("Type /help for commands.\n")

    while True:
        try:
            user_in = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye")
            return 0

        if not user_in:
            continue

        if user_in in {"/exit", "/quit"}:
            print("bye")
            return 0
        if user_in == "/help":
            _print_help()
            continue
        if user_in == "/reset":
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            print("(conversation reset)\n")
            continue
        if user_in.startswith("/system"):
            text = user_in[len("/system") :].strip()
            if not text:
                print("usage: /system TEXT\n")
                continue
            system_prompt = text
            messages = [{"role": "system", "content": system_prompt}]
            print("(system prompt set)\n")
            continue

        messages.append({"role": "user", "content": user_in})
        t0 = time.time()
        try:
            out = chat_completion(
                base_url=base_url,
                api_key=api_key,
                model=model,
                messages=messages,
            )
        except Exception as e:
            print(f"error: {e}\n")
            # keep the user message so retries keep context
            continue
        dt_ms = int((time.time() - t0) * 1000)

        messages.append({"role": "assistant", "content": out})
        print(f"bot> {out}\n({dt_ms} ms)\n")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

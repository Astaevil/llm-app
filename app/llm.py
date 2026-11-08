import os
from typing import Iterator

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ.get("OPENAI_BASE_URL"),
)
MODEL = os.environ.get("MODEL_NAME", "deepseek-chat")


def chat_messages(messages: list[dict], temperature: float = 0.7) -> dict:
    """最底层：传什么 messages 就发什么，返回统一结构。"""
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
    )
    return {
        "answer": resp.choices[0].message.content,
        "tokens": resp.usage.total_tokens if resp.usage else None,
    }


def chat_once(question: str, temperature: float = 0.7) -> dict:
    return chat_messages([{"role": "user", "content": question}], temperature)


def chat_stream(question: str, temperature: float = 0.7) -> Iterator[str]:
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
        temperature=temperature,
        stream=True,
    )
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        if delta and delta.content:
            yield delta.content


def chat_stream_messages(messages: list[dict], temperature: float = 0.7) -> Iterator[str]:
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        stream=True,
    )
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        if delta and delta.content:
            yield delta.content

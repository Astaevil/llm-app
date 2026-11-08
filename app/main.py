from collections import defaultdict

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.llm import chat_once, chat_stream, chat_messages, chat_stream_messages

app = FastAPI(title="LLM App")

SYSTEM_PROMPT = "你是一个简洁的助手，请用中文回答。"
MAX_HISTORY_MESSAGES = 20

conversations: dict[str, list[dict]] = defaultdict(list)


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    temperature: float = Field(0.7, ge=0.0, le=2.0)


class MultiChatRequest(ChatRequest):
    conversation_id: str = Field(default="default", max_length=64)


def sse(piece: str) -> str:
    """把一段文本包成合法的 SSE 帧。内容里的换行必须拆成多个 data: 行。"""
    lines = piece.split("\n")
    return "".join(f"data: {line}\n" for line in lines) + "\n"


@app.get("/health")
def health():
    return {"status": "ok", "llm": "deepseek"}


@app.post("/chat")
def chat(req: ChatRequest):
    try:
        return chat_once(req.question, req.temperature)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"模型调用失败：{e}")


@app.post("/chat/stream")
def chat_stream_api(req: ChatRequest):
    def gen():
        try:
            for piece in chat_stream(req.question, req.temperature):
                yield sse(piece)
        except Exception as e:
            yield sse(f"[ERROR] {e}")
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.post("/chat/multi")
def chat_multi(req: MultiChatRequest):
    history = conversations[req.conversation_id]
    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + history
        + [{"role": "user", "content": req.question}]
    )
    try:
        result = chat_messages(messages, req.temperature)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"模型调用失败：{e}")

    history.append({"role": "user", "content": req.question})
    history.append({"role": "assistant", "content": result["answer"]})
    if len(history) > MAX_HISTORY_MESSAGES:
        del history[: len(history) - MAX_HISTORY_MESSAGES]

    return {
        **result,
        "conversation_id": req.conversation_id,
        "turns": len(history) // 2,
    }


@app.post("/chat/multi/stream")
def chat_multi_stream(req: MultiChatRequest):
    history = conversations[req.conversation_id]
    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + history
        + [{"role": "user", "content": req.question}]
    )

    def gen():
        collected = []
        try:
            for piece in chat_stream_messages(messages, req.temperature):
                collected.append(piece)
                yield sse(piece)
        except Exception as e:
            yield sse(f"[ERROR] {e}")
        history.append({"role": "user", "content": req.question})
        history.append({"role": "assistant", "content": "".join(collected)})
        if len(history) > MAX_HISTORY_MESSAGES:
            del history[: len(history) - MAX_HISTORY_MESSAGES]
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/history/{conversation_id}")
def get_history(conversation_id: str):
    return {"conversation_id": conversation_id, "messages": conversations[conversation_id]}


@app.delete("/history/{conversation_id}")
def clear_history(conversation_id: str):
    conversations.pop(conversation_id, None)
    return {"conversation_id": conversation_id, "cleared": True}




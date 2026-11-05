from fastapi import FastAPI

app = FastAPI(title="LLM App")

@app.get("/health")
def health():
    return {"status":"ok"}

from fastapi import FastAPI, HTTPException
from app_agent.schemas import ChatRequest, ChatResponse, Suggestion
from app_agent.tools import fpl_bootstrap, optimize_squad
from app_agent.openai_agent import OpenAIAgent

app = FastAPI(title="FPL Agent POC")
agent = OpenAIAgent()

@app.get("/health")
async def health():
    return {"ok": True}

@app.get("/tools/fpl_bootstrap")
async def tool_fpl_bootstrap():
    try:
        data = await fpl_bootstrap()
        return {"ok": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimize", response_model=Suggestion)
async def optimize():
    data = await fpl_bootstrap()
    suggestion = await optimize_squad(data.get("players", []))
    return Suggestion(**suggestion)

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    data = await fpl_bootstrap()
    suggestion = await optimize_squad(data.get("players", []))
    reply = await agent.reply(req.message, suggestion["captain"], suggestion["rationale"])
    return ChatResponse(reply=reply, suggestion=Suggestion(**suggestion))
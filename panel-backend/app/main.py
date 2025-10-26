from fastapi import FastAPI
from app.routers import websites, nodes, contracts

app = FastAPI(title="Stralix Panel", version="0.1.0")

app.include_router(websites.router, prefix="/api/panel")
app.include_router(nodes.router, prefix="/api/panel")
app.include_router(contracts.router, prefix="/api/panel")

@app.get("/health")
async def health():
    return {"status":"ok"}

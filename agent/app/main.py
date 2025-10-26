import ssl
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Stralix Agent", version="0.1.0")

class VhostIn(BaseModel):
    domain: str
    engine: str # nginx|apache
    root: str

@app.get("/health")
async def health():
    return {"status":"ok"}

@app.post("/v1/vhosts")
async def create_vhost(v: VhostIn):
    # TODO: write template to sites-available, run configtest, enable, reload
    return {"id": v.domain, "status":"applied"}

from pydantic import BaseModel

class AgentCreateVhostRequest(BaseModel):
    domain: str
    engine: str
    root: str

class AgentCreateVhostResponse(BaseModel):
    id: str
    status: str

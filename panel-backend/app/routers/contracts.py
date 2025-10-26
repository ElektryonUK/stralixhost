from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/contracts", tags=["contracts"]) 

class CreateVhostRequest(BaseModel):
    domain: str
    engine: str # nginx|apache
    root: str

class CreateVhostResponse(BaseModel):
    id: str
    status: str

@router.get("/openapi/panel-agent")
async def openapi_stub():
    return {
      "v1": {
        "agent": {
          "POST /v1/vhosts": {
            "request": CreateVhostRequest.model_json_schema(),
            "response": CreateVhostResponse.model_json_schema()
          }
        }
      }
    }

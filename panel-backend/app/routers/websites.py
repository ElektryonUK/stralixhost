from fastapi import APIRouter

router = APIRouter(prefix="/websites", tags=["websites"]) 

@router.post("/provision")
async def provision_website(payload: dict):
    # TODO: validate payload, enqueue task, call agent client
    return {"status":"queued", "payload": payload}

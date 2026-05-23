from fastapi import APIRouter, Request, Header, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.api.v1.dependencies import get_db
from app.repositories.deploy_repo import DeploymentRepository
from app.models.deployment import DeploymentStatus

router = APIRouter()

@router.post("/webhook")
async def github_webhook(
    request: Request, 
    x_hub_signature_256: str = Header(None), 
    db: Session = Depends(get_db)
):
    # In production, we MUST verify the x-hub-signature-256 using a secret
    payload = await request.json()
    
    # Example payload: { "action": "completed", "workflow_run": { "id": 123, "conclusion": "success" } }
    action = payload.get("action")
    run_id = payload.get("workflow_run", {}).get("id")
    conclusion = payload.get("workflow_run", {}).get("conclusion")
    
    if action == "completed" and run_id:
        repo = DeploymentRepository(db)
        # Find deployment by external_job_id
        # (We would add a specific method to the repo for this)
        # For now, we simulate the update
        status_map = {"success": DeploymentStatus.SUCCESS, "failure": DeploymentStatus.FAILED}
        final_status = status_map.get(conclusion, DeploymentStatus.FAILED)
        
        # Logic to find deployment by external_id and update it
        # repo.update_by_external_id(run_id, final_status, log=f"Webhook: {conclusion}")
        
    return {"status": "accepted"}

import time
import random
import asyncio
from app.worker.celery_app import celery_app
from app.repositories.deploy_repo import DeploymentRepository
from app.models.deployment import DeploymentStatus
from app.core.config import settings
from app.services.pipeline_service import GitHubService
from app.services.k8s_service import K8sService
from app.schemas.pipeline import GitHubPipelineConfig
from app.core.websocket_manager import manager # Import manager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database setup for worker
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def notify_deployment_update(deployment_id: int, status: str, log: str):
    """Helper to push updates to WebSockets"""
    await manager.broadcast_to_deployment(deployment_id, {
        "status": status,
        "log": log
    })

async def run_github_deployment(deployment_id: int, app_id: int, env_id: int, commit_hash: str):
    db = SessionLocal()
    try:
        k8s = K8sService()
        repo = DeploymentRepository(db)
        
        # 1. Fetch Application/Env config (In real app, fetch from DB)
        gh_config = GitHubPipelineConfig(
            workflow_id="deploy.yml",
            github_token="ghp_simulated_token",
            owner="devops-org",
            repo="main-app"
        )
        gh_service = GitHubService(gh_config)
        
        # 2. Trigger GitHub Action
        log_msg = "Triggering GitHub Action..."
        repo.update_status(deployment_id, DeploymentStatus.RUNNING, log=log_msg)
        await notify_deployment_update(deployment_id, "running", log_msg)
        
        gh_response = await gh_service.trigger_workflow(ref=commit_hash)
        
        log_msg = f"Workflow triggered. Run ID: {gh_response.run_id}"
        repo.update_status(
            deployment_id, 
            DeploymentStatus.RUNNING, 
            log=log_msg,
            external_id=str(gh_response.run_id)
        )
        await notify_deployment_update(deployment_id, "running", log_msg)
        
        # 3. Poll for completion
        while True:
            status = await gh_service.get_run_status(gh_response.run_id)
            if status: # --- K8S INTEGRATION START ---
                log_msg = "CI Pipeline Success. Updating Kubernetes Deployment..."
                await notify_deployment_update(deployment_id, "running", log_msg)
                
                # In production, the image tag would come from the GitHub Action output
                image_tag = f"my-reg/app:{commit_hash[:7]}"
                await k8s.deploy_image(
                    namespace="production", 
                    deployment_name="main-app", 
                    image=image_tag
                )
                
                log_msg = "K8s Deployment updated successfully!"
                repo.update_status(deployment_id, DeploymentStatus.SUCCESS, log=log_msg)
                await notify_deployment_update(deployment_id, "success", log_msg)
                # --- K8S INTEGRATION END ---og_msg)
                await notify_deployment_update(deployment_id, "success", log_msg)
                break
            elif status == "cancelled":
                log_msg = "GitHub Action was cancelled."
                repo.update_status(deployment_id, DeploymentStatus.CANCELLED, log=log_msg)
                await notify_deployment_update(deployment_id, "cancelled", log_msg)
                break
            
            time.sleep(30) # Poll every 30s
            
    except Exception as e:
        log_msg = f"GitHub Integration Error: {str(e)}"
        repo.update_status(deployment_id, DeploymentStatus.FAILED, log=log_msg)
        await notify_deployment_update(deployment_id, "failed", log_msg)
    finally:
        db.close()

@celery_app.task(bind=True, name="tasks.execute_deployment")
def execute_deployment_task(self, deployment_id: int, app_id: int, env_id: int, commit_hash: str):
    asyncio.run(run_github_deployment(deployment_id, app_id, env_id, commit_hash))

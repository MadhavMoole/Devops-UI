import httpx
from fastapi import HTTPException, status
from app.core.config import settings
from app.schemas.pipeline import GitHubPipelineConfig, GitHubWorkflowResponse

class GitHubService:
    def __init__(self, config: GitHubPipelineConfig):
        self.config = config
        self.base_url = f"https://api.github.com/repos/{config.owner}/{config.repo}"
        self.headers = {
            "Authorization": f"token {config.github_token}",
            "Accept": "application/vnd.github+json",
        }

    async def trigger_workflow(self, ref: str) -> GitHubWorkflowResponse:
        """
        Triggers a GitHub Action workflow dispatch event.
        """
        url = f"{self.base_url}/actions/workflows/{self.config.workflow_id}/dispatches"
        data = {"ref": ref}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=data)
            
            if response.status_code == 204:
                # GitHub returns 204 No Content on success for dispatch
                # We need to fetch the latest run to get the run_id
                return await self._get_latest_run_id()
            
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"GitHub API Error: {response.text}"
            )

    async def _get_latest_run_id(self) -> GitHubWorkflowResponse:
        url = f"{self.base_url}/actions/workflows/{self.config.workflow_id}/runs"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            data = response.json()
            latest_run = data["workflow_runs"][0]
            return GitHubWorkflowResponse(
                run_id=latest_run["id"],
                status=latest_run["status"]
            )

    async def get_run_status(self, run_id: int) -> str:
        url = f"{self.base_url}/actions/runs/{run_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            return response.json().get("status", "unknown")

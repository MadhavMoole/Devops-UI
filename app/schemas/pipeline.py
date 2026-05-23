from pydantic import BaseModel, Field
from typing import Optional

class GitHubPipelineConfig(BaseModel):
    workflow_id: str = Field(..., description="The ID or filename of the GitHub workflow (e.g., 'deploy.yml')")
    github_token: str = Field(..., description="Personal Access Token or GitHub App Token")
    owner: str = Field(..., description="GitHub organization or user owner")
    repo: str = Field(..., description="Repository name")

class GitHubWorkflowResponse(BaseModel):
    run_id: int
    status: str

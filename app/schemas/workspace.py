from pydantic import BaseModel, Field


class WorkspaceCreate(BaseModel):
    """
    Request schema for creating a new workspace.
    """

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Workspace name"
    )

    description: str = Field(
        default="",
        max_length=500,
        description="Workspace description"
    )

    industry: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Business industry"
    )

    objective: str = Field(
        ...,
        min_length=5,
        max_length=300,
        description="Business objective"
    )


class WorkspaceResponse(BaseModel):
    """
    Response schema returned after a workspace
    has been created successfully.
    """

    workspace_id: str
    name: str
    description: str
    industry: str
    objective: str
    status: str
    version: str


class WorkspaceMetadata(BaseModel):
    """
    Complete metadata stored inside metadata.json
    """

    workspace_id: str
    name: str
    description: str
    industry: str
    objective: str

    status: str
    version: str

    created_at: str
    last_modified: str
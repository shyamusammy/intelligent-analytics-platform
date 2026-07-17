from app.repositories.profiling_repository import ProfilingRepository
from app.core.exceptions import ProfilingArtifactNotFoundError

repository = ProfilingRepository()

try:
    profile = repository.load("ws_999")  # Workspace that doesn't exist
    print(profile.model_dump())

except ProfilingArtifactNotFoundError as e:
    print("✅ Custom exception works!")
    print(e)
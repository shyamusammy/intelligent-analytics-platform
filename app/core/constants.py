"""
Application-wide constants.

This module contains only values that are reused
across multiple modules in the application.
"""


# ==========================================================
# Workspace
# ==========================================================

class WorkspaceFolders:
    ROOT = "workspaces"

    DATASETS = "datasets"

    PROCESSED = "processed"

    ARTIFACTS = "artifacts"

    DASHBOARD = "dashboard"

    REPORTS = "reports"

    EXPORTS = "exports"

    LOGS = "logs"


# ==========================================================
# Artifact Folders
# ==========================================================

class ArtifactFolders:
    PROFILING = "profiling"

    STATISTICS = "statistics"

    MODELS = "models"

    FORECASTS = "forecasts"

    EVALUATION = "evaluation"

    AI = "ai"


# ==========================================================
# Dataset
# ==========================================================

class DatasetFolders:
    ORIGINAL = "original"


class DatasetFiles:
    METADATA = "metadata.json"


# ==========================================================
# Dataset Validation
# ==========================================================

class DatasetValidation:
    SUPPORTED_EXTENSIONS = {
        ".csv",
        ".xlsx",
        ".xls",
    }

    MAX_UPLOAD_SIZE_MB = 100


# ==========================================================
# Status Values
# ==========================================================

class WorkspaceStatus:
    ACTIVE = "active"

    ARCHIVED = "archived"


class DatasetStatus:
    UPLOADED = "uploaded"

    VALIDATED = "validated"

    PROFILED = "profiled"

    PROCESSED = "processed"

    READY = "ready"


# ==========================================================
# Version
# ==========================================================

APP_VERSION = "1.0"
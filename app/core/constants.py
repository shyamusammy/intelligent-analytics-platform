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


class ETLConstants:
    """
    Configuration values used throughout the ETL Engine.
    """

    # --------------------------------------------------
    # Datatype Inference
    # --------------------------------------------------

    DATETIME_DETECTION_THRESHOLD = 0.95

    CATEGORICAL_UNIQUE_RATIO = 0.05

    MAX_CATEGORICAL_UNIQUE_VALUES = 50


# ==========================================================
# ETL Artifacts
# ==========================================================

class ETLArtifacts:

    PROFILING_FOLDER = "profiling"

    PROFILE_FILE = "profile.json"


# ==========================================================
# ML Constants
# ==========================================================

class MLConstants:
    MINIMUM_ROWS = 30
    MINIMUM_FEATURE_COLUMNS = 2

    MAX_CLASSIFICATION_UNIQUE_VALUES = 20
    CLASSIFICATION_UNIQUE_RATIO = 0.05

    TEST_SIZE = 0.2
    RANDOM_STATE = 42

# ==========================================================
# Version
# ==========================================================

APP_VERSION = "1.0"
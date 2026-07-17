"""
Application-specific exceptions.

This module defines the domain exceptions used throughout the
Intelligent Analytics Platform.

These exceptions provide meaningful errors for the service layer
and allow the API layer to translate them into appropriate HTTP
responses.
"""


# ==========================================================
# Base Exception
# ==========================================================

class AnalyticsPlatformError(Exception):
    """
    Base exception for all application-specific errors.
    """

    pass


# ==========================================================
# Workspace Exceptions
# ==========================================================

class WorkspaceError(AnalyticsPlatformError):
    """
    Base class for workspace-related exceptions.
    """

    pass


class WorkspaceNotFoundError(WorkspaceError):
    """
    Raised when the requested workspace does not exist.
    """

    def __init__(self, workspace_id: str):
        super().__init__(
            f"Workspace '{workspace_id}' was not found."
        )


class WorkspaceAlreadyExistsError(WorkspaceError):
    """
    Raised when attempting to create an existing workspace.
    """

    def __init__(self, workspace_id: str):
        super().__init__(
            f"Workspace '{workspace_id}' already exists."
        )


# ==========================================================
# Dataset Exceptions
# ==========================================================

class DatasetError(AnalyticsPlatformError):
    """
    Base class for dataset-related exceptions.
    """

    pass


class DatasetNotFoundError(DatasetError):
    """
    Raised when a dataset cannot be located.
    """

    def __init__(
        self,
        dataset_id: str,
    ):
        super().__init__(
            f"Dataset '{dataset_id}' was not found."
        )


class DatasetAlreadyExistsError(DatasetError):
    """
    Raised when attempting to create a duplicate dataset.
    """

    def __init__(
        self,
        dataset_id: str,
    ):
        super().__init__(
            f"Dataset '{dataset_id}' already exists."
        )


class DatasetMetadataNotFoundError(DatasetError):
    """
    Raised when metadata.json is missing.
    """

    def __init__(
        self,
        dataset_id: str,
    ):
        super().__init__(
            f"Metadata for dataset '{dataset_id}' was not found."
        )


class OriginalDatasetNotFoundError(DatasetError):
    """
    Raised when the original uploaded file is missing.
    """

    def __init__(
        self,
        dataset_id: str,
    ):
        super().__init__(
            f"Original file for dataset '{dataset_id}' was not found."
        )


class UnsupportedDatasetFormatError(DatasetError):
    """
    Raised when no reader exists for the dataset type.
    """

    def __init__(
        self,
        extension: str,
    ):
        super().__init__(
            f"Unsupported dataset format '{extension}'."
        )


class DatasetValidationError(DatasetError):
    """
    Raised when dataset validation fails.
    """

    pass


# ==========================================================
# ETL Exceptions
# ==========================================================

class ETLError(AnalyticsPlatformError):
    """
    Base class for ETL-related exceptions.
    """

    pass


class DatasetLoadError(ETLError):
    """
    Raised when a dataset cannot be loaded into memory.
    """

    def __init__(
        self,
        dataset_id: str,
    ):
        super().__init__(
            f"Failed to load dataset '{dataset_id}'."
        )


class SchemaDetectionError(ETLError):
    """
    Raised when schema detection fails.
    """

    pass


class ProfilingError(ETLError):
    """
    Raised when dataset profiling fails.
    """

    pass


class QualityAnalysisError(ETLError):
    """
    Raised when data quality analysis fails.
    """

    pass


class ProfilingArtifactNotFoundError(ETLError):
    """
    Raised when the ETL profiling artifact is not found.
    """
    pass
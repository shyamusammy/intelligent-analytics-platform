from enum import Enum


class MLTaskType(str, Enum):
    CLASSIFICATION = "classification"
    REGRESSION = "regression"

class MLEstimator(str, Enum):
    LINEAR_REGRESSION = "linear_regression"
    RANDOM_FOREST_REGRESSOR = "random_forest_regressor"

    LOGISTIC_REGRESSION = "logistic_regression"
    RANDOM_FOREST_CLASSIFIER = "random_forest_classifier"


class CorrelationMethod(str, Enum):
    PEARSON = "pearson"
    SPEARMAN = "spearman"
    KENDALL = "kendall"

class CorrelationStrength(str, Enum):
    VERY_WEAK = "very_weak"
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    VERY_STRONG = "very_strong"


class CorrelationDirection(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NONE = "none"


class InsightSeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class InsightCategory(str, Enum):
    DATASET = "dataset"
    STATISTICS = "statistics"
    KPI = "kpi"
    CORRELATION = "correlation"
    TREND = "trend"
    SEGMENTATION = "segmentation"


class TrendDirection(str, Enum):
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
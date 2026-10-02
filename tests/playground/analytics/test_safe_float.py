"""
Test suite for StatisticsService._safe_float().
"""

import math

from app.services.analytics.statistics_service import StatisticsService


def test_safe_float():
    service = StatisticsService()

    test_cases = [
        # normal integers
        (10, 10.0),

        # normal floats
        (10.5, 10.5),

        # numeric string
        ("10.5", 10.5),

        # None
        (None, None),

        # NaN
        (float("nan"), None),

        # positive infinity
        (float("inf"), None),

        # negative infinity
        (float("-inf"), None),
    ]

    for value, expected in test_cases:
        result = service._safe_float(value)

        if expected is None:
            assert result is None
        else:
            assert math.isclose(result, expected)


if __name__ == "__main__":
    test_safe_float()
    print("✓ _safe_float() test passed")
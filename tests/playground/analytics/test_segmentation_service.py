import pandas as pd

from app.services.analytics.segmentation_service import (
    SegmentationService,
)


def main() -> None:

    dataframe = pd.DataFrame(
        {
            "Region": (
                ["North"] * 40
                + ["South"] * 30
                + ["East"] * 20
                + ["West"] * 10
            ),
            "Department": (
                ["Sales"] * 50
                + ["HR"] * 25
                + ["Finance"] * 25
            ),
            "Revenue": list(range(100, 200)),
            "Profit": list(range(50, 150)),
        }
    )

    service = SegmentationService()

    result = service.run(
        dataframe,
    )

    print("=" * 70)
    print("SEGMENTATION RESULT")
    print("=" * 70)

    print()

    for segment in result.segments:

        print(
            segment.model_dump(
                mode="json",
            )
        )


if __name__ == "__main__":
    main()
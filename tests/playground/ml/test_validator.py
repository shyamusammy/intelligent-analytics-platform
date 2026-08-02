from app.services.ml.validator import MLValidator
from pandas import DataFrame


df = DataFrame({
    "Age": [20, 20, 30],
    "Salary": [100, 100, 200],
    "Revenue": [10, 10, 20]
})

validator = MLValidator()

result = validator.validate(
    dataframe=df,
    target_column="Revenue"
)

print(result.model_dump())
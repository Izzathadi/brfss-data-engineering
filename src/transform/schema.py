import pandera.pandas as pa
from pandera.pandas import Column, DataFrameSchema
from pandera import Check

diabetes_schema = DataFrameSchema({
    "Diabetes_01": Column(int, Check.isin([0, 1])),
    "HighBP": Column(int, Check.isin([0, 1])),
    "HighChol": Column(int, Check.isin([0, 1])),
    "BMI": Column(
        float,
        checks=[
            Check(lambda x: x.mean() >= -0.1 and x.mean() <= 0.1, error="Mean BMI not approx 0"),
            Check(lambda x: x.std() >= 0.9 and x.std() <= 1.1, error="Std BMI not approx 1"),
            Check.in_range(-5, 5)
        ]
    ),
    "Smoker": Column(int, Check.isin([0, 1])),
    "PhysActivity": Column(int, Check.isin([0, 1])),
    "Fruits": Column(int, Check.isin([0, 1])),
    "Veggies": Column(int, Check.isin([0, 1])),
    "DiffWalk": Column(int, Check.isin([0, 1])),
    "Sex": Column(int, Check.isin([0, 1])),
    "Age": Column(int, Check.ge(0))
})

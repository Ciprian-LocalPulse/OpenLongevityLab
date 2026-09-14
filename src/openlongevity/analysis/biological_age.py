"""Small, transparent regression baseline for synthetic biological-age data."""

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class RegressionMetrics:
    mae: float
    rmse: float
    r_squared: float


class BiologicalAgeModel:
    """Ordinary least-squares baseline; prediction is not clinical validation."""

    def __init__(self) -> None:
        self.means: list[float] = []
        self.scales: list[float] = []
        self.coefficients: list[float] = []
        self.intercept = 0.0

    def fit(self, features: list[list[float]], targets: list[float]) -> "BiologicalAgeModel":
        if not features or len(features) != len(targets):
            raise ValueError("features and targets must be non-empty and aligned")
        width = len(features[0])
        if width == 0 or any(len(row) != width for row in features):
            raise ValueError("all feature rows must have the same non-zero width")
        self.means = [sum(row[j] for row in features) / len(features) for j in range(width)]
        self.scales = [
            sqrt(sum((row[j] - self.means[j]) ** 2 for row in features) / len(features)) or 1.0
            for j in range(width)
        ]
        normalized = [
            [(row[j] - self.means[j]) / self.scales[j] for j in range(width)] for row in features
        ]
        design = [[1.0, *row] for row in normalized]
        coefficients = _solve_normal_equations(design, targets)
        self.intercept, *self.coefficients = coefficients
        return self

    def predict(self, features: list[list[float]]) -> list[float]:
        if not self.coefficients:
            raise RuntimeError("fit the model before prediction")
        if any(len(row) != len(self.coefficients) for row in features):
            raise ValueError("feature width does not match fitted model")
        return [
            self.intercept
            + sum(
                coef * ((value - mean) / scale)
                for coef, value, mean, scale in zip(self.coefficients, row, self.means, self.scales)
            )
            for row in features
        ]

    def evaluate(self, features: list[list[float]], targets: list[float]) -> RegressionMetrics:
        predictions = self.predict(features)
        if len(predictions) != len(targets) or not targets:
            raise ValueError("targets must be non-empty and aligned")
        residuals = [actual - predicted for actual, predicted in zip(targets, predictions)]
        mae = sum(abs(value) for value in residuals) / len(residuals)
        rmse = sqrt(sum(value * value for value in residuals) / len(residuals))
        mean = sum(targets) / len(targets)
        total = sum((value - mean) ** 2 for value in targets)
        r_squared = 1.0 - sum(value * value for value in residuals) / total if total else 0.0
        return RegressionMetrics(round(mae, 6), round(rmse, 6), round(r_squared, 6))


def _solve_normal_equations(design: list[list[float]], targets: list[float]) -> list[float]:
    width = len(design[0])
    matrix = [[sum(row[i] * row[j] for row in design) for j in range(width)] for i in range(width)]
    vector = [sum(row[i] * target for row, target in zip(design, targets)) for i in range(width)]
    for pivot in range(width):
        best = max(range(pivot, width), key=lambda index: abs(matrix[index][pivot]))
        if abs(matrix[best][pivot]) < 1e-12:
            raise ValueError("feature matrix is singular")
        matrix[pivot], matrix[best] = matrix[best], matrix[pivot]
        vector[pivot], vector[best] = vector[best], vector[pivot]
        scale = matrix[pivot][pivot]
        matrix[pivot] = [value / scale for value in matrix[pivot]]
        vector[pivot] /= scale
        for row in range(width):
            if row == pivot:
                continue
            factor = matrix[row][pivot]
            matrix[row] = [left - factor * right for left, right in zip(matrix[row], matrix[pivot])]
            vector[row] -= factor * vector[pivot]
    return vector

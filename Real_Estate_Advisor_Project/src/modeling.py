import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, mean_squared_error, r2_score

# ---------------- Regression ---------------- #

def future_price_fixed_rate(current_price, rate=0.08, years=5):
    return current_price * ((1 + rate) ** years)

def future_price_by_location(df, rate_map, years=5):
    df["Future_Price"] = df.apply(
        lambda row: row["Price_in_Lakhs"] * ((1 + rate_map.get((row["City"], row["Property_Type"]), 0.08)) ** years),
        axis=1
    )
    return df

def train_regression_model(X_train, y_train):
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    return model

# ---------------- Classification ---------------- #

def classify_good_investment(df):
    # Ensure Price_per_SqFt exists
    if "Price_per_SqFt" not in df.columns:
        df["Price_per_SqFt"] = (df["Price_in_Lakhs"] * 100000) / df["Size_in_SqFt"].replace(0, np.nan)

    # Compute medians
    median_price = df["Price_in_Lakhs"].median()
    median_sqft = df["Price_per_SqFt"].median()

    # Multi-factor score
    df["Investment_Score"] = (
        (df["BHK"] >= 3).astype(int) +
        (df["RERA_Compliant"] == 1).astype(int) +
        (df["Availability_Status"] == "Ready-to-move").astype(int)
    )

    # Final condition: combine all rules
    df["Good_Investment"] = np.where(
        (df["Price_in_Lakhs"] <= median_price) &
        (df["Price_per_SqFt"] <= median_sqft) |
        (df["Investment_Score"] >= 2),
        1,
        0
    )

    return df


def train_classification_model(X_train, y_train):
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

# ---------------- Evaluation ---------------- #

from sklearn.metrics import mean_absolute_error

def evaluate_regression(y_true, y_pred):
    """Return RMSE, MAE, R² for regression model."""
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return rmse, mae, r2


def evaluate_classification(y_true, y_pred):
    """Return Accuracy, F1-score, Confusion Matrix for classification model."""
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average="weighted")
    cm = confusion_matrix(y_true, y_pred)
    return acc, f1, cm

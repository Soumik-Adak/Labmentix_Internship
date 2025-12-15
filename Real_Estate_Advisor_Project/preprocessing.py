import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("Data/india_housing_prices.csv")


# ---------------- Stage 1: Cleaning & Dtype Enforcement ---------------- #

def exact_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    dtype_map = {
        "ID": "int64",
        "City": "object",
        "Property_Type": "object",
        "BHK": "int64",
        "Size_in_SqFt": "int64",
        "Year_Built": "int64",
        "Floor_No": "int64",
        "Total_Floors": "int64",
        "Age_of_Property": "int64",
        "Nearby_Schools": "int64",
        "Nearby_Hospitals": "int64"
    }

    for col, dtype in dtype_map.items():
        if col in df.columns:
            if "int" in dtype:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(dtype)
            else:
                df[col] = df[col].astype(dtype)
    return df


# ---------------- Stage 2: ML‑Ready Encoding ---------------- #

def preprocess_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Remove duplicates
    df = df.drop_duplicates()

    # 2. Handle missing values
    num_cols = df.select_dtypes(include=np.number).columns
    cat_cols = df.select_dtypes(include="object").columns
    df[num_cols] = SimpleImputer(strategy="median").fit_transform(df[num_cols])
    df[cat_cols] = SimpleImputer(strategy="most_frequent").fit_transform(df[cat_cols])

    # 3. Feature engineering
    df["Price_per_SqFt"] = (df["Price_in_Lakhs"] * 100000) / df["Size_in_SqFt"]
    #df["Age_of_Property"] = 2025 - df["Year_Built"]
    df["School_Density_Score"] = df.groupby("City")["Nearby_Schools"].transform(lambda x: x / x.max())

    # 4. Encode categorical
    for col in ["City", "Property_Type"]:
        df[col] = LabelEncoder().fit_transform(df[col].astype(str))

    # 5. Scale numerical
    df[num_cols] = StandardScaler().fit_transform(df[num_cols])

    # 6. Binary label
    median_price = df["Price_per_SqFt"].median()
    df["Good_Investment"] = np.where(df["Price_per_SqFt"] <= median_price, 1, 0)

    return df


import streamlit as st
import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt


from src.preprocessing import exact_dtypes, preprocess_pipeline
from src.eda import (
    plot_price_distribution,
    plot_size_distribution,
    plot_price_per_sqft_by_type,
    plot_outliers,
    plot_avg_price_sqft_by_state,
    plot_avg_price_by_city,
    plot_bhk_distribution_by_city,
    plot_price_trends_top_localities,
    plot_numeric_correlations,
    plot_hospitals_vs_price,
    plot_price_by_furnished_status,
    plot_price_sqft_by_facing,
    plot_owner_type_distribution,
    plot_availability_status_distribution,
    plot_parking_vs_price,
    plot_amenities_vs_price_sqft
)
from src.modeling import (
    future_price_fixed_rate,
    classify_good_investment,
    evaluate_classification,
    evaluate_regression, 
    train_classification_model,
    train_regression_model,
    train_test_split
)


# ---------------- Load Data ---------------- #
@st.cache_data
def load_data():
    df_clean = exact_dtypes(pd.read_csv("Data/india_housing_prices.csv"))
    df_ml = preprocess_pipeline(df_clean)
    return df_clean, df_ml

df_clean, df_ml = load_data()


# ---------------- Train/Test Split ---------------- #
# Classification dataset
X_class = df_ml[["BHK", "Size_in_SqFt", "Price_in_Lakhs", "City", "Property_Type"]]  # example features
y_class = df_ml["Good_Investment"]

X_train_class, X_test_class, y_train_class, y_test_class = train_test_split(
    X_class, y_class, test_size=0.2, random_state=42
)

classification_model = train_classification_model(X_train_class, y_train_class)

# Regression dataset
X_reg = df_ml[["BHK", "Size_in_SqFt", "City", "Property_Type"]]  # example features
y_reg = df_ml["Price_in_Lakhs"]

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

regression_model = train_regression_model(X_train_reg, y_train_reg)

# ---------------- Sidebar ---------------- #
st.sidebar.title("🏠 Real Estate Investment Advisor")
menu = st.sidebar.radio("Navigation", ["Data Inspection", "EDA", "Prediction"])


# ---------------- Data Inspection Section ---------------- #
if menu == "Data Inspection":
    st.title("🔍 Dataset Overview")

    with st.expander("Head of Dataset"):
        st.write(df_clean.head())

    with st.expander("Missing Values"):
        st.write(df_clean.isnull().sum())

    with st.expander("Duplicates"):
        st.write(df_clean.duplicated().sum())

    with st.expander("Unique Values"):
        st.write(df_clean.nunique())

    with st.expander("Data Types"):
        st.write(df_clean.dtypes)


# ---------------- EDA Section ---------------- #
if menu == "EDA":
    st.title("📊 Exploratory Data Analysis")
    st.write("Visual insights into property prices, sizes, and investment factors.")


    st.subheader("Distribution of Property Prices")
    fig = plot_price_distribution(df_clean)
    st.pyplot(fig)

    st.subheader("Distribution of Property Sizes")
    fig = plot_size_distribution(df_clean)
    st.pyplot(fig)

    st.subheader("Price per SqFt by Property Type")
    fig = plot_price_per_sqft_by_type(df_clean)
    st.pyplot(fig)

    st.subheader("Outlier Detection")
    fig = plot_outliers(df_clean)
    st.pyplot(fig)

    st.subheader("Average Price per SqFt by State")
    fig = plot_avg_price_sqft_by_state(df_clean)
    st.pyplot(fig)

    st.subheader("Average Property Price by City")
    fig = plot_avg_price_by_city(df_clean)
    st.pyplot(fig)

    st.subheader("BHK Distribution Across Cities")
    fig = plot_bhk_distribution_by_city(df_clean)
    st.pyplot(fig)

    st.subheader("Price Trends for Top 5 Most Expensive Localities")
    fig = plot_price_trends_top_localities(df_clean)
    st.pyplot(fig)

    st.subheader("Correlation Between Numeric Features")
    fig = plot_numeric_correlations(df_clean)
    st.pyplot(fig)

    st.subheader("Nearby Hospitals vs Price per SqFt")
    fig = plot_hospitals_vs_price(df_clean)
    st.pyplot(fig)

    st.subheader("Distribution of Furnished Status by Total Price")
    fig = plot_price_by_furnished_status(df_clean)
    st.pyplot(fig)

    st.subheader("Price per SqFt by Property Facing Direction")
    fig = plot_price_sqft_by_facing(df_clean)
    st.pyplot(fig)

    st.subheader("Properties Belong to Each Owner Type")
    fig = plot_owner_type_distribution(df_clean)
    st.pyplot(fig)

    st.subheader("Properties Available Under Availability Status")
    fig = plot_availability_status_distribution(df_clean)
    st.pyplot(fig)

    st.subheader("Parking Space vs Property Price")
    fig = plot_parking_vs_price(df_clean)
    st.pyplot(fig)

    st.subheader("Amenities vs Price per SqFt")
    fig = plot_amenities_vs_price_sqft(df_clean)
    st.pyplot(fig)


# ---------------- Prediction Section ---------------- #
elif menu == "Prediction":
    st.title("Investment Prediction")

    # ---------------- User Input Form ---------------- #
    city = st.selectbox("City", df_clean["City"].unique())
    property_type = st.selectbox("Property Type", df_clean["Property_Type"].unique())
    bhk = st.number_input("BHK", min_value=1, max_value=5, value=3)
    sqft = st.number_input("Size (SqFt)", min_value=200, max_value=10000, value=1200)
    price = st.number_input("Current Price (Lakhs)", min_value=10, max_value=1000, value=50)
    rera = st.selectbox("RERA Compliant", ["Yes", "No"])
    status = st.selectbox("Availability Status", ["Ready-to-move", "Under Construction"])

    # ---------------- Future Price Prediction ---------------- #
    future_price = future_price_fixed_rate(price, rate=0.08, years=5)
    st.metric("Estimated Price after 5 Years", f"{future_price:.2f} Lakhs")

    # ---------------- Good Investment Classification ---------------- #
    df_input = pd.DataFrame({
        "City": [city],
        "Property_Type": [property_type],
        "BHK": [bhk],
        "Size_in_SqFt": [sqft],
        "Price_in_Lakhs": [price],
        "RERA_Compliant": [1 if rera == "Yes" else 0],
        "Availability_Status": [status]
    })

    df_input = classify_good_investment(df_input)
    investment_label = "Good Investment" if df_input["Good_Investment"].iloc[0] == 1 else "Not Recommended Investment"
    st.subheader("Investment Decision")
    st.write(investment_label)

    # ---------------- Model Evaluation ---------------- #
    st.subheader("📈 Model Evaluation")

    # Classification evaluation
    y_pred_class = classification_model.predict(X_test_class)
    acc, f1, cm = evaluate_classification(y_test_class, y_pred_class)

    st.markdown("**Classification Metrics**")
    st.metric("Accuracy", f"{acc:.3f}")
    st.metric("F1-score", f"{f1:.3f}")

    fig, ax = plt.subplots(figsize=(6,4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_title("Confusion Matrix")
    st.pyplot(fig)

    # Regression evaluation
    y_pred_reg = regression_model.predict(X_test_reg)
    rmse, mae, r2 = evaluate_regression(y_test_reg, y_pred_reg)

    st.markdown("**Regression Metrics**")
    st.metric("RMSE", f"{rmse:.3f}")
    st.metric("MAE", f"{mae:.3f}")
    st.metric("R²", f"{r2:.3f}")

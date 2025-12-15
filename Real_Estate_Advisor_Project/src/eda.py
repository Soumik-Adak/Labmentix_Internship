import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px




# 1. Distribution of Property Prices
def plot_price_distribution(df):
    fig, ax = plt.subplots(figsize=(10,6))
    sns.histplot(df["Price_in_Lakhs"], bins=50, kde=True, ax=ax)
    ax.set_title("Distribution of Property Prices")
    ax.set_xlabel("Price (Lakhs)")
    ax.set_ylabel("Count")
    return fig

# 2. Distribution of Property Sizes
def plot_size_distribution(df):
    fig, ax = plt.subplots(figsize=(10,6))
    sns.histplot(df["Size_in_SqFt"], bins=50, kde=True, ax=ax)
    ax.set_title("Distribution of Property Sizes")
    ax.set_xlabel("Size (SqFt)")
    ax.set_ylabel("Count")
    return fig

# 3. Price per SqFt Variation by Property Type
def plot_price_per_sqft_by_type(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10,6))
    sns.boxplot(x="Property_Type", y="Price_per_SqFt", data=df, ax=ax)
    ax.set_title("Price per SqFt by Property Type")
    return fig

# 4. Relationship Between Property Size and Price
def plot_size_vs_price(df):
    fig, ax = plt.subplots(figsize=(10,6))
    sns.scatterplot(x="Size_in_SqFt", y="Price_in_Lakhs", data=df, alpha=0.6, ax=ax)
    ax.set_title("Relationship Between Property Size and Price")
    ax.set_xlabel("Size (SqFt)")
    ax.set_ylabel("Price (Lakhs)")
    corr = df["Size_in_SqFt"].corr(df["Price_in_Lakhs"])
    return fig, corr

# 5. Outlier Detection in Price per SqFt and Property Size
def plot_outliers(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(14,6))
    sns.boxplot(y=df["Price_per_SqFt"], ax=axes[0])
    axes[0].set_title("Outliers in Price per SqFt")
    sns.boxplot(y=df["Size_in_SqFt"], ax=axes[1])
    axes[1].set_title("Outliers in Property Size")
    return fig

# 6. Average Price per SqFt by State
def plot_avg_price_sqft_by_state(df: pd.DataFrame):
    state_price = df.groupby("State")["Price_per_SqFt"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(12,6))
    sns.barplot(x=state_price.index, y=state_price.values)
    ax.set_xticklabels(state_price.index, rotation=90)
    ax.set_title("Average Price per SqFt by State")
    ax.set_ylabel("Avg Price per SqFt")
    return fig

# 7. Average Property Price by City
def plot_avg_price_by_city(df: pd.DataFrame, top_n: int = 10):
    city_price = df.groupby("City")["Price_in_Lakhs"].mean().sort_values(ascending=False).head(top_n)
    fig, ax = plt.subplots(figsize=(12,6))
    sns.barplot(x=city_price.index, y=city_price.values)
    ax.set_xticklabels(city_price.index, rotation=90)
    ax.set_title(f"Top {top_n} Cities - Average Property Price")
    ax.set_ylabel("Avg Price (Lakhs)")
    return fig

# 8. Median Age of Properties by Locality
def plot_median_age_by_locality(df: pd.DataFrame, top_n: int = 10):
    locality_age = df.groupby("Locality")["Age_of_Property"].median().sort_values(ascending=False).head(top_n)
    fig, ax = plt.subplots(figsize=(12,6))
    sns.barplot(x=locality_age.index, y=locality_age.values)
    ax.set_xticklabels(locality_age.index, rotation=90)
    ax.set_title(f"Top {top_n} Localities - Median Age of Properties")
    ax.set_ylabel("Median Age (Years)")
    return fig

# 9. BHK Distribution Across Cities
def plot_bhk_distribution_by_city(df: pd.DataFrame, top_n: int = 10):
    top_cities = df["City"].value_counts().head(top_n).index
    df_top = df[df["City"].isin(top_cities)]
    fig, ax = plt.subplots(figsize=(12,6))
    sns.countplot(data=df_top, x="City", hue="BHK", palette="Set1", ax=ax)
    ax.set_title(f"BHK Distribution Across Top {top_n} Cities")
    ax.set_ylabel("Count")
    ax.set_xlabel("City")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    return fig

# 10. Price Trends for Top 5 Most Expensive Localities
def plot_price_trends_top_localities(df: pd.DataFrame, top_n: int = 5):
    top_localities = df.groupby("Locality")["Price_in_Lakhs"].mean().sort_values(ascending=False).head(top_n).index
    trend_data = df[df["Locality"].isin(top_localities)]
    fig, ax = plt.subplots(figsize=(12,6))
    sns.lineplot(x="Year_Built", y="Price_in_Lakhs", hue="Locality", data=trend_data)
    ax.set_title(f"Price Trends for Top {top_n} Most Expensive Localities")
    ax.set_ylabel("Price (Lakhs)")
    ax.set_xlabel("Year Built")
    return fig

# 11. Correlation Between Numeric Features
def plot_numeric_correlations(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(12,8))
    corr_matrix = df.select_dtypes(include="number").corr()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    ax.set_title("Correlation Between Numeric Features")
    return fig

# 12. Nearby Schools vs Price per SqFt
def plot_schools_vs_price(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10,6))
    sns.scatterplot(x="Nearby_Schools", y="Price_per_SqFt", data=df, alpha=0.6)
    ax.set_title("Nearby Schools vs Price per SqFt")
    ax.set_xlabel("Nearby Schools")
    ax.set_ylabel("Price per SqFt")
    return fig
# 13. Nearby Hospitals vs Price per SqFt
def plot_hospitals_vs_price(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10,6))
    sns.scatterplot(x="Nearby_Hospitals", y="Price_per_SqFt", data=df, alpha=0.6)
    ax.set_title("Nearby Hospitals vs Price per SqFt")
    ax.set_xlabel("Nearby Hospitals")
    ax.set_ylabel("Price per SqFt")
    
    #corr = df["Nearby_Hospitals"].corr(df["Price_per_SqFt"])
    return fig

# 14. Price by Furnished Status
def plot_price_by_furnished_status(df: pd.DataFrame):
    # Aggregate total price by furnished status
    status_price = df.groupby("Furnished_Status")["Price_in_Lakhs"].sum()

    # Plot Pie Chart
    fig, ax = plt.subplots(figsize=(5,5))
    ax.pie(
        status_price,
        labels=status_price.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=plt.cm.Set1.colors
    )
    ax.set_title("Distribution of Furnished Status According Price")
    return fig


# 15. Price per SqFt by Property Facing Direction
def plot_price_sqft_by_facing(df: pd.DataFrame):
    # Aggregate average price per sqft by facing direction
    facing_avg = df.groupby("Facing")["Price_per_SqFt"].mean()

    # Plot Donut Chart
    fig, ax = plt.subplots(figsize=(8,8))
    ax.pie(
        facing_avg,
        labels=facing_avg.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=plt.cm.Set2.colors
    )
    ax.set_title("Total Price per SqFt by Facing Direction")
    return fig

# 16. Properties by Owner Type
def plot_owner_type_distribution(df: pd.DataFrame):
    owner_counts = df["Owner_Type"].value_counts()
    fig , ax = plt.subplots(figsize=(8,6))
    sns.barplot(x=owner_counts.index, y=owner_counts.values, ax=ax)
    ax.set_title("Number of Properties by Owner Type")
    ax.set_ylabel("Count")
    ax.set_xlabel("Owner Type")
    # Add data labels on top of bars
    for p in ax.patches:
        ax.annotate(
            f'{int(p.get_height())}',                # bar height
            (p.get_x() + p.get_width() / 2., p.get_height()),  # position
            ha='center', va='bottom', fontsize=10, color='black', xytext=(0, 5),
            textcoords='offset points'
        )

    return fig

# 17. Properties by Availability Status
def plot_availability_status_distribution(df: pd.DataFrame):
    status_counts = df["Availability_Status"].value_counts()
    fig, ax = plt.subplots(figsize=(8,6))
    sns.barplot(x=status_counts.index, y=status_counts.values)
    ax.set_title("Number of Properties by Availability Status")
    ax.set_ylabel("Count")
    ax.set_xlabel("Availability Status")
    ax.set_xticklabels(status_counts.index, rotation=45)
    # Add data labels on top of bars
    for p in ax.patches:
        ax.annotate(
            f'{int(p.get_height())}',                # bar height
            (p.get_x() + p.get_width() / 2., p.get_height()),  # position
            ha='center', va='bottom', fontsize=10, color='black', xytext=(0, 5),
            textcoords='offset points'
        )
    return fig

# 18. Parking Space vs Property Price
def plot_parking_vs_price(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10,6))
    sns.boxplot(x="Parking_Space", y="Price_in_Lakhs", data=df, ax=ax)
    ax.set_title("Parking Space vs Property Price")
    ax.set_xlabel("Parking Space")
    ax.set_ylabel("Price (Lakhs)")
    return fig

# 19. Amenities vs Price per SqFt
def plot_amenities_vs_price_sqft(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10,6))
    sns.boxplot(x="Amenities", y="Price_per_SqFt", data=df, ax=ax)
    ax.set_title("Amenities vs Price per SqFt")
    ax.set_xlabel("Amenities")
    ax.set_ylabel("Price per SqFt")
    # ax.set_xticklabels(rotation=45)
    return fig

# 20. Public Transport Accessibility vs Price per SqFt / Investment Potential
def plot_transport_vs_price_investment(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10,6))
    sns.scatterplot(x="Public_Transport_Accessibility", y="Price_per_SqFt", data=df, hue="Good_Investment", alpha=0.6)
    ax.set_title("Public Transport Accessibility vs Price per SqFt / Investment Potential")
    ax.set_xlabel("Transport Accessibility Score")
    ax.set_ylabel("Price per SqFt")
    corr = df["Public_Transport_Accessibility"].corr(df["Price_per_SqFt"])
    return fig, corr


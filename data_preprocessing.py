# -*- coding: utf-8 -*-
"""Data Preprocessing.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18k8eydSJ3K21iBRu5lez-qZimweYB9oJ

# **1. Visualizing Before Dataset Cleaning**
"""

import streamlit as st
st.title('Wastewater Treatment Plants')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("Data-Melbourne_F_fixed.csv")

df.shape

df.head()

df.tail()

df.dtypes

df.info()

df.describe()

df.columns

"""##**1.1. Missing Values (Heatmap)**



"""

# Replace zeros with NaN for the columns that should have missing values
df_with_zeros_as_nan = df.replace(0, pd.NA)

# Generate the missing value heatmap
msno.matrix(df_with_zeros_as_nan, color=(0.3, 0.6, 0.9))

# Title and display the heatmap
plt.title("Missing Data Heatmap (Zeros as NaN)")
plt.show()

"""The blue bar with white gaps shows that columns Atmospheric Pressure, Total Rainfall, and Average Visibility have high counts of missing values.

##**1.2. Outliers (Boxplots)**
"""

# Select only numerical columns
numeric_cols = df.select_dtypes(include=np.number).columns

# Set up the figure
plt.figure(figsize=(16, len(numeric_cols) * 4))

# Plot boxplots for each numeric column
for i, col in enumerate(numeric_cols, 1):
    plt.subplot(len(numeric_cols), 1, i)
    sns.boxplot(x=df[col], color='skyblue')
    plt.title(f'Box Plot of {col}')
    plt.tight_layout()

plt.show()

"""The dataset got outliers.

## **1.3 Contaminated Data**
"""

# Check for unrealistic or invalid values for each feature and display the count

# Invalid Energy Consumption
invalid_energy_consumption_count = df[(df['Energy Consumption'] <= 0)].shape[0]

# Invalid Inflow and Outflow
invalid_inflow_outflow_count = df[(df['Average Inflow'] <= 0) | (df['Average Outflow'] <= 0)].shape[0]

# Invalid Contaminants (Ammonia, BOD, COD, Total Nitrogen)
invalid_contaminants_count = df[(df['Ammonia'] < 0) | (df['Biological Oxygen Demand'] < 0) |
                                 (df['Chemical Oxygen Demand'] < 0) | (df['Total Nitrogen'] < 0)].shape[0]

# Invalid Atmospheric Pressure
invalid_pressure_count = df[(df['Atmospheric pressure'] <= 0) | (df['Atmospheric pressure'] > 2000)].shape[0]

# Invalid Humidity
invalid_humidity_count = df[(df['Average humidity'] < 0) | (df['Average humidity'] > 100)].shape[0]

# Invalid Rainfall
invalid_rainfall_count = df[df['Total rainfall'] < 0].shape[0]

# Invalid Visibility
invalid_visibility_count = df[(df['Average visibility'] <= 0)].shape[0]

# Invalid Average Wind Speed
invalid_average_wind_speed_count = df[(df['Average wind speed'] <= 0)].shape[0]

# Invalid Maximum Wind Speed
invalid_maximum_wind_speed_count= df[df['Maximum wind speed'] <= 0].shape[0]

# Print the count of invalid rows for each feature
print(f"Invalid Energy Consumption Rows: {invalid_energy_consumption_count}")
print(f"Invalid Inflow/Outflow Rows: {invalid_inflow_outflow_count}")
print(f"Invalid Contaminants Rows: {invalid_contaminants_count}")
print(f"Invalid Atmospheric Pressure Rows: {invalid_pressure_count}")
print(f"Invalid Humidity Rows: {invalid_humidity_count}")
print(f"Invalid Rainfall Rows: {invalid_rainfall_count}")
print(f"Invalid Visibility Rows: {invalid_visibility_count}")
print(f"Invalid Average Wind Speed Rows: {invalid_average_wind_speed_count}")
print(f"Invalid Maximum Wind Speed Rows: {invalid_maximum_wind_speed_count}")

# Count of unrealistic temperature values for each temperature column

# Count rows where temperatures are out of the defined range
unrealistic_temp_count = df[(df['Average Temperature'] < -10) |
                             (df['Average Temperature'] > 50) |
                             (df['Maximum temperature'] < -10) |
                             (df['Maximum temperature'] > 50) |
                             (df['Minimum temperature'] < -10) |
                             (df['Minimum temperature'] > 50)].shape[0]

# Print the count of rows with unrealistic temperature values
print(f"Invalid Temperature Rows: {unrealistic_temp_count}")

# Count rows with invalid dates
invalid_dates_count = df[(df['Month'] < 1) |
                          (df['Month'] > 12) |
                          (df['Day'] < 1) |
                          (df['Day'] > 31)].shape[0]

# Print the count of invalid dates
print(f"Invalid Date Rows: {invalid_dates_count}")

"""The features Atmospheric Pressure, Visibility, and Wind Speed are not useful for clustering energy consumption profiles in wastewater treatment plants. These features either don't directly influence energy consumption or have invalid data and should be excluded from the analysis.

## **1.4 Inconsistent Data**
"""

# Function to count decimal places
def count_decimal_places(value):
    if isinstance(value, float):
        if value.is_integer():
            return 0
        return len(str(value).split('.')[-1])
    return 0

decimal_place_consistency = {}

for column in df.columns:
    if df[column].dtype == 'float64':
        decimal_places = set()

        for value in df[column]:
            decimal_places.add(count_decimal_places(value))

        decimal_place_consistency[column] = len(decimal_places)

for column, num_decimal_places in decimal_place_consistency.items():
    if num_decimal_places > 1:
        print(f"Column '{column}' has inconsistent decimal places.")
    else:
        print(f"Column '{column}' has consistent decimal places.")

"""Decimal place inconsistencies: In numerical columns, some have one decimal place, and others have two or more decimal places.

## **1.5 Duplicate Data**
"""

# Count duplicate rows based on all columns
duplicate_count = df.duplicated().sum()

print(f"Number of duplicate rows: {duplicate_count}")

"""The dataset contains no duplicate rows based on all columns, as no duplicate entries were found.

## **1.6 Data Type Issues**
"""

# Select the numerical columns
numerical_columns = df.select_dtypes(include=['float64']).columns  # Only float columns

# Check if the float columns contain only integer values
for column in numerical_columns:
    # Check if all values are integers
    if all(df[column].apply(lambda x: x.is_integer())):
        print(f"Column '{column}' has float data type but contains only integer values.")

"""Data type inconsistencies: Some columns that are expected to have integer values are stored as float64, which is unnecessary since the values do not have decimals.

# **2. Data Preprocessing**

## **2.1 Data Transformation**
"""

# Drop the "Unnamed" column
df_clean = df.drop(columns=['Unnamed: 0'])

# Rename the columns
short_column_names = {
    'Average Outflow': 'Avg_Outflow',
    'Average Inflow': 'Avg_Inflow',
    'Energy Consumption': 'Energy_Cons',
    'Ammonia': 'Ammonia',
    'Biological Oxygen Demand': 'BOD',
    'Chemical Oxygen Demand': 'COD',
    'Total Nitrogen': 'TN',
    'Average Temperature': 'Avg_Temperature',
    'Maximum temperature': 'Max_Temperature',
    'Minimum temperature': 'Min_Temperature',
    'Atmospheric pressure': 'Atmos_Pressure',
    'Average humidity': 'Avg_Humidity',
    'Total rainfall': 'Rainfall',
    'Average visibility': 'Avg_Visibility',
    'Average wind speed': 'Avg_Wind_Speed',
    'Maximum wind speed': 'Max_Wind_Speed',
    'Year': 'Year',
    'Month': 'Month',
    'Day': 'Day'
}

# Rename columns
df_clean = df_clean.rename(columns=short_column_names)

# Check the updated dataframe
df_clean.head()

"""## **2.2 Handle Missing Values and Contaminated Data**"""

# Calculate the percentage of zero values for each column
zero_percentage = (df_clean == 0).mean() * 100

columns_with_high_zeros = zero_percentage[zero_percentage > 50]

print("Columns with more than 50% zero values:")
print(columns_with_high_zeros)

columns_to_remove = ['Atmos_Pressure', 'Rainfall', 'Avg_Visibility', 'Avg_Wind_Speed', 'Max_Wind_Speed']

df_clean = df_clean.drop(columns=columns_to_remove)

df_clean.head()

# Calculate again the percentage of zero values for each column
zero_percentage = (df_clean == 0).mean() * 100

columns_with_high_zeros = zero_percentage[zero_percentage > 50]

print("Columns with more than 50% zero values:")
print(columns_with_high_zeros)

"""Columns that do not contribute to the analysis or prediction and have a significant percentage of missing values are removed.

## **2.3 Handle Outliers**
"""

# Calculate IQR for each column
Q1 = df_clean.quantile(0.25)
Q3 = df_clean.quantile(0.75)
IQR = Q3 - Q1

outliers_iqr = (df_clean < (Q1 - 1.5 * IQR)) | (df_clean > (Q3 + 1.5 * IQR))

outliers_iqr_count = outliers_iqr.sum()
print(f"Outliers detected using IQR:\n{outliers_iqr_count}")

df_clean[['Avg_Outflow', 'Avg_Inflow', 'Energy_Cons', 'Ammonia', 'BOD', 'COD', 'TN', 'Avg_Temperature','Max_Temperature','Min_Temperature', 'Avg_Humidity']].hist(bins=30, figsize=(15, 10))
plt.suptitle("Histograms Before Remove Outliers")
plt.show()

# Remove rows with outliers based on IQR method
df_no_outliers = df_clean[~outliers_iqr.any(axis=1)]

"""The outliers was removed.

## **2.4 Handle Inconsistent data**
"""

# List of columns with inconsistent decimal places (as you mentioned in your output)
inconsistent_columns = [
    'Avg_Outflow',
    'Avg_Inflow',
    'Energy_Cons',
    'COD',
    'TN',
    'Avg_Temperature',
    'Max_Temperature',
    'Min_Temperature',
    'Avg_Humidity'
]

# Round inconsistent columns to 2 decimal places
for column in inconsistent_columns:
    if column in df_no_outliers.columns:
        df_no_outliers[column] = df_no_outliers[column].round(2)

df_no_outliers.head()

"""The columns with inconsistent decimal places will be rounded to 2 decimal places.

## **2.5 Handle Data Types Issues**
"""

# Convert columns with float type that contain only integer values to integer type

columns_to_convert = [
    'Energy_Cons',
    'Avg_Humidity',
    'Year',
    'Month',
    'Day'
]

for column in columns_to_convert:
    if column in df_no_outliers.columns:
        df_no_outliers[column] = df_no_outliers[column].astype(int)

df_no_outliers.dtypes

"""Columns Energy_Cons, Avg_Humidity, Year, Month, and Day was converted to integer type."""

#Save the processed data to csv
df_no_outliers.to_csv('processed_data.csv', index=False)

"""# **3. Feature Engineering**"""

# Select numerical columns (both float and integer types) from df_no_outliers
numeric_cols = df_no_outliers.select_dtypes(include=['float64', 'int64']).columns

# Apply StandardScaler to the numerical columns of df_no_outliers
df_scaled = StandardScaler().fit_transform(df_no_outliers[numeric_cols])

# Convert the scaled values back into a DataFrame for easier handling
df_scaled = pd.DataFrame(df_scaled, columns=numeric_cols)

from sklearn.decomposition import PCA

pca = PCA(n_components=11)  # Try using 5 components
df_pca = pca.fit_transform(df_scaled)
cumulative_variance = pca.explained_variance_ratio_.cumsum()
print("Cumulative Explained Variance with 11 components:", cumulative_variance)

"""# **4. Clustering Algorithm Selection**

## **4.1 HDBSCAN**
"""

import hdbscan

clusterer = hdbscan.HDBSCAN(min_samples=10, min_cluster_size=100)

df_scaled['HDBSCAN_labels'] = clusterer.fit_predict(df_scaled)

print(df_scaled[['HDBSCAN_labels']].head())

"""## **4.2 OPTICS**"""

from sklearn.cluster import OPTICS

optics = OPTICS(min_samples=10)
df_scaled['OPTICS_labels'] = optics.fit_predict(df_scaled)

print(df_scaled[['OPTICS_labels']].head())

"""## **4.3 Agglomerative**"""

from sklearn.cluster import AgglomerativeClustering

agglo = AgglomerativeClustering(n_clusters=5)  # Adjust number of clusters as needed
df_scaled['Agglomerative_labels'] = agglo.fit_predict(df_scaled)

print(df_scaled[['Agglomerative_labels']].head())

"""## **4.4 AffinityProgagation**"""

from sklearn.cluster import AffinityPropagation

affinity = AffinityPropagation()
df_scaled['Affinity_labels'] = affinity.fit_predict(df_scaled)

print(df_scaled[['Affinity_labels']].head())

"""## **4.5 Self-Organizing Maps**"""

from minisom import MiniSom

som = MiniSom(10, 10, df_scaled.shape[1], sigma=1.0, learning_rate=0.5)

som.train(df_scaled.values, 1000)

som_labels = [som.winner(x) for x in df_scaled.values]

som_labels_1d = [x[0] * 10 + x[1] for x in som_labels]

df_scaled['SOM_labels'] = som_labels_1d

print(df_scaled[['SOM_labels']].head())

"""## **4.6 MeanShift**"""

from sklearn.cluster import MeanShift

mean_shift = MeanShift()
df_scaled['MeanShift_labels'] = mean_shift.fit_predict(df_scaled)

print(df_scaled[['MeanShift_labels']].head())

"""# **5. Clustering Evaluation**"""

from sklearn.metrics import silhouette_score, davies_bouldin_score

silhouette_scores = {}
davies_bouldin_scores = {}

som_labels_1d = [x[0] * 10 + x[1] for x in som_labels]

silhouette_scores['SOM'] = silhouette_score(df_scaled, som_labels_1d)
davies_bouldin_scores['SOM'] = davies_bouldin_score(df_scaled, som_labels_1d)

for algorithm in ['HDBSCAN', 'OPTICS', 'Agglomerative', 'Affinity', 'MeanShift']:
    labels = df_scaled[f'{algorithm}_labels']
    silhouette_scores[algorithm] = silhouette_score(df_scaled, labels)
    davies_bouldin_scores[algorithm] = davies_bouldin_score(df_scaled, labels)

print("Silhouette Scores:", silhouette_scores)
print("Davies-Bouldin Scores:", davies_bouldin_scores)

"""Best Algorithm:

*  Silhouette Score: MeanShift has the highest silhouette score (0.392), suggesting it performed the best in terms of cluster separation and cohesion.

*  DBI: Affinity Propagation has the lowest DBI (0.50), suggesting it has the most compact and well-separated clusters.

Worst Algorithm:

*  Silhouette Score: Both HDBSCAN and OPTICS have negative silhouette scores, indicating poor clustering performance.

*  DBI: HDBSCAN and OPTICS have the highest DBI values, suggesting that their clusters are poorly separated.
"""

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Apply PCA for visualization (using 2 components)
pca = PCA(n_components=2)
df_pca = pca.fit_transform(df_scaled)

# Convert PCA results into DataFrame, ensuring the same index as df_scaled
df_pca = pd.DataFrame(df_pca, columns=['PCA1', 'PCA2'], index=df_scaled.index)

# Plot the clusters (assuming PCA transformation for 2D visualization)
plt.figure(figsize=(8, 6))
plt.scatter(df_pca['PCA1'], df_pca['PCA2'], c=df_scaled['MeanShift_labels'], cmap='viridis', alpha=0.7)
plt.title('MeanShift Clustering Visualization')
plt.xlabel('PCA1')
plt.ylabel('PCA2')
plt.show()
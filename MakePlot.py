import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def sanitize_filename(name):
    """Replace invalid characters in the filename."""
    return name.replace("/", "_")

def plot_correlation_matrix(data, output_dir):
    # Compute the correlation matrix
    correlation_matrix = data.corr()

    # Create a mask for the upper triangle
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

    # Plot the correlation matrix as a heatmap with correlation values in the cells
    plt.figure(figsize=(30, 28))  # Enlarge figure further for better clarity
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', 
                linewidths=0.5, cbar_kws={'shrink': 0.8}, mask=mask, square=True)
    
    # Rotate the axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=45, va='top')

    plt.title("Correlation Matrix of Numerical Variables")
    
    # Adjust the layout to prevent label overlap
    plt.tight_layout()

    # Save the plot
    output_path = os.path.join(output_dir, "correlation_matrix.png")
    plt.savefig(output_path)
    plt.close()  # Close the plot to free up memory

def plot_histograms_with_limited_range(data, column, output_dir, lower_percentile=1, upper_percentile=99):
    # Calculate the lower and upper bounds for the range
    lower_bound = np.percentile(data[column].dropna(), lower_percentile)
    upper_bound = np.percentile(data[column].dropna(), upper_percentile)
    
    # Create histograms with the limited range
    plt.figure(figsize=(10, 6))
    data[data["pricechange/year"] > 1.3][column].hist(
        bins=100, alpha=0.5, label="pricechange/year > 1.3", density=True, range=(lower_bound, upper_bound)
    )
    data[data["pricechange/year"] < 1.3][column].hist(
        bins=100, alpha=0.5, label="pricechange/year < 1.3", density=True, range=(lower_bound, upper_bound)
    )
    plt.title(f"Normalized Distribution of {column} (Limited Range)")
    plt.xlabel(column)
    plt.ylabel("Probability Density")
    plt.legend()
    plt.grid(True)
    
    # Save the plot with sanitized filename
    sanitized_column = sanitize_filename(column)
    output_path = os.path.join(output_dir, f"{sanitized_column}_distribution.png")
    plt.savefig(output_path)
    plt.close()  # Close the plot to free up memory

# Path to preprocess directory
preprocess_path = "./preprocess"

# Step 1: Identify the most recent directory
recent_dir = max([d for d in os.listdir(preprocess_path) if os.path.isdir(os.path.join(preprocess_path, d))])

# Step 2: Create output directory in `./plot/`
plot_dir = f"./plot/{recent_dir}"
os.makedirs(plot_dir, exist_ok=True)

# Step 3: Read all CSV files in the most recent directory
recent_dir_path = os.path.join(preprocess_path, recent_dir)
all_data = pd.concat(
    [pd.read_csv(os.path.join(recent_dir_path, file)) for file in os.listdir(recent_dir_path) if file.endswith(".csv")]
)

# Step 4: Draw histograms for all numerical columns except specified ones
exclude_columns = {"symbol", "date", "pricechange/year"}
numerical_columns = [col for col in all_data.columns if col not in exclude_columns and pd.api.types.is_numeric_dtype(all_data[col])]

# Step 5: Create and save normalized histograms
for column in numerical_columns:
    plot_histograms_with_limited_range(all_data, column, plot_dir)

plot_correlation_matrix(all_data[numerical_columns], plot_dir)

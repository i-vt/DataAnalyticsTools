import numpy as np
import pandas as pd

def summary(data):
    """
    Provide a statistical summary of a NumPy array or Pandas Series, similar to R's summary function.
    """
    if isinstance(data, list):
        data = np.array(data)
    
    summary_data = {
        "Min": np.min(data),
        "1st Quartile": np.percentile(data, 25),
        "Median": np.median(data),
        "Mean": np.mean(data),
        "3rd Quartile": np.percentile(data, 75),
        "Max": np.max(data)
    }

    return pd.DataFrame(summary_data, index=[0])

def summary_with_correlation(df):
    """
    Provide a statistical summary and correlation matrix for a Pandas DataFrame, similar to R's summary function.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a Pandas DataFrame")

    # Summary statistics
    summary_stats = df.describe().T
    summary_stats['Mean'] = df.mean()
    summary_stats['Median'] = df.median()

    # Correlation matrix
    correlation_matrix = df.corr()

    return summary_stats, correlation_matrix

# Example usage with a DataFrame
data = pd.DataFrame({
    'col1': np.random.rand(100),
    'col2': np.random.rand(100),
    'col3': np.random.rand(100)
})

summary_stats, correlation_matrix = summary_with_correlation(data)
print("Summary Statistics:\n", summary_stats)
print("\nCorrelation Matrix:\n", correlation_matrix)


# Example usage with an array
data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(summary(data))

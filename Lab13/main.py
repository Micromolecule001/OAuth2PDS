import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Load Excel Files
def load_excel_files(file_paths):
    """
    Load multiple Excel files into a dictionary of DataFrames.
    :param file_paths: List of Excel file paths.
    :return: Dictionary with file names as keys and DataFrames as values.
    """
    dfs = {}
    for file_path in file_paths:
        df = pd.read_excel(file_path)

        # Convert column names to strings, ensuring compatibility with .str methods
        df.columns = [str(col) for col in df.columns]

        # Clean column names: remove special characters and whitespace
        df.columns = df.columns.str.replace(r'[^\w\s]', '', regex=True).str.strip()

        # Debug: Print the cleaned column names
        print(f"Columns in {file_path}: {list(df.columns)}")
        
        # Save the DataFrame in the dictionary
        dfs[file_path] = df
    
    return dfs

# Step 2: Calculate Key Statistics
def calculate_statistics(df, file_name):
    """
    Calculate statistics: mean, std, min, and max for Pause and Duration columns.
    :param df: DataFrame with 'Key', 'Pause' and 'Duration' columns.
    :param file_name: The name of the file to handle specific column names.
    :return: DataFrame with calculated statistics.
    """
    # Handle column names based on the file
    pause_column = 'Pause ms'
    duration_column = 'Duration ms'

    stats = pd.DataFrame({
        'Mean(Pause)': df[pause_column].mean(),
        'Std(Pause)': df[pause_column].std(),
        'Min(Pause)': df[pause_column].min(),
        'Max(Pause)': df[pause_column].max(),
        'Mean(Duration)': df[duration_column].mean(),
        'Std(Duration)': df[duration_column].std(),
        'Min(Duration)': df[duration_column].min(),
        'Max(Duration)': df[duration_column].max(),
    }, index=[0])
    
    return stats

# Step 3: Plot Duration Over Time
def plot_duration(df, title="Duration Plot"):
    """
    Plot the duration of key presses from the DataFrame.
    :param df: DataFrame with columns 'Key' and 'Duration ms'.
    :param title: Title of the plot.
    """
    try:
        # Ensure 'Key' is converted to strings for categorical plotting
        df['Key'] = df['Key'].astype(str)
        
        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(df['Key'], df['Duration ms'], label='Duration', marker='o')
        plt.xlabel("Keys")
        plt.ylabel("Duration (ms)")
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    except KeyError as e:
        print(f"Error: Missing column in DataFrame - {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Step 4: Generate Biometric Template
def generate_biometric_template(stats_df):
    """
    Generate a biometric template dynamically from statistical data.
    :param stats_df: DataFrame with statistics (mean, std, min, max).
    :return: DataFrame representing the biometric template.
    """
    # Ensure the stats_df includes a 'Key' column if not already present
    if 'Key' not in stats_df.columns:
        stats_df.insert(0, 'Key', [f'Key_{i+1}' for i in range(len(stats_df))])
    
    # Prepare the biometric template with existing keys and statistics
    biometric_template = {
        'Key': stats_df['Key'].values,
        'Mean(Pause)': stats_df['Mean(Pause)'].values,
        'Std(Pause)': stats_df['Std(Pause)'].values,
        'Min(Pause)': stats_df['Min(Pause)'].values,
        'Max(Pause)': stats_df['Max(Pause)'].values,
        'Mean(Duration)': stats_df['Mean(Duration)'].values,
        'Std(Duration)': stats_df['Std(Duration)'].values,
        'Min(Duration)': stats_df['Min(Duration)'].values,
        'Max(Duration)': stats_df['Max(Duration)'].values,
    }
    
    return pd.DataFrame(biometric_template)

# Step 5: Add Custom Data and Calculations
def add_custom_statistics():
    """
    Add a table with custom vectors (v1, v2, ..., vL) and calculate their statistics.
    :return: DataFrame with calculated statistics.
    """
    # Example data: Replace with your actual data
    data = {
        'v1': [1.2, 1.3, 1.1, 1.4],
        'v2': [0.8, 0.7, 0.9, 0.85],
        'v3': [1.5, 1.6, 1.4, 1.3],
        'v4': [1.4, 0.8, 1.3, 1.1],
        'v5': [0.9, 1.5, 1.3, 1.3],
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Calculate statistics
    means = df.mean()
    std_devs = df.std()
    mins = df.min()
    maxs = df.max()

    # Add statistics as rows to the table
    statistics_df = df.copy()
    statistics_df.loc['m(vi)'] = means
    statistics_df.loc['σ(vi)'] = std_devs
    statistics_df.loc['min(vi)'] = mins
    statistics_df.loc['max(vi)'] = maxs

    # Fill missing cells with empty strings
    statistics_df.fillna('', inplace=True)

    # Save table to CSV for inspection
    statistics_df.to_csv("custom_statistics.csv")

    # Return the custom statistics DataFrame
    return statistics_df

# Main Function to Run the Analysis
def main():
    # Step 1: Specify file paths for the Excel files
    file_paths = ['file1.xlsx', 'file2.xlsx', 'file3.xlsx', 'file4.xlsx', 'file5.xlsx']  # Replace with your actual file paths
    
    # Step 2: Load the Excel files into DataFrames
    dfs = load_excel_files(file_paths)
    
    # Step 3: Process each file and calculate statistics, passing the file name
    stats_dfs = [calculate_statistics(df, file_name) for file_name, df in dfs.items()]
    combined_stats = pd.concat(stats_dfs, ignore_index=True)
    
    # Step 4: Plot the duration for one of the files (first file as example)
    plot_duration(dfs[file_paths[0]], title="Duration for File 1")
    
    # Step 5: Generate the biometric template from the statistics
    biometric_df = generate_biometric_template(combined_stats)
    print("Biometric Template:")
    print(biometric_df)
    
    # Save biometric template to a CSV
    biometric_df.to_csv("biometric_template.csv", index=False)
    
    # Step 6: Add and save custom statistics
    custom_stats_df = add_custom_statistics()
    print("Custom Statistics:")
    print(custom_stats_df)

    # Save custom statistics to a CSV
    custom_stats_df.to_csv("custom_statistics.csv")
    
    # Conclusion
    print("\nAnalysis complete. Files have been saved.")
    print("Biometric template: 'biometric_template.csv'")
    print("Custom statistics: 'custom_statistics.csv'")

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()


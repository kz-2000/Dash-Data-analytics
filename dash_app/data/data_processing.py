import pandas as pd

def calculate_conversion_rate(df):
    # Calculate cumulative counts
    df['cumulative_total'] = range(1, len(df) + 1)
    df['cumulative_converted'] = df['status'].eq('CONFIRMED').cumsum()
    
    # Calculate total conversion rate
    df['total_conversion_rate'] = (df['cumulative_converted'] / df['cumulative_total']).fillna(0)
    
    # Debug: print out the DataFrame columns and first few rows
    print("Proposal Data Columns:", df.columns)
    print("Proposal Data Sample:", df.head())
    
    return df
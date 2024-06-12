import pandas as pd

def calculate_conversion_rate(df):
    # Calculate cumulative counts
    df['cumulative_total'] = df.index + 1
    df['cumulative_converted'] = (df['status'] == 'CONFIRMED').astype(int).cumsum()

    # Calculate total conversion rate
    df['total_conversion_rate'] = (df['cumulative_converted'] / df['cumulative_total'])
    print(df['total_conversion_rate'])
    
    # Debug: print out the DataFrame columns and first few rows

    print("Proposal Data Sample:", df.head())
    
    return df
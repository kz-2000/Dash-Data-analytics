import pandas as pd

def calculate_conversion_rate(df):
    # Calculate cumulative counts
    df['cumulative_total'] = df.index + 1
    df['cumulative_converted'] = (df['status'] == 'CONFIRMED').astype(int).cumsum()

    # Calculate total conversion rate
    df['total_conversion_rate'] = (df['cumulative_converted'] / df['cumulative_total'])
    #print(df['total_conversion_rate'])
    
    # Debug: print out the DataFrame columns and first few rows

   # print("Proposal Data Sample:", df.head())
    
    return df

def merge_tables(df1, df2, left_column, right_column):
    # Merge the data on supplier_id
    merged_data = pd.merge(df1, df2, left_on=left_column, right_on=right_column)
    
    return merged_data
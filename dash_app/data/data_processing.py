import pandas as pd

def calculate_conversion_rate(proposal_df, itinerary_df):
       # Ensure the correct column names for merging
    proposal_df.rename(columns={'created_at': 'created_at_proposal'}, inplace=True)
    itinerary_df.rename(columns={'created_at': 'created_at_itinerary'}, inplace=True)

   # print(proposal_df.info())
   # print(itinerary_df.info())

 # Merge proposals with itineraries on 'id' and 'proposal_id'
    merged_df = pd.merge(proposal_df, itinerary_df, left_on='id', right_on='proposal_id', how='left')

   # print(merged_df.info())

     # Convert the 'created_at' columns to datetime
    merged_df['created_at_proposal'] = pd.to_datetime(merged_df['created_at_proposal'], format='ISO8601')
    merged_df['created_at_itinerary'] = pd.to_datetime(merged_df['created_at_itinerary'], format='ISO8601')


    # Sort by proposal creation date
    merged_df = merged_df.sort_values(by='created_at_proposal', ascending=True).reset_index()

    # Calculate cumulative counts
    merged_df['cumulative_total'] = merged_df.index + 1
    merged_df['cumulative_converted'] = (merged_df['status'] == 'CONFIRMED').astype(int).cumsum()

   # print(merged_df['cumulative_total'])
   # print(merged_df['cumulative_converted'])

    # Calculate total conversion rate
    merged_df['total_conversion_rate'] = (merged_df['cumulative_converted'] / merged_df['cumulative_total'])

  #  print(merged_df)
    # Aggregate by day to get the daily conversion rate
   # conversion_rate_by_day = merged_df.resample('D', on='created_at_proposal').last().reset_index()

       # Resample by day to get the daily conversion rate
    # We are resampling on 'created_at_proposal' since it is the primary date of interest.
    conversion_rate_by_day = merged_df.resample('D', on='created_at_proposal').last().dropna(subset=['total_conversion_rate']).reset_index()

    # Print the resampled DataFrame for debugging
  #  print("Resampled DataFrame with daily conversion rates:")
   # print(conversion_rate_by_day.head())

  #  print(conversion_rate_by_day)t

    return merged_df[['created_at_proposal', 'total_conversion_rate']]
    
    """
    # Calculate cumulative counts
    df['cumulative_total'] = df.index + 1
    df['cumulative_converted'] = (df['status'] == 'CONFIRMED').astype(int).cumsum()

    # Calculate total conversion rate
    df['total_conversion_rate'] = (df['cumulative_converted'] / df['cumulative_total'])
    #print(df['total_conversion_rate'])
    
    # Debug: print out the DataFrame columns and first few rows

   # print("Proposal Data Sample:", df.head())
    
    return df
    """

def merge_tables(df1, df2, left_column, right_column):
    # Merge the data on supplier_id
    merged_data = pd.merge(df1, df2, left_on=left_column, right_on=right_column)
    
    return merged_data

def merge_names(df, column_name):
    df[column_name] = df['first_name'] + ' ' + df['last_name']

    return df

def pick_columns(df, *columns):
    df = df[list(columns)]

    return df
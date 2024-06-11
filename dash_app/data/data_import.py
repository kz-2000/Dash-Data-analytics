from supabase import create_client, Client
import pandas as pd

# Supabase URL and API Key
url = 'https://lmpflklddofmcbqsfdot.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxtcGZsa2xkZG9mbWNicXNmZG90Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTYzMzk4MzMsImV4cCI6MjAxMTkxNTgzM30.r_QmcE2G653d94rb7DpU3wPhiUStJVwxtqOePenLrvk'

# Create a Supabase client
supabase: Client = create_client(url, key)

def fetch_proposals_data():
    response = supabase.table('proposal').select('*').execute()
    data = response.data
    df = pd.DataFrame(data)
    df['created_at'] = pd.to_datetime(df['created_at'], format='ISO8601')
    df['updated_at'] = pd.to_datetime(df['updated_at'], format='ISO8601')
    return df

def fetch_requests_data():
    response = supabase.table('request').select('*').execute()
    data = response.data
    df = pd.DataFrame(data)
    df['created_at'] = pd.to_datetime(df['created_at'], format='ISO8601')
    return df

def fetch_area_data():
    response = supabase.table('area').select('*').execute()
    data = response.data
    return pd.DataFrame(data)

# Clean the data for the proposal table

def clean_data(df):
    df = df[~df['title'].str.contains('sample|test|ivo|nadine', case=False)]
#    df = df[df['owner_id'] != '751f6b1f-e696-4eb1-9b4e-4e93b9ef1025']
    df = df.reset_index(drop=True)

#    print(df[df['status']=='TO_DO'])
    return df

# Clean the data for the request table

def clean_request_data(df):
    print(f"Initial number of rows in the request data: {len(df)}")  # Print the initial number of rows
    
    # Filter the DataFrame
    df = df[df['status'] != 'ARCHIVED']
    
    print(f"Number of rows after filtering: {len(df)}")  # Print the number of rows after filtering
    
    # Reset the index
    df = df.reset_index(drop=True)
    
    print(f"Number of rows in the cleaned request data: {len(df)}")  # Print the number of rows after resetting the index
    
    return df

# Fetch the data
proposal_data = fetch_proposals_data()

request_data = fetch_requests_data()

# Clean the data
clean_proposal_df = clean_data(proposal_data)

clean_request_df = clean_data(request_data)
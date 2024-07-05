from supabase import create_client, Client
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase URL and API Key
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')
# Create a Supabase client
supabase: Client = create_client(url, key)


def fetch_proposals_data():
    # List of owner IDs to exclude
    excluded_owner_ids = [
        'cf5e54ff-f7b6-4ac9-b26c-b1a53a6ff421', 
        '356ed23b-ea02-41b0-98ab-89ba686e1ab2', 
        'dc424d6e-dd04-4850-be63-19b4f557ffdc',
        '392cb83a-26e9-4b81-aad5-a65144902e23'
    ]
    
    # Using the Supabase SDK to filter data
    response = supabase.table('proposal').select('*')\
        .neq('title', 'sample')\
        .neq('title', 'test')\
        .neq('title', 'ivo')\
        .neq('title', 'nadine')\
        .not_.in_('owner_id', excluded_owner_ids)\
        .execute()
        
    data = response.data
    df = pd.DataFrame(data)
    df['created_at'] = pd.to_datetime(df['created_at'], format='ISO8601')
    df['updated_at'] = pd.to_datetime(df['updated_at'], format='ISO8601')
    return df

def fetch_requests_data():
    response = supabase.table('request').select('*').neq('status', 'ARCHIVED').execute()
    data = response.data
    df = pd.DataFrame(data)
    df['created_at'] = pd.to_datetime(df['created_at'], format='ISO8601')
    return df

def fetch_area_data():
    response = supabase.table('area').select('*').execute()
    data = response.data
    return pd.DataFrame(data)

def fetch_supplier_data():
    response = supabase.table('supplier').select('*').execute()
    data = response.data
    return pd.DataFrame(data)

def fetch_proposal_service_data():
    response = supabase.table('proposal_service').select('*').execute()
    data = response.data
    return pd.DataFrame(data)

def fetch_itinerary_service_data():
    response = supabase.table('itinerary_service').select('*').execute()
    data = response.data
    return pd.DataFrame(data)

def fetch_profiles_data():
    response = supabase.table('profiles').select('*').execute()
    data = response.data
    return  pd.DataFrame(data)

def fetch_service_data():
    response = supabase.table('service').select('*').execute()
    data = response.data
    return pd.DataFrame(data)

def fetch_proposal_history_data():
    response = supabase.table('proposal_history').select('*').execute()
    data = response.data
    return pd.DataFrame(data)

def fetch_travel_agent_data():
    response = supabase.table('travel_agent').select('*').execute()
    data = response.data
    return pd.DataFrame(data)

# Clean the data for the proposal table

#def clean_data(df):
#    df = df[~df['title'].str.contains('sample|test|ivo|nadine', case=False)]
   # df = df[df['owner_id'] != 'cf5e54ff-f7b6-4ac9-b26c-b1a53a6ff421']
#    df = df.reset_index(drop=True)

#    print(df[df['status']=='TO_DO'])
 #   return df

# Clean the data for the request table

#def clean_request_data(df):
 #   df = df[df['status'] != 'ARCHIVED']

  #  df = df.reset_index(drop=True)
    
   # return df

def clean_profiles_data(df):
    df = df[df['id'] != 'dc424d6e-dd04-4850-be63-19b4f557ffdc' & '356ed23b-ea02-41b0-98ab-89ba686e1ab2']

    df = df.reset_index(drop=True)

    return df

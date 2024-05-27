import pandas as pd
from data.data_import import fetch_proposals_data, clean_data

df = fetch_proposals_data()

clean_data = clean_data()

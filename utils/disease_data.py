import pandas as pd

def load_historical_data(disease_name):
    df = pd.read_csv("data/historical_diseases.csv")
    filtered = df[df['Disease'].str.lower() == disease_name.lower()]
    return filtered.sort_values(by='Year')

def get_available_diseases():
    df = pd.read_csv("data/historical_diseases.csv")
    return df['Disease'].unique().tolist()

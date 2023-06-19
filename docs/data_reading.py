import pandas as pd

hdi = pd.read_csv('HDI.csv')
happy = pd.read_csv('Happy.csv')

def data_frame(input):
    return pd.DataFrame.head(input)

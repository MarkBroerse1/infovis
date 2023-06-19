import pandas as pd

hdi = pd.read_csv('HDI.csv')
happy = pd.read_csv('Happy.csv')

def data_frame(input):
    return pd.DataFrame.head(input)


# Merge the two dataframes based on 'country' and 'year'
merged_data = pd.merge(hdi, happy, on=['Country', 'Year'])

# Save the merged data to full_data.csv
merged_data.to_csv('full_data.csv', index=False)

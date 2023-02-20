# You can use the orca_api_wrapper.py --output-download-link and --csv_delimiter parameters to return data in csv format.
# However, not all nested JSON data is returned, you can use this script to extract all nested JSON data into a csv file.

import pandas as pd
import json

# Open the JSON file and load its contents into the data variable
with open('alerts.json', 'r') as f:
    data = json.load(f)

# Normalize the JSON data into a Pandas DataFrame
df = pd.json_normalize(data)

# Print the column names in the DataFrame
print(df.columns)

# Write the DataFrame to a CSV file
df.to_csv('alerts.csv', sep='¬', index=False)

import requests
import pandas as pd

# Define the datetime range for Socrata API request
report_datetime = "'" + '2022-03-01T00:00:00' + "' AND '2023-03-31T23:59:59'" 

# Define the API params
params = {
    '$$exclude_system_fields': False,
    '$limit':999999999,
    '$where':'report_datetime BETWEEN' + report_datetime
}

# Define the API headers
headers = {
    "X-App-Token": "Ax7ks1Cmr0r6TEssy44yJj4ts",
    "Content-type": "application/json"
}

# Call the API, including url, params and headers
response = requests.get('https://data.sfgov.org/resource/wg3w-h783.json', 
                            params=params, 
                            headers=headers
)

# JSON formatted as string
dictr = response.json()

# Normalize to Dataframe
df = pd.json_normalize(dictr)

pd.set_option('display.max_columns', None)

# What is the data shape?
print('\n\n# What is the data shape?')
data_shape = df.shape 
print(f'The data shape is {data_shape}.')

# What is the datatypes?
data_types = df.dtypes
print('\n\n# What is the datatypes?')
print(data_types) 

# How many missing values per attribute?
print('\n\n# How many missing values per attribute?')
data_missing = df.isna().sum()
print(data_missing)

# How does the categorical variables behave?
print('\n\n# How does the categorical variables behave?')
for col in df.select_dtypes(include='object'):
    print(f'\n\nColumn name: {col}')
    print(df[col].value_counts())

# How does the continuous variables behave?
print('\n\n# How does the continuous variables behave?')
data_describe = df.describe()
print(data_describe)
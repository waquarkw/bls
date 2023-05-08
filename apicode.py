import requests
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv


# CES0500000003 - Average hourly earnings of all employees, total private, seasonally adjusted
# CEU0500000001 - All employees, thousands, total private, not seasonally adjusted
# CUSR0000SA0 - All items in U.S. city average, all urban consumers, seasonally adjusted

load_dotenv()
# Using the os.environ.get function to call the BLS_API_KEY from environment variables
BLS_API_key = os.environ.get('BLS_API_KEY')
headers = {"Content-type" : "application/json"}
series_ids =  ["CES0500000003","CEU0500000001", "CUSR0000SA0"]

# Interactive function to get start year and end year from user
def get_years():
    print("Enter start year (yyyy):")
    start_year = input()
    if start_year == "":
        start_year = "2016" # Default start year if no input is provided
    print("Enter end year (yyyy):")
    end_year = input()
    if end_year == "":
        end_year = "2023" # Default end year if no input is provided
    return start_year, end_year

# Get start year and end year from user
start_year, end_year = get_years()

parameters = {
    "seriesid": series_ids,
    "startyear": start_year,
    "endyear": end_year,
    "calculations" : True,
    "registrationkey" : BLS_API_key
}
response = requests.post(
    "https://api.bls.gov/publicAPI/v2/timeseries/data/", 
    json=parameters, 
    headers=headers
)
json_response = response.json()
i = 0
for series in json_response["Results"]["series"]:
    df = pd.json_normalize(series["data"])
    df["series"] = series_ids[i]
    df.to_csv(f"series_{i}.csv", index=False)
    # This dynamic creation/naming of csv's is done to only create 3 different csv filesn (as 3 seriesid's were passed), one for each seriesid.
    i+=1

#Reading 3 data series csv's  
df1 = pd.read_csv('series_0.csv')
df2 = pd.read_csv('series_1.csv')
df3 = pd.read_csv('series_2.csv')

# Combining the 3 csv's to create a new combine_df 
combined_df = pd.concat([df1,df2,df3])

# Adding a new Column 'Y+M' to create unquie time periods in the dataframe combined_df
combined_df["Y+M"] = combined_df['year'].astype(str) +"-"+ combined_df['periodName'].astype(str)

# Writing the combined_df's to a new cdv file to perform an analysis
combined_df.to_csv('combined_file.csv', index=False)

dff = pd.read_csv("combined_file.csv")

# Grouping the rows in the comfined_file based on series column to build a line graph
groups = dff.groupby('series')

fig, ax = plt.subplots(figsize=(13,8))

# This for loop is used because it checks the value of name, which is the name of the group, and sets label_name accordingly 
for name, group in groups:
    if name == 'CES0500000003':
        label_name = 'Average hourly earnings of all employees'
    elif name == 'CEU0500000001':
        label_name = 'All employees (thousands)'
    elif name == 'CUSR0000SA0':
        label_name = 'All items in U.S. city average'
    ax.plot(group['Y+M'], group['calculations.pct_changes.12'], label = label_name)

ax.set_xlabel('Period')
ax.set_ylabel('Value')
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.gca().invert_xaxis()

ax.legend()

plt.show()

# Calculate the correlation matrix
corr = dff.pivot_table(index='Y+M', columns='series', values='calculations.pct_changes.12').corr()

# Plot the correlation matrix
fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0, ax=ax)
ax.set_title('Correlation Matrix')
plt.show()


#os.system("jupyter nbconvert --to notebook --execute --inplace pycode2nb.ipynb")

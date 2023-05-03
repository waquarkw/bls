import requests
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# CES0500000003 - Average hourly earnings of all employees, total private, seasonally adjusted
# CEU0500000001 - All employees, thousands, total private, not seasonally adjusted
# CUSR0000SA0 - All items in U.S. city average, all urban consumers, seasonally adjusted

BLS_API_key = "cde0c6b32c6341039ec07aee8d93e891"
headers = {"Content-type" : "application/json"}
series_ids =  ["CES0500000003","CEU0500000001", "CUSR0000SA0"]
parameters = {
    "seriesid": series_ids,
    "startyear":"2016", 
    "endyear":"2023",
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
    i+=1
    
df1 = pd.read_csv('series_0.csv')
df2 = pd.read_csv('series_1.csv')
df3 = pd.read_csv('series_2.csv')

combined_df = pd.concat([df1,df2,df3])
combined_df["Y+M"] = combined_df['year'].astype(str) +"-"+ combined_df['periodName'].astype(str)
combined_df.to_csv('combined_file.csv', index=False)

dff = pd.read_csv("combined_file.csv")

groups = dff.groupby('series')

fig, ax = plt.subplots(figsize=(13,8))

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

# BLS
This repository holds an API code that retrieves data from Bureau of Labor Statistics from multiple data series and analyses the data in python language

# Bureau of Labour Statistics
An analysis of 3 different data fries from BLS that are:
 CES0500000003 - Average hourly earnings of all employees, total private, seasonally adjusted,
 CEU0500000001 - All employees, thousands, total private, not seasonally adjusted,
 CUSR0000SA0 - All items in U.S. city average, all urban consumers, seasonally adjusted.
The idea of thsi project is to understand how the number of employment in the country affects the salaries of the employees in the country.
More over how the salaries of the employees in the country run against the all items costs increase or decrease on a country basis.

# Relevant Packages
Make sure to use Python 3.10 or above.

The required packages to run this project can be found in requirement.txt file.

# Features used in this project
1. Reading data from the BLS website using the end point "https://api.bls.gov/publicAPI/v2/timeseries/data/" and post method API call.
2. Authorizing the data request by using an API key for BLS Public Data API Signatures (Version 2.0) for multiple time series.
3. Receiving the daat from the client in JSON and converting into python object by using pandas "pd.json_normalize".
4. Storing the data into .csv files.
5. Combining dataframes to run an analysis.
6. Grouping the data based on Series id's to compare the datasets.
7. Running a multiple line graph analysis to observe the different series datasets over time and how they move inaccorance to each other in a visual forma.
8. Beautifying the visual by cleaning and relableing legend.
9. Finally run a correlation analysis to see the correlation between the different data series using a Correlation matrix(coolwarm)

# File to run
All the project is complied in a single .py script named "apicode.py".

To run this file add a simple text file in your root directory with a file named ".env" and add a line in this text file
 --> BLS_API_KEY=ENTER_YOUR_KEY_HERE
 
To obtain this key follow the link -> [Public Data API Key Generator V2](https://www.bls.gov/developers/home.htm)

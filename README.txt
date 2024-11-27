Car Sales Data Web Scraping and Analysis
This repository contains a Python script for web scraping car sales data from a car sales website and performing various data cleaning and analysis tasks. The dataset includes information such as car prices, mileage, transmission types, CO2 emissions, and more. The analysis focuses on cleaning the data, visualizing trends, and extracting insights.

Project Overview
The script performs the following steps:

Web Scraping: Extracts car details from a car sales website using Python, BeautifulSoup, and regular expressions. The details include car titles, prices, locations, mileage, reviews, and other features.
Data Cleaning: Handles missing or invalid data by filling, replacing, or dropping problematic values. The script also converts string representations of numeric data into proper formats (e.g., converting prices and mileage to integers).
Data Analysis: Groups the data by different features (e.g., year, transmission type, body type) and computes useful statistics like total sales and average reviews.
Visualization: Plots bar and line charts to visualize trends in the data, such as car sales by year, transmission type, and body type.
Exporting Data: Outputs cleaned data and analysis results to CSV files for further use.
Installation
Requirements
Python 3.x
Required libraries: pandas, numpy, matplotlib, requests, beautifulsoup4
Install Dependencies
You can install the required dependencies using pip:

bash
Copy code
pip install pandas numpy matplotlib requests beautifulsoup4
Usage
1. Run the Script
The script performs the web scraping and data cleaning/analysis tasks automatically. To run it, execute the script as follows:

bash
Copy code
python car_sales_analysis.py
2. Expected Output
The script will generate the following outputs:

raw_webscraping_output.csv: The raw web scraped data.
Q2b_data_cleaned.csv: The cleaned data after preprocessing steps.
Various CSV files with analysis results:
Car sales by year.
Car sales by transmission type.
Car sales by body type.
Top 10 cars by number of reviews.

3. Visualizations
The script will also generate visualizations using matplotlib:

A line chart showing car sales over the years.
Bar charts showing car sales by transmission type and body type.
Data Cleaning Details
Price: Removed the "£" symbol and commas, and converted the values to integers.
Mileage: Removed commas and converted values to integers.
CO2 Emissions: Removed "g/km" and converted to integers.
Year: Converted to integer format.
Location/Distance: Converted various distance metrics (e.g., yards to miles).
Number of Reviews: Converted to integers and handled missing values.

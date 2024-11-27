import requests
import random
import time
import re
from bs4 import BeautifulSoup

# Define headers and proxy for the requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
proxy = {'http': 'http://41.65.55.10:1976'}

# Create empty lists for car details
urls, prices, titles, distances = [], [], [], []
mileages, years, fuel_types, transmissions = [], [], [], []
body_types, colours, doors, engine_sizes = [], [], [], []
co2s, rating_values, review_counts = [], [], []

# Define a function to extract details
def find_detail(car_page, index):
    details = car_page.find_all("span", {"class": "vd-spec-value"})
    return details[index].text.strip() if len(details) > index else "N/A"

# Set up a session for requests
session = requests.Session()
session.headers.update(headers)

# Loop through pages 1-50
for page_num in range(1, 51):
    url = f"https://www.theaa.com/used-cars/displaycars?fullpostcode=E27NT&travel=2000&page={page_num}"
    page = requests.get(url, headers=headers, proxies=proxy)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Parse car listings
    all_cars = soup.find("div", {"class": "vl-list"}).find_all("div", {"class": "vl-item"})
    
    for car in all_cars:
        # Extract individual car details
        details_url = "https://www.theaa.com/" + re.findall(r'href="(.*?)"', str(car.find("div", {"class": "view-vehicle"})))[0]
        urls.append(details_url)
        prices.append(car.find("strong", {"class": "total-price strong-inline new-transport--bold"}).text.strip().split()[0])
        distances.append(car.find("div", {"class": "vl-location"}).text.replace(" from you", "").strip())
        titles.append(re.search(r'title="(.*?)"', str(car)).group(1) if re.search(r'title="(.*?)"', str(car)) else "")
        
        # Request individual car details
        car_page = session.get(details_url)
        car_soup = BeautifulSoup(car_page.content, "html.parser")
        
        # Extract additional details for each car
        mileage = find_detail(car_soup, 0)
        year = find_detail(car_soup, 1)
        fuel_type = find_detail(car_soup, 2)
        transmission = find_detail(car_soup, 3)
        body_type = find_detail(car_soup, 4)
        colour = find_detail(car_soup, 5)
        num_doors = find_detail(car_soup, 6)
        engine_size = find_detail(car_soup, 7)
        co2 = find_detail(car_soup, 8)
        
        # Extract ratings and review counts
        rating_html = car_soup.find_all("div", {"itemprop": "ratingValue"})
        review_html = car_soup.find_all("div", {"itemprop": "ratingCount"})
        
        rating_values.append(float(rating_html[0].get("content", "N/A")) if rating_html else "N/A")
        review_counts.append(int(review_html[0].get("content", "N/A")) if review_html else "N/A")
        
        # Append car details to the lists
        mileages.append(mileage)
        years.append(year)
        fuel_types.append(fuel_type)
        transmissions.append(transmission)
        body_types.append(body_type)
        colours.append(colour)
        doors.append(num_doors)
        engine_sizes.append(engine_size)
        co2s.append(co2)
        
        # Track the number of rows loaded
        print(f"\rNumber of rows generated: {len(urls)}", end='')




# Create a dictionary with car details
carsDict = {
    "Sales Title": titles, 
    "Location/Distance (Miles)": distances, 
    "Price (£)": prices, 
    "Mileage": mileages, 
    "Year": years, 
    "Fuel Type": fuel_types, 
    "Transmissions": transmissions, 
    "Colour": colours, 
    "Number of Doors": doors, 
    "Engine Size": engine_sizes, 
    "Number of Reviews": review_counts, 
    "Rating": rating_values, 
    "Body Type": body_types, 
    "CO2 Emissions (g/km)": co2s
}

# Create DataFrame from the dictionary
carsData = pd.DataFrame(carsDict)

# Export pre-cleaned data as CSV
carsData.to_csv(r'/data/raw_webscraping_output', index=False)

# Create a copy of the original webscrape file for backup
carsData_unclean = carsData.copy()

# Data Cleaning

# Clean 'Price' column by removing currency symbol and commas, then convert to integer
carsData["Price"] = carsData["Price"].str.replace("£", "").str.replace(",", "").astype("int32")

# Convert 'Number of Reviews' column to integer, replacing nulls with 0
carsData["Number of Reviews"] = pd.to_numeric(carsData["Number of Reviews"], errors='coerce').fillna(0).astype("int32")

# Clean 'Mileage' column by removing commas and converting to integer
carsData["Mileage"] = pd.to_numeric(carsData["Mileage"].str.replace(",", ""), errors='coerce').fillna(0).astype(int)

# Clean 'CO2 Emissions' column by removing unit and converting to integer
carsData["CO2 Emissions"] = pd.to_numeric(carsData["CO2 Emissions"].str.replace(" g/km", ""), errors='coerce').fillna(0).astype(int)

# Convert 'Year' column to integer and handle any null values
carsData["Year"] = pd.to_datetime(carsData["Year"], format='%Y', errors='coerce').dt.strftime('%Y')

# Convert 'Number of Doors' column to integer
carsData["Number of Doors"] = pd.to_numeric(carsData["Number of Doors"], errors='coerce').fillna(0).astype(int)

# Clean 'Location/Distance' column by converting units to miles
carsData[['Location/Distance', 'Distance Metric']] = carsData['Location/Distance'].str.split(' ', n=1, expand=True)
carsData["Location/Distance"] = pd.to_numeric(carsData['Location/Distance'], errors='coerce').fillna(0).astype(int)
carsData['Location/Distance'] = np.where(carsData['Distance Metric'] == 'yards', carsData['Location/Distance'] / 1760, carsData['Location/Distance']).round(1)

# Drop 'Distance Metric' as it is no longer needed
carsData = carsData.drop(['Distance Metric'], axis=1)

# Rename columns for better clarity
carsData = carsData.rename(columns={
    "Price": "Price (£)", 
    "CO2 Emissions": "CO2 Emissions (g/km)", 
    "Location/Distance": "Location/Distance (Miles)"
})

# Export the cleaned data to CSV
carsData.to_csv(r'/data/car_clean_output', index=False)

# Data Analysis

# Plot Car Sales by Year
sales_per_year = carsData.groupby('Year').size().reset_index(name='Sales Count')
sales_per_year = sales_per_year[sales_per_year['Year'] != 0]

plt.plot(sales_per_year['Year'], sales_per_year['Sales Count'])
plt.title('Car Sales by Year')
plt.xlabel('Year')
plt.ylabel('Car Sales')
plt.xticks(sales_per_year['Year'][::2], sales_per_year['Year'][::2], rotation=45, ha='right')
plt.show()

# Export the sales per year data
sales_per_year.to_csv(r'/data/car_sales.csv', index=False)

# Plot Car Sales by Transmission Type
sales_by_transmission = carsData.groupby('Transmissions').size().reset_index(name='Sales Count')
sales_by_transmission = sales_by_transmission[sales_by_transmission['Transmissions'] != 0].sort_values('Sales Count')

plt.bar(sales_by_transmission['Transmissions'], sales_by_transmission['Sales Count'])
plt.title('Car Sales per Transmission')
plt.xlabel('Transmission')
plt.ylabel('Car Sales')
plt.show()

# Export the sales by transmission data
sales_by_transmission.to_csv(r'/car_sales_transmission.csv', index=False)

# Plot Car Sales by Body Type
sales_by_bodytype = carsData.groupby('Body Type').size().reset_index(name='Sales Count')
sales_by_bodytype = sales_by_bodytype[sales_by_bodytype['Body Type'] != 0].sort_values('Sales Count')

plt.bar(sales_by_bodytype['Body Type'], sales_by_bodytype['Sales Count'])
plt.title('Car Sales per Body Type')
plt.xlabel('Body Type')
plt.ylabel('Car Sales')
plt.show()

# Export the sales by body type data
sales_by_bodytype.to_csv(r'/data/car_sales_body_type.csv', index=False)

# Q2f: Calculate Top 10 Cars by Number of Reviews
top_10_cars_review_count = carsData.groupby('Sales Title')['Number of Reviews'].mean().reset_index(name='Number of Reviews').sort_values('Number of Reviews', ascending=False).head(10)

# Export the top 10 cars by review count
top_10_cars_review_count.to_csv(r'/data/car_top_review_count.csv', index=False)


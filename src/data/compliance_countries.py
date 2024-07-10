import pandas as pd
from geopy.geocoders import Nominatim
import pycountry

# Import the entire fda_compliance_actions dataset
compliance_countries = pd.read_csv("src/data/fda_compliance_actions.csv")

# Initialize the geocoder
geolocator = Nominatim(user_agent="my_agent")

# Function to get coordinates
def get_coordinates(country):
    try:
        location = geolocator.geocode(country)
        return location.latitude, location.longitude
    except:
        return None, None

# Function to normalize country names
def normalize_country_name(name):
    try:
        return pycountry.countries.search_fuzzy(name)[0].name
    except:
        return name

# Normalize country names
compliance_countries['Country'] = compliance_countries['Country/Area'].apply(normalize_country_name)

# Group by normalized country names and count compliance actions
compliance_countries = compliance_countries.groupby("Country").size().reset_index(name="Count")

# Add latitude and longitude columns
compliance_countries['latitude'], compliance_countries['longitude'] = zip(*compliance_countries['Country'].apply(get_coordinates))

# Sort by Count in descending order
compliance_countries = compliance_countries.sort_values("Count", ascending=False)

# Calculate total compliance actions
total_actions = compliance_countries['Count'].sum()

# Add a column for percentage of total
compliance_countries['Percentage'] = (compliance_countries['Count'] / total_actions) * 100

# Ensure Count is integer
compliance_countries['Count'] = compliance_countries['Count'].astype(int)

# Add ISO country code
def get_country_code(country_name):
    try:
        return pycountry.countries.search_fuzzy(country_name)[0].alpha_3
    except:
        return None

compliance_countries['ISO_Code'] = compliance_countries['Country'].apply(get_country_code)

# Write to CSV
compliance_countries.to_csv("compliance_countries.csv", index=False)
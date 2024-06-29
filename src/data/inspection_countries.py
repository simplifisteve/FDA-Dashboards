import pandas as pd 
import sys

# Import the entire fda_inspections dataset
fda_inspections = pd.DataFrame(pd.read_csv("src/fda_inspections.csv"))

# Filter dataset to include: Biologics, Drugs, Devices
fda_inspections = fda_inspections[fda_inspections["Product Type"].isin(["Biologics", "Drugs", "Devices"])]

# Domestic Inspections Count
domestic = fda_inspections[fda_inspections["Country/Area"] == "United States"].groupby("Fiscal Year").size()
domestic = domestic.reset_index()
domestic.columns = ["Fiscal Year", "Count"]

# Foreign Inspections Count
foreign = fda_inspections[fda_inspections["Country/Area"] != "United States"].groupby("Fiscal Year").size()
foreign = foreign.reset_index()
foreign.columns = ["Fiscal Year", "Count"]

# Merge domestic_us and foreign_count to create merged_inspection_counts
merged_inspection_counts = pd.merge(domestic, foreign, on='Fiscal Year', how='outer')
merged_inspection_counts.columns = ['Fiscal Year', 'Domestic', 'Foreign']

# Replace NaN with 0
merged_inspection_counts = merged_inspection_counts.fillna(0)

# Write to CSV
merged_inspection_counts.to_csv(sys.stdout, index=False)
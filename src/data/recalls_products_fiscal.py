import pandas as pd 
import sys

# Import the entire fda_recalls dataset
fda_recalls = pd.DataFrame(pd.read_csv("src/data/fda_recalls.csv"))

# Extract Year value from Center Classification Date
fda_recalls['Fiscal Year'] = pd.to_datetime(fda_recalls['Center Classification Date']).dt.year

# Recalled Products by Fiscal Year
recalls_fiscal = fda_recalls.groupby(["Fiscal Year", "Product Type"]).size().reset_index()
recalls_fiscal.columns = ["Fiscal Year", "Product Type", "Count"]

# Write to CSV
recalls_fiscal.to_csv("recalls_fiscal.csv", index=False)
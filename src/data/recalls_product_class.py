import pandas as pd 
import sys

# Import the entire fda_recalls dataset
fda_recalls = pd.DataFrame(pd.read_csv("src/data/fda_recalls.csv"))

# Extract Year value from Center Classification Date
fda_recalls['Fiscal Year'] = pd.to_datetime(fda_recalls['Center Classification Date']).dt.year

# Recalled Products by Classification
recalls_product_class = fda_recalls.groupby(["Fiscal Year", "Product Classification"]).size().reset_index()
recalls_product_class.columns = ["Fiscal Year", "Product Classification", "Total"]

# Write to CSV
recalls_product_class.to_csv("recalls_product_class.csv", index=False)
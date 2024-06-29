import pandas as pd 
import sys

# Import the entire fda_inspections dataset
fda_inspections = pd.DataFrame(pd.read_csv("src/fda_inspections.csv"))

# Filter dataset to include: Biologics, Drugs, Devices
fda_inspections = fda_inspections[fda_inspections["Product Type"].isin(["Biologics", "Drugs", "Devices"])]

# Inspection Classification by Product Type
class_product = fda_inspections.groupby(["Fiscal Year", "Product Type"]).size().reset_index()
class_product.columns = ["Fiscal Year", "Product Type", "Total"]

# Write to CSV
class_product.to_csv(sys.stdout, index=False)
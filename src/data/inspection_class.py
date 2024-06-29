import pandas as pd 
import sys

# Import the entire fda_inspections dataset
fda_inspections = pd.DataFrame(pd.read_csv("src/fda_inspections.csv"))

# Filter dataset to include: Biologics, Drugs, Devices
fda_inspections = fda_inspections[fda_inspections["Product Type"].isin(["Biologics", "Drugs", "Devices"])]

# Inspection Classification by Fiscal Year
class_fiscal = fda_inspections.groupby(["Fiscal Year", "Classification"]).size().reset_index()
class_fiscal.columns = ["Fiscal Year", "Classification", "Count"]

# Write to CSV
class_fiscal.to_csv(sys.stdout, index=False)
import pandas as pd 
import sys

# Import the entire fda_compliance_actions dataset
compliance_products = pd.DataFrame(pd.read_csv("src/data/fda_compliance_actions.csv"))

# Filter dataset to only include Injunctions & Seizures
compliance_products = compliance_products[compliance_products['Action Type'].isin(['Injunction', 'Seizure'])]

# Compliance Actions by Product Type
compliance_products = compliance_products.groupby(["Product Type", "Action Type"])['Case/Injunction ID'].nunique().reset_index()
compliance_products.columns = ["Product Type", "Action Type", "Total"]

# Write to CSV
compliance_products.to_csv("compliance_products.csv", index=False)
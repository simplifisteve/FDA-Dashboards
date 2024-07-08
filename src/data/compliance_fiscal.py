import pandas as pd 
import sys

# Import the entire fda_compliance_actions dataset
compliance_fiscal = pd.DataFrame(pd.read_csv("src/data/fda_compliance_actions.csv"))

# Filter dataset to only include Injunctions & Seizures
compliance_fiscal = compliance_fiscal[compliance_fiscal['Action Type'].isin(['Injunction', 'Seizure'])]

# Extract Year value from Action Taken Date
compliance_fiscal['Fiscal Year'] = pd.to_datetime(compliance_fiscal['Action Taken Date']).dt.year

# Compliance Actions by Fiscal Year
compliance_fiscal = compliance_fiscal.groupby(["Fiscal Year", "Action Type"])['Case/Injunction ID'].nunique().reset_index()
compliance_fiscal.columns = ["Fiscal Year", "Action Type", "Total"]

# Write to CSV
compliance_fiscal.to_csv("compliance_fiscal.csv", index=False)
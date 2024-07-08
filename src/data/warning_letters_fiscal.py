import pandas as pd 
import sys

# Import the entire fda_compliance_actions dataset
fda_compliance_actions = pd.DataFrame(pd.read_csv("src/data/fda_compliance_actions.csv"))

# Extract Year value from Action Taken Date
fda_compliance_actions['Fiscal Year'] = pd.to_datetime(fda_compliance_actions['Action Taken Date']).dt.year

# Warning Letters by Fiscal Year
warning_letters_fiscal = fda_compliance_actions.groupby(["Fiscal Year", "Product Type"])['Case/Injunction ID'].nunique().reset_index()
warning_letters_fiscal.columns = ["Fiscal Year", "Product Type", "Total"]

# Write to CSV
warning_letters_fiscal.to_csv("warning_letters_fiscal.csv", index=False)
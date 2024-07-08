import pandas as pd 
import sys

# Import the entire fda_recalls dataset
fda_recalls = pd.DataFrame(pd.read_csv("src/data/fda_recalls.csv"))

# Extract Year value from Center Classification Date
fda_recalls['Fiscal Year'] = pd.to_datetime(fda_recalls['Center Classification Date']).dt.year

# Recalled Events by Fiscal Year
recalls_events_fiscal = fda_recalls.groupby(["Fiscal Year", "Event Classification"])['Event ID'].nunique().reset_index()
recalls_events_fiscal.columns = ["Fiscal Year", "Event Classification", "Total"]

# Write to CSV
recalls_events_fiscal.to_csv("recalls_events_fiscal.csv", index=False)
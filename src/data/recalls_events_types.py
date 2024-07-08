import pandas as pd 
import sys

# Import the entire fda_recalls dataset
fda_recalls = pd.DataFrame(pd.read_csv("src/data/fda_recalls.csv"))

# Recalled Events by Product Type
recalls_events_types = fda_recalls.groupby(["Product Type", "Event Classification"])["Event ID"].nunique().reset_index()
recalls_events_types.columns = ["Product Type", "Event Classification", "Total"]

# Write to CSV
recalls_events_types.to_csv("recalls_events_types.csv", index=False)
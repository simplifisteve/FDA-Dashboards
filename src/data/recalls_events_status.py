import pandas as pd 
import sys

# Import the entire fda_recalls dataset
fda_recalls = pd.DataFrame(pd.read_csv("src/data/fda_recalls.csv"))

# Recalled Events by Status
recalls_events_status = fda_recalls.groupby("Status")["Event ID"].nunique().reset_index()
recalls_events_status.columns = ["Status", "Total"]

# Write to CSV
recalls_events_status.to_csv("recalls_events_status.csv", index=False)
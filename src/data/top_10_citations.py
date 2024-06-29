import pandas as pd
import sys

# Import the entire fda_citations dataset
fda_citations = pd.DataFrame(pd.read_csv("src/fda_citations.csv"))

# Filter dataset to only include: Biologics, Drugs, Devices
fda_citations = fda_citations[fda_citations["Program Area"].isin(["Biologics", "Drugs", "Devices"])]

# Top 10 Citations
top_10_citations = fda_citations.groupby(["Act/CFR Number", "Short Description"])["FEI Number"].count().nlargest(10)

# Convert the series 'top_10_citations' into a DataFrame and reset the index
top_10_citations_table = top_10_citations.reset_index()

# Rename the 'FEI Number' column to Total
top_10_citations_table.rename(columns = {'FEI Number' : 'Total'}, inplace = True)

# Write to CSV
top_10_citations_table.to_csv("top_10_citations_table.csv", index=False)

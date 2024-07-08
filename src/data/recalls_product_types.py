import pandas as pd 
import sys

# Import the entire fda_recalls dataset
fda_recalls = pd.DataFrame(pd.read_csv("src/data/fda_recalls.csv"))

# Recalled Products by Product Type
recalls_product_types = fda_recalls.groupby("Product Type")["Product ID"].nunique().reset_index()
recalls_product_types.columns = ["Product Type", "Total"]

# Write to CSV
recalls_product_types.to_csv("recalls_product_types.csv", index=False)
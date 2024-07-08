import pandas as pd 
import sys
import us

# Import the entire fda_inspections dataset
fda_inspections = pd.DataFrame(pd.read_csv("data/fda_inspections.csv"))

# Filter dataset to include: Biologics, Drugs, Devices
fda_inspections = fda_inspections[fda_inspections["Product Type"].isin(["Biologics", "Drugs", "Devices"])]

# Count of Inspections by State
inspections_state = fda_inspections.groupby("State").size().reset_index()
inspections_state.columns = ["State", "Total"]

# Order the 'Count' column in descending order
inspections_state = inspections_state.sort_values('Total', ascending=False, ignore_index=True)

# Fill missing state names with "No State"
inspections_state['State'] = inspections_state['State'].fillna('No State')

# Update rows where State is a dash
inspections_state.loc[inspections_state['State'] == '-', 'State'] = "No State"

# Function to convert state name to state code
def get_state_code(state_name):
    try:
        return us.states.lookup(state_name).abbr
    except AttributeError:
        return None

inspections_state['State_Code'] = inspections_state['State'].apply(get_state_code)

# Remove any rows where State is "No State" and Total is "20194"
condition = (inspections_state['State'] == 'No State') & (inspections_state['Total'] == 20194)
if condition.sum() > 0:
    remove_index = inspections_state[condition].index[0]
    inspections_state = inspections_state.drop(remove_index)

# Write to CSV
inspections_state.to_csv("inspections_state.csv", index=False)
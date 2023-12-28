import pandas as pd



df = pd.read_excel("testfile.xls",header=2)

df['Item List'] = df['Item List'].astype(str)
df['LaborExt\n(sec)'] = df['LaborExt\n(sec)'].astype(str)


seen_items_columnA = set()
column_a = []
column_b = []
labor_values = []

for index, row in df.iterrows():
    item = row['Item List']
    labor = row['LaborExt\n(sec)']

    # Check if the item starts with "C" and does not have leading spaces
    if item.startswith("C") and not item.startswith(" "):
        # Check if we've seen this item before
        if item not in seen_items_columnA:
            seen_items_columnA.add(item)
            column_a.append(item)
            column_b.append('')  # Append an empty string to maintain alignment in column B
            labor_values.append("")  # Append the labor value
        # If we have seen it, don't append to column A or labor, but append an empty string to maintain alignment
        else:
            column_a.append('')
            labor_values.append('')
            column_b.append('')

    # Check if the item has exactly three leading spaces
    elif item.startswith("   ") and not item.startswith("    "):
        column_a.append('')  # Append an empty string to maintain alignment in column A
        column_b.append(item.lstrip())  # Remove leading spaces and append to column B
        labor_values.append(labor)  # Append the labor value

# Create a new DataFrame from the lists
final_df = pd.DataFrame({'Column A': column_a, 'Column B': column_b, 'Labor Values': labor_values})

# Filter out rows where both 'Column A' and 'Column B' are empty strings
filtered_df = final_df[(final_df['Column A'] != '') | (final_df['Column B'] != '')]

# Reset the index of the resulting DataFrame
df = filtered_df.reset_index(drop=True)








df['Labor Values'] = pd.to_numeric(df['Labor Values'], errors='coerce')
# Group by 'Column B' and sum 'Labor Values'
labor_sum_df = df.groupby('Column B')['Labor Values'].sum().reset_index()



final_df = pd.DataFrame(columns=['Column A', 'Column B', 'Labor Values'])


# Track the unique values in 'Column B' that have been processed
seen_items_columnB = set()


# Iterate through the original DataFrame
for index, row in df.iterrows():
    # Check if the value in 'Column B' is unique and has not been processed
    if row['Column B'] not in seen_items_columnB:
        # Add the unique value to the processed set
        seen_items_columnB.add(row['Column B'])

        # Find the corresponding labor sum
        labor_sum = labor_sum_df.loc[labor_sum_df['Column B'] == row['Column B'], 'Labor Values'].iloc[0]

        # Append the row to the final DataFrame
        final_df = final_df._append({'Column A': row['Column A'], 
                                    'Column B': row['Column B'], 
                                    'Labor Values': labor_sum}, ignore_index=True)
    else:
        # For already processed 'Column B' values, append only 'Column A'
        final_df = final_df._append({'Column A': row['Column A'], 
                                    'Column B': '', 
                                    'Labor Values': ''}, ignore_index=True)




# Filter out rows where both 'Column A' and 'Column B' are empty strings
filtered_df = final_df[(final_df['Column A'] != '') | (final_df['Column B'] != '')]

# Reset the index of the resulting DataFrame
df = filtered_df.reset_index(drop=True)

# Display the filtered DataFrame
print(df)



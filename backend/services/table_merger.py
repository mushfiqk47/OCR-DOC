import pandas as pd

def merge_tables(tables: list[pd.DataFrame]) -> list[pd.DataFrame]:
    """
    Merges a list of DataFrames based on header similarity.
    Useful for reconstructing multi-page tables.
    """
    if not tables:
        return []

    merged_tables = []
    current_master = tables[0]

    for i in range(1, len(tables)):
        next_table = tables[i]
        
        # Scenario A: Exact Header Match (Continuation with repeated header)
        if list(current_master.columns) == list(next_table.columns):
            current_master = pd.concat([current_master, next_table], ignore_index=True)
        
        # Scenario B: Column Count Match (Continuation without header, or different header names but same structure)
        # This is risky. We only do this if the column count is identical.
        elif len(current_master.columns) == len(next_table.columns):
             # Assume next_table lacks proper header or has garbage header
             # We align syntax: assign master columns to next_table
             next_table.columns = current_master.columns
             current_master = pd.concat([current_master, next_table], ignore_index=True)
        
        # Scenario C: Mismatch -> New Table
        else:
            merged_tables.append(current_master)
            current_master = next_table

    merged_tables.append(current_master)
    return merged_tables

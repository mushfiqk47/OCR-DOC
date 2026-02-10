import pandas as pd
import io
from openpyxl.utils import get_column_letter

def dataframes_to_excel(dfs: list[pd.DataFrame], sheet_names: list[str] = None) -> bytes:
    """
    Writes a list of DataFrames to an Excel file in memory.
    """
    output = io.BytesIO()
    
    # Create Excel writer object
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for i, df in enumerate(dfs):
            sheet_name = f"Table {i+1}"
            if sheet_names and i < len(sheet_names):
                 sheet_name = sheet_names[i]
            
            # Write DF to sheet
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets[sheet_name]
            for idx, col in enumerate(worksheet.columns):
                max_length = 0
                column = get_column_letter(idx + 1) # Get the column name
                # iterating through each cell in the column
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column].width = adjusted_width

    return output.getvalue()

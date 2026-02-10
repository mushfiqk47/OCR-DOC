import pandas as pd
import io
import re

def parse_markdown_tables(md_text: str) -> list[pd.DataFrame]:
    """
    Extracts Markdown tables from text and converts them to DataFrames.
    Handlers standard pipe-separated tables.
    """
    tables = []
    lines = md_text.split('\n')
    current_table_lines = []
    in_table = False

    for line in lines:
        stripped = line.strip()
        # Simple heuristic: a table line starts and ends with |
        if stripped.startswith('|') and stripped.endswith('|'):
            # Check if it's a separator line (e.g., |---|---|)
            if re.match(r'^\|[\s-:]+(\|[\s-:]+)+\|$', stripped):
                if not in_table:
                    # If we hit a separator but weren't "in" a table, the previous line was likely the header
                    # But if we are accumulating, we just skip this line as pandas handles headers
                    pass
                continue
            
            in_table = True
            current_table_lines.append(stripped)
        else:
            if in_table:
                # Table ended
                if current_table_lines:
                    try:
                        df = _convert_lines_to_df(current_table_lines)
                        if not df.empty:
                            tables.append(df)
                    except Exception as e:
                        print(f"Failed to parse table block: {e}")
                current_table_lines = []
                in_table = False

    # Handle case where text ends with a table
    if in_table and current_table_lines:
         try:
            df = _convert_lines_to_df(current_table_lines)
            if not df.empty:
                tables.append(df)
         except Exception as e:
            print(f"Failed to parse table block: {e}")

    return tables

def _convert_lines_to_df(lines: list[str]) -> pd.DataFrame:
    # Join lines and use pandas to read
    # We strip outer pipes manually to avoid empty first/last columns if pandas read_csv separator is strict
    cleaned_lines = []
    for line in lines:
        # Remove leading/trailing pipes
        content = line.strip('|')
        cleaned_lines.append(content)
    
    data_str = "\n".join(cleaned_lines)
    # Use | as separator
    try:
        df = pd.read_csv(io.StringIO(data_str), sep="|", engine="python")
        # Clean column names (strip whitespace)
        df.columns = df.columns.str.strip()
        # Clean string data
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        # Drop empty columns (often resulting from extra pipes)
        df = df.dropna(axis=1, how='all')
        return df
    except pd.errors.EmptyDataError:
        return pd.DataFrame()

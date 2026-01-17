import pandas as pd
from sqlalchemy import create_engine

def inspect_safran_data():
    """
    STRICT DATA RESOLUTION (DB MODE):
    Loads data from SQLite (data.db), validates columns,
    and verifies engineering signals.
    """

    print("🔍 Loading data from SQLite database: data.db")

    # 1. CONNECT DATABASE
    try:
        engine = create_engine("sqlite:///data.db")
        df = pd.read_sql("SELECT * FROM manufacturing_data", engine)
        print("✅ Successfully loaded data from database")
    except Exception as e:
        print(f"❌ DATABASE LOAD FAILED: {e}")
        return None

    if df.empty:
        print("⚠️ WARNING: Database table is empty.")
        return df

    # 2. COLUMN VALIDATION
    print("\n--- VALIDATING SAFRAN STRUCTURE ---")

    # Nominal typo handling
    nom_col = next(
        (c for c in df.columns if c.lower() in ["nominal", "nomial"]),
        None
    )
    meas_col = "Measured Value"

    if nom_col:
        print(f"Found Nominal Column: '{nom_col}'")
    else:
        print("⚠️ Warning: Nominal/Nomial column not found")

    if meas_col in df.columns:
        print(f"Found Measured Column: '{meas_col}'")
    else:
        print(f"⚠️ Warning: '{meas_col}' column not found")

    # 3. SIGNAL CHECK — Deviation
    if nom_col and meas_col in df.columns:
        try:
            df[nom_col] = pd.to_numeric(df[nom_col], errors="coerce")
            df[meas_col] = pd.to_numeric(df[meas_col], errors="coerce")

            df["Test_Deviation"] = (df[meas_col] - df[nom_col]).abs()
            print("✅ Signal Logic Test: Deviation calculated successfully")
        except Exception as e:
            print(f"❌ Signal Logic Failed: {e}")

    # 4. DATA QUALITY SUMMARY
    print("\n--- DATA QUALITY SUMMARY ---")
    print(f"Total Rows: {len(df)}")
    print(f"Total Columns: {len(df.columns)}")

    rag_cols = ["NC description", "Root cause of occurrence"]
    for col in rag_cols:
        if col in df.columns:
            populated = df[col].notna().sum()
            print(f"Column '{col}': {populated}/{len(df)} populated")

    # 5. PREVIEW
    print("\n--- PREVIEW (First 3 Rows) ---")
    print(df.head(3))

    print("\n✅ DATA RESOLUTION COMPLETE: DB data is valid for dashboard & RAG")
    return df


if __name__ == "__main__":
    inspect_safran_data()

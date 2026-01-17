import pandas as pd
import numpy as np
import os
import time
from http import HTTPStatus

# --- 数据加载 & 信号计算 ---
def resolve_and_load_data():
    """
    Load data from data.db or local CSV/XLSX and calculate Deviation.
    Here we simulate CSV/XLSX fallback for compatibility.
    """
    import sqlite3

    db_path = "data.db"
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database '{db_path}' not found!")

    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query("SELECT * FROM manufacturing_data", conn)
    finally:
        conn.close()

    # Calculate Deviation if relevant columns exist
    nom_col = next((c for c in df.columns if c.lower() in ['nominal', 'nomial']), None)
    meas_col = 'Measured Value'
    if nom_col and meas_col in df.columns:
        df[nom_col] = pd.to_numeric(df[nom_col], errors='coerce').fillna(0)
        df[meas_col] = pd.to_numeric(df[meas_col], errors='coerce').fillna(0)
        df['Deviation'] = (df[meas_col] - df[nom_col]).abs()

    # Clean text columns for RAG
    cols_to_clean = ['Part type', 'NC description', 'Root cause of occurrence', 
                     'Corrective actions', 'Job order']
    for col in cols_to_clean:
        if col in df.columns:
            df[col] = df[col].fillna('N/A').astype(str)

    return df

# --- RAG 模拟分析 ---
def run_rag_investigation(target_id, df):
    """
    Simulated Sentinel RAG:
    Embedding is replaced by random vectors to avoid torch/Win DLL issues.
    """
    perf_metrics = {}
    total_start = time.time()

    target_row = df[df['Job order'] == target_id]
    if target_row.empty:
        return f"❌ Error: Job ID '{target_id}' not found."

    target_row = target_row.iloc[0]
    query_text = target_row['NC description']

    print("\n" + "—"*80)
    print(f"📍 INITIATING INVESTIGATION: Job #{target_id}")
    print(f"🔎 SYMPTOM: {query_text}")
    print("—"*80)

    # --- Step 1: Retrieval (Randomized simulation instead of embedding) ---
    print("\n[STEP 1: CONSULTING ARCHIVES]")
    np.random.seed(42)
    sims = np.random.rand(len(df))
    top_indices = sims.argsort()[-4:][::-1]

    history_context = ""
    source_ids = []
    top_confidence = 0
    cases_found = 0

    print("\n--- 📖 RAW EVIDENCE FROM ARCHIVE (SIMULATED) ---")
    for idx in top_indices:
        row = df.iloc[idx]
        if row['Job order'] == target_id: 
            continue
        if cases_found >= 3: 
            break

        if cases_found == 0: top_confidence = sims[idx]

        print(f"▶ Historical Record {row['Job order']}:")
        print(f"  Cause: {row['Root cause of occurrence']}")
        print(f"  Fix:   {row['Corrective actions']}")
        print("-"*40)

        history_context += f"Case {row['Job order']}: Cause was {row['Root cause of occurrence']}. Fix was {row['Corrective actions']}.\n"
        source_ids.append(row['Job order'])
        cases_f_

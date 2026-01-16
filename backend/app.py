"""
Industrial Detective - Backend API
Provides data analysis and root cause analysis services
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine, text

# Import analysis modules
from analysis import DataAnalyzer, RootCauseAnalyzer
from ml_models import CorrelationDetector, AnomalyDetector

app = Flask(__name__)
CORS(app)

# Global variables to store data and analyzers
data_analyzer = None
root_cause_analyzer = None
correlation_detector = None
anomaly_detector = None

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

engine = create_engine('sqlite:///data.db')

# 允许的列
REQUIRED_COLUMNS = [
    'timestamp', 'production_line', 'machine_id', 'operator_id',
    'temperature', 'pressure', 'vibration', 'quality_score',
    'defect_count', 'ncr_type', 'severity', 'shift', 'material_batch'
]

# RAG 分级阈值
RAG_THRESHOLDS = {
    'defect_count': {'R': 5, 'A': 3}  # >5 红，>3 黄，<=3 绿
}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_data():
    """Load Excel data"""
    global data_analyzer, root_cause_analyzer, correlation_detector, anomaly_detector
    
    # Try loading data from different paths
    data_paths = [
        '../../Master Data for Hackathon .xlsx',
        '../Master Data for Hackathon .xlsx',
        './data/Master Data for Hackathon .xlsx'
    ]
    
    df = None
    for path in data_paths:
        if os.path.exists(path):
            try:
                df = pd.read_excel(path)
                print(f"Successfully loaded data: {path}")
                print(f"Data shape: {df.shape}")
                print(f"Column names: {df.columns.tolist()}")
                break
            except Exception as e:
                print(f"Failed to load {path}: {e}")
                continue
    
    if df is None:
       return None
    
    # Initialize analyzers
    data_analyzer = DataAnalyzer(df)
    root_cause_analyzer = RootCauseAnalyzer(df)
    correlation_detector = CorrelationDetector(df)
    anomaly_detector = AnomalyDetector(df)
    
    return df

def serialize_anomalies(anomalies):
    if isinstance(anomalies, pd.DataFrame):
        return anomalies.applymap(lambda x: x.isoformat() if isinstance(x, (pd.Timestamp, datetime, time)) else x).to_dict(orient='records')
    elif isinstance(anomalies, list):
        def serialize_obj(obj):
            if isinstance(obj, dict):
                return {k: (v.isoformat() if isinstance(v, (pd.Timestamp, datetime, time)) else v) for k, v in obj.items()}
            return obj
        return [serialize_obj(a) for a in anomalies]
    else:
        return anomalies     

def create_sample_data():
    """Create sample manufacturing data"""
    np.random.seed(42)
    n_records = 1000
    
    dates = pd.date_range(start='2024-01-01', periods=n_records, freq='H')
    
    data = {
        'timestamp': dates,
        'production_line': np.random.choice(['Line A', 'Line B', 'Line C'], n_records),
        'machine_id': np.random.choice(['M001', 'M002', 'M003', 'M004'], n_records),
        'operator_id': np.random.choice(['OP01', 'OP02', 'OP03'], n_records),
        'temperature': np.random.normal(75, 5, n_records),
        'pressure': np.random.normal(100, 10, n_records),
        'vibration': np.random.normal(50, 8, n_records),
        'quality_score': np.random.normal(95, 5, n_records),
        'defect_count': np.random.poisson(2, n_records),
        'ncr_type': np.random.choice(['Dimensional', 'Surface', 'Material', 'Assembly'], n_records, p=[0.3, 0.3, 0.2, 0.2]),
        'severity': np.random.choice(['Low', 'Medium', 'High', 'Critical'], n_records, p=[0.4, 0.3, 0.2, 0.1]),
        'shift': np.random.choice(['Day', 'Night'], n_records),
        'material_batch': np.random.choice([f'BATCH_{i:03d}' for i in range(1, 51)], n_records),
    }
    
    # Add some correlations
    data['defect_count'] = np.maximum(0, data['defect_count'] + 
                                      (data['temperature'] > 80).astype(int) * 2 +
                                      (data['vibration'] > 60).astype(int) * 1)
    
    return pd.DataFrame(data)

@app.route('/api/clear-data', methods=['POST'])
def clear_data():
    try:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM manufacturing_data"))
        return jsonify({'status': 'success', 'message': 'All data cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-excel', methods=['POST'])
def upload_excel():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400
    
    try:
        df = pd.read_excel(file)

        # 补全缺失列
        for col in REQUIRED_COLUMNS:
            if col not in df.columns:
                df[col] = None

        # 确保时间列为 datetime
        if df['timestamp'].dtype != 'datetime64[ns]':
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

        # 存入 SQLite
        df.to_sql('manufacturing_data', engine, if_exists='replace', index=False)

        return jsonify({'status': 'success', 'rows': len(df)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/data/overview', methods=['GET'])
def get_data_overview():
    """Get data overview"""
    if data_analyzer is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    overview = data_analyzer.get_overview()
    return jsonify(overview)

@app.route('/api/data/columns', methods=['GET'])
def get_columns():
    """Get data column information"""
    if data_analyzer is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    columns = data_analyzer.get_columns_info()
    return jsonify(columns)

@app.route('/api/data/sample', methods=['GET'])
def get_sample_data():
    """Get sample data"""
    if data_analyzer is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    limit = request.args.get('limit', 100, type=int)
    sample = data_analyzer.get_sample(limit)
    return jsonify(sample)

@app.route('/api/analysis/correlations', methods=['GET'])
def get_correlations():
    """Get correlation analysis"""
    if correlation_detector is None:
        return jsonify({'error': 'Analyzer not initialized'}), 500
    
    threshold = request.args.get('threshold', 0.5, type=float)
    correlations = correlation_detector.get_correlations(threshold)
    return jsonify(correlations)

@app.route('/api/analysis/anomalies', methods=['GET'])
def get_anomalies():
    if anomaly_detector is None:
        return jsonify({'error': 'Analyzer not initialized'}), 500
    
    limit = request.args.get('limit', 50, type=int)
    anomalies = anomaly_detector.detect_anomalies(limit)
    anomalies_serializable = serialize_anomalies(anomalies)
    return jsonify(anomalies_serializable)

@app.route('/api/analysis/root-cause', methods=['POST'])
def analyze_root_cause():
    """Root cause analysis"""
    if root_cause_analyzer is None:
        return jsonify({'error': 'Analyzer not initialized'}), 500
    
    data = request.json
    issue_type = data.get('issue_type')
    filters = data.get('filters', {})
    
    result = root_cause_analyzer.analyze(issue_type, filters)
    return jsonify(result)

@app.route('/api/insights/generate', methods=['POST'])
def generate_insights():
    """Generate insights"""
    if data_analyzer is None or root_cause_analyzer is None:
        return jsonify({'error': 'Analyzer not initialized'}), 500
    
    data = request.json
    filters = data.get('filters', {})
    
    insights = root_cause_analyzer.generate_insights(filters)
    return jsonify(insights)

@app.route('/api/actions/suggest', methods=['POST'])
def suggest_actions():
    """Suggest corrective actions"""
    if root_cause_analyzer is None:
        return jsonify({'error': 'Analyzer not initialized'}), 500
    
    data = request.json
    root_cause = data.get('root_cause')
    issue_type = data.get('issue_type')
    
    actions = root_cause_analyzer.suggest_actions(root_cause, issue_type)
    return jsonify(actions)

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    if data_analyzer is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    stats = data_analyzer.get_dashboard_stats()
    return jsonify(stats)

@app.route('/api/time-series', methods=['GET'])
def get_time_series():
    """Get time series data"""
    if data_analyzer is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    column = request.args.get('column', 'defect_count')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    group_by = request.args.get('group_by', 'hour')  # hour, day, week
    
    time_series = data_analyzer.get_time_series(column, start_date, end_date, group_by)
    return jsonify(time_series)  

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    try:
        df = pd.read_sql('manufacturing_data', engine)

        if df.empty:
            return jsonify({'error': 'No data available'}), 400

        # ---------- 基础清洗 ----------
        df['Date of detection'] = pd.to_datetime(
            df['Date of detection'], errors='coerce'
        )

        today = pd.Timestamp.now().normalize()
        week_ago = today - pd.Timedelta(days=7)

        # ---------- 1. Overview ----------
        total_ncr = len(df)

        today_ncr = df[df['Date of detection'] >= today].shape[0]
        week_ncr = df[df['Date of detection'] >= week_ago].shape[0]

        # 超公差判断
        def is_out_of_tolerance(row):
            try:
                return (
                    row['Measured Value'] < row['Nomial'] + row['FLowerTolerance']
                    or row['Measured Value'] > row['Nomial'] + row['FUpperTolerance']
                )
            except Exception:
                return False

        df['out_of_tolerance'] = df.apply(is_out_of_tolerance, axis=1)
        out_ratio = round(df['out_of_tolerance'].mean(), 2)

        overview = {
            'total_ncr': total_ncr,
            'today_ncr': int(today_ncr),
            'week_ncr': int(week_ncr),
            'out_of_tolerance_ratio': out_ratio
        }

        # ---------- 2. Distribution ----------
        distribution = {
            'by_nc_code': df['NC Code'].value_counts().to_dict(),
            'by_part_type': df['Part type'].value_counts().to_dict(),
            'by_machine': df['MachineNum of detection'].value_counts().to_dict()
        }

        # ---------- 3. Trend ----------
        trend_df = (
            df.dropna(subset=['Date of detection'])
              .groupby(df['Date of detection'].dt.date)
              .size()
              .reset_index(name='count')
        )

        trend = [
            {'date': str(row['Date of detection']), 'count': int(row['count'])}
            for _, row in trend_df.iterrows()
        ]

        # ---------- 4. Quality ----------
        df['deviation'] = df['Measured Value'] - df['Nomial']

        quality = {
            'deviation_distribution': df['deviation']
                .dropna()
                .round(3)
                .to_frame(name='deviation')
                .to_dict(orient='records'),
            'out_of_tolerance_count': int(df['out_of_tolerance'].sum())
        }

        return jsonify({
            'overview': overview,
            'distribution': distribution,
            'trend': trend,
            'quality': quality
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Loading data...")
    load_data()
    print("Data loaded, starting server...")
    app.run(debug=True, host='0.0.0.0', port=5000)

   

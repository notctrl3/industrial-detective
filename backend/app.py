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
        # Create sample data
        print("Data file not found, creating sample data...")
        df = create_sample_data()
    
    # Initialize analyzers
    data_analyzer = DataAnalyzer(df)
    root_cause_analyzer = RootCauseAnalyzer(df)
    correlation_detector = CorrelationDetector(df)
    anomaly_detector = AnomalyDetector(df)
    
    return df

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
    """Get anomaly detection results"""
    if anomaly_detector is None:
        return jsonify({'error': 'Analyzer not initialized'}), 500
    
    limit = request.args.get('limit', 50, type=int)
    anomalies = anomaly_detector.detect_anomalies(limit)
    return jsonify(anomalies)

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

if __name__ == '__main__':
    print("Loading data...")
    load_data()
    print("Data loaded, starting server...")
    app.run(debug=True, host='0.0.0.0', port=5000)

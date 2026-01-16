"""
Machine Learning Models
Provides correlation detection and anomaly detection functionality
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')

class CorrelationDetector:
    """Correlation Detector"""
    
    def __init__(self, df):
        self.df = df.copy()
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    def get_correlations(self, threshold=0.5):
        """Get correlation matrix"""
        if len(self.numeric_cols) < 2:
            return {'correlations': [], 'message': 'Insufficient numeric columns to calculate correlations'}
        
        correlations = []
        corr_matrix = self.df[self.numeric_cols].corr()
        
        # Get upper triangle matrix (avoid duplicates)
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                corr_value = corr_matrix.iloc[i, j]
                
                if abs(corr_value) >= threshold:
                    # Calculate p-value
                    try:
                        p_value = pearsonr(self.df[col1].dropna(), self.df[col2].dropna())[1]
                    except:
                        p_value = None
                    
                    correlations.append({
                        'variable1': col1,
                        'variable2': col2,
                        'correlation': float(corr_value),
                        'abs_correlation': float(abs(corr_value)),
                        'p_value': float(p_value) if p_value else None,
                        'strength': self._get_correlation_strength(abs(corr_value))
                    })
        
        # Sort by absolute correlation
        correlations.sort(key=lambda x: x['abs_correlation'], reverse=True)
        
        return {
            'correlations': correlations,
            'threshold': threshold,
            'total_pairs': len(correlations)
        }
    
    def _get_correlation_strength(self, abs_corr):
        """Get correlation strength description"""
        if abs_corr >= 0.8:
            return 'very_strong'
        elif abs_corr >= 0.6:
            return 'strong'
        elif abs_corr >= 0.4:
            return 'moderate'
        else:
            return 'weak'


class AnomalyDetector:
    """Anomaly Detector"""
    
    def __init__(self, df):
        self.df = df.copy()
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.scaler = StandardScaler()
        self.model = None
        self._train_model()
    
    def _train_model(self):
        """Train anomaly detection model"""
        if len(self.numeric_cols) < 2:
            return
        
        # Prepare data
        X = self.df[self.numeric_cols].fillna(self.df[self.numeric_cols].mean())
        
        # Standardize
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Isolation Forest
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.model.fit(X_scaled)
    
    def detect_anomalies(self, limit=50):
        """Detect anomalies"""
        if self.model is None:
            return {'anomalies': [], 'message': 'Model not trained'}
        
        # Prepare data
        X = self.df[self.numeric_cols].fillna(self.df[self.numeric_cols].mean())
        X_scaled = self.scaler.transform(X)
        
        # Predict
        predictions = self.model.predict(X_scaled)
        anomaly_scores = self.model.score_samples(X_scaled)
        
        # Get anomaly records
        anomaly_indices = np.where(predictions == -1)[0]
        
        anomalies = []
        for idx in anomaly_indices[:limit]:
            record = self.df.iloc[idx].to_dict()
            
            # Convert timestamp
            for key, value in record.items():
                if pd.api.types.is_datetime64_any_dtype(type(value)) or isinstance(value, pd.Timestamp):
                    record[key] = value.isoformat() if hasattr(value, 'isoformat') else str(value)
                elif pd.isna(value):
                    record[key] = None
                elif isinstance(value, (np.integer, np.floating)):
                    record[key] = float(value) if isinstance(value, np.floating) else int(value)
            
            anomalies.append({
                'index': int(idx),
                'anomaly_score': float(anomaly_scores[idx]),
                'data': record
            })
        
        # Sort by anomaly score (lower score = higher anomaly)
        anomalies.sort(key=lambda x: x['anomaly_score'])
        
        return {
            'anomalies': anomalies,
            'total_anomalies': len(anomaly_indices),
            'anomaly_rate': float(len(anomaly_indices) / len(self.df) * 100)
        }
    
    def get_anomaly_features(self, anomaly_index):
        """Get feature analysis for anomaly record"""
        if anomaly_index >= len(self.df):
            return None
        
        record = self.df.iloc[anomaly_index]
        features = {}
        
        for col in self.numeric_cols:
            value = record[col]
            mean = self.df[col].mean()
            std = self.df[col].std()
            
            if not pd.isna(value) and std > 0:
                z_score = (value - mean) / std
                features[col] = {
                    'value': float(value),
                    'mean': float(mean),
                    'std': float(std),
                    'z_score': float(z_score),
                    'is_outlier': abs(z_score) > 2
                }
        
        return features

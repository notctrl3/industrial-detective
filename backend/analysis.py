"""
Data Analysis Module
Provides data overview, statistical analysis, and time series analysis functionality
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter

class DataAnalyzer:
    """Data Analyzer"""
    
    def __init__(self, df):
        self.df = df.copy()
        self._preprocess()
    
    def _preprocess(self):
        """Data preprocessing"""
        # Ensure timestamp column exists
        if 'timestamp' in self.df.columns:
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        elif 'date' in self.df.columns:
            self.df['timestamp'] = pd.to_datetime(self.df['date'])
            self.df['date'] = pd.to_datetime(self.df['date'])
        
        # Identify numeric columns
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
    
    def get_overview(self):
        """Get data overview"""
        return {
            'total_records': len(self.df),
            'total_columns': len(self.df.columns),
            'date_range': {
                'start': self.df['timestamp'].min().isoformat() if 'timestamp' in self.df.columns else None,
                'end': self.df['timestamp'].max().isoformat() if 'timestamp' in self.df.columns else None
            },
            'columns': self.df.columns.tolist(),
            'numeric_columns': self.numeric_cols,
            'categorical_columns': self.categorical_cols,
            'missing_values': self.df.isnull().sum().to_dict()
        }
    
    def get_columns_info(self):
        """Get column information"""
        info = []
        for col in self.df.columns:
            col_info = {
                'name': col,
                'type': str(self.df[col].dtype),
                'null_count': int(self.df[col].isnull().sum()),
                'null_percentage': float(self.df[col].isnull().sum() / len(self.df) * 100)
            }
            
            if col in self.numeric_cols:
                col_info.update({
                    'min': float(self.df[col].min()),
                    'max': float(self.df[col].max()),
                    'mean': float(self.df[col].mean()),
                    'std': float(self.df[col].std()),
                    'median': float(self.df[col].median())
                })
            else:
                unique_values = self.df[col].unique().tolist()
                col_info['unique_count'] = len(unique_values)
                col_info['top_values'] = dict(Counter(self.df[col].dropna()).most_common(10))
            
            info.append(col_info)
        
        return info
    
    def get_sample(self, limit=100):
        """Get sample data"""
        sample_df = self.df.head(limit)
        # Convert timestamp to string
        for col in sample_df.columns:
            if pd.api.types.is_datetime64_any_dtype(sample_df[col]):
                sample_df[col] = sample_df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            'data': sample_df.to_dict('records'),
            'count': len(sample_df)
        }
    
    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        stats = {
            'total_records': len(self.df),
            'date_range': {
                'start': self.df['timestamp'].min().isoformat() if 'timestamp' in self.df.columns else None,
                'end': self.df['timestamp'].max().isoformat() if 'timestamp' in self.df.columns else None
            }
        }
        
        # If defect count exists
        if 'defect_count' in self.df.columns:
            stats['total_defects'] = int(self.df['defect_count'].sum())
            stats['avg_defects'] = float(self.df['defect_count'].mean())
            stats['max_defects'] = int(self.df['defect_count'].max())
        
        # If NCR type exists
        if 'ncr_type' in self.df.columns:
            stats['ncr_distribution'] = dict(Counter(self.df['ncr_type'].dropna()))
        
        # If severity exists
        if 'severity' in self.df.columns:
            stats['severity_distribution'] = dict(Counter(self.df['severity'].dropna()))
        
        # If production line exists
        if 'production_line' in self.df.columns:
            stats['line_distribution'] = dict(Counter(self.df['production_line'].dropna()))
        
        # Calculate statistics for numeric columns
        numeric_stats = {}
        for col in self.numeric_cols[:10]:  # Limit to first 10 numeric columns
            numeric_stats[col] = {
                'mean': float(self.df[col].mean()),
                'std': float(self.df[col].std()),
                'min': float(self.df[col].min()),
                'max': float(self.df[col].max())
            }
        stats['numeric_stats'] = numeric_stats
        
        return stats
    
    def get_time_series(self, column, start_date=None, end_date=None, group_by='hour'):
        """Get time series data"""
        if column not in self.df.columns:
            return {'error': f'Column {column} does not exist'}
        
        if 'timestamp' not in self.df.columns:
            return {'error': 'Timestamp column does not exist'}
        
        # Filter data
        df_filtered = self.df.copy()
        
        if start_date:
            df_filtered = df_filtered[df_filtered['timestamp'] >= pd.to_datetime(start_date)]
        if end_date:
            df_filtered = df_filtered[df_filtered['timestamp'] <= pd.to_datetime(end_date)]
        
        # Group by time
        if group_by == 'hour':
            df_grouped = df_filtered.groupby(df_filtered['timestamp'].dt.floor('H'))
        elif group_by == 'day':
            df_grouped = df_filtered.groupby(df_filtered['timestamp'].dt.date)
        elif group_by == 'week':
            df_grouped = df_filtered.groupby(df_filtered['timestamp'].dt.to_period('W'))
        else:
            df_grouped = df_filtered.groupby(df_filtered['timestamp'].dt.floor('H'))
        
        # Aggregate data
        if column in self.numeric_cols:
            aggregated = df_grouped[column].agg(['mean', 'sum', 'count', 'min', 'max']).reset_index()
        else:
            aggregated = df_grouped[column].agg(['count']).reset_index()
            aggregated['value'] = aggregated['count']
        
        # Convert timestamp
        if group_by == 'day':
            aggregated['timestamp'] = aggregated['timestamp'].astype(str)
        elif group_by == 'week':
            aggregated['timestamp'] = aggregated['timestamp'].astype(str)
        else:
            aggregated['timestamp'] = aggregated['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            'data': aggregated.to_dict('records'),
            'column': column,
            'group_by': group_by
        }


class RootCauseAnalyzer:
    """Root Cause Analyzer"""
    
    def __init__(self, df):
        self.df = df.copy()
        if 'timestamp' in self.df.columns:
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
    
    def analyze(self, issue_type=None, filters=None):
        """Perform root cause analysis"""
        df_filtered = self._apply_filters(filters)
        
        if issue_type:
            if 'ncr_type' in df_filtered.columns:
                df_filtered = df_filtered[df_filtered['ncr_type'] == issue_type]
        
        # Analyze potential root causes
        root_causes = []
        
        # 1. Time pattern analysis
        time_patterns = self._analyze_time_patterns(df_filtered)
        if time_patterns:
            root_causes.append({
                'type': 'time_pattern',
                'description': 'Time Pattern Analysis',
                'findings': time_patterns,
                'confidence': 0.7
            })
        
        # 2. Equipment correlation analysis
        equipment_correlations = self._analyze_equipment_correlations(df_filtered)
        if equipment_correlations:
            root_causes.append({
                'type': 'equipment',
                'description': 'Equipment Correlation Analysis',
                'findings': equipment_correlations,
                'confidence': 0.8
            })
        
        # 3. Operator correlation analysis
        operator_correlations = self._analyze_operator_correlations(df_filtered)
        if operator_correlations:
            root_causes.append({
                'type': 'operator',
                'description': 'Operator Correlation Analysis',
                'findings': operator_correlations,
                'confidence': 0.6
            })
        
        # 4. Environmental factors analysis
        environmental = self._analyze_environmental_factors(df_filtered)
        if environmental:
            root_causes.append({
                'type': 'environmental',
                'description': 'Environmental Factors Analysis',
                'findings': environmental,
                'confidence': 0.75
            })
        
        # Sort root causes by confidence
        root_causes.sort(key=lambda x: x['confidence'], reverse=True)
        
        return {
            'root_causes': root_causes,
            'total_issues': len(df_filtered),
            'analysis_date': datetime.now().isoformat()
        }
    
    def _apply_filters(self, filters):
        """Apply filters"""
        df = self.df.copy()
        
        if not filters:
            return df
        
        if 'start_date' in filters:
            df = df[df['timestamp'] >= pd.to_datetime(filters['start_date'])]
        if 'end_date' in filters:
            df = df[df['timestamp'] <= pd.to_datetime(filters['end_date'])]
        if 'production_line' in filters:
            df = df[df['production_line'] == filters['production_line']]
        if 'severity' in filters:
            df = df[df['severity'] == filters['severity']]
        
        return df
    
    def _analyze_time_patterns(self, df):
        """Analyze time patterns"""
        if 'timestamp' not in df.columns:
            return None
        
        patterns = []
        
        # Analyze by hour
        df['hour'] = df['timestamp'].dt.hour
        hour_counts = df.groupby('hour').size()
        if hour_counts.max() / hour_counts.mean() > 1.5:
            peak_hour = hour_counts.idxmax()
            patterns.append({
                'pattern': f'Issues are more frequent during {peak_hour}:00',
                'evidence': f'Issue count in this period is {hour_counts.max() / hour_counts.mean():.2f}x the average'
            })
        
        # Analyze by shift
        if 'shift' in df.columns:
            shift_counts = df['shift'].value_counts()
            if len(shift_counts) > 1:
                dominant_shift = shift_counts.index[0]
                ratio = shift_counts.iloc[0] / shift_counts.iloc[1]
                if ratio > 1.3:
                    patterns.append({
                        'pattern': f'{dominant_shift} shift has more issues',
                        'evidence': f'Issue count in this shift is {ratio:.2f}x other shifts'
                    })
        
        return patterns
    
    def _analyze_equipment_correlations(self, df):
        """Analyze equipment correlations"""
        if 'machine_id' not in df.columns:
            return None
        
        findings = []
        
        # Equipment failure frequency
        machine_counts = df['machine_id'].value_counts()
        if len(machine_counts) > 1:
            problematic_machine = machine_counts.index[0]
            avg_count = machine_counts.mean()
            if machine_counts.iloc[0] > avg_count * 1.5:
                findings.append({
                    'equipment': problematic_machine,
                    'issue_count': int(machine_counts.iloc[0]),
                    'avg_issue_count': float(avg_count),
                    'ratio': float(machine_counts.iloc[0] / avg_count)
                })
        
        # Equipment-defect correlation
        if 'defect_count' in df.columns and 'machine_id' in df.columns:
            machine_defects = df.groupby('machine_id')['defect_count'].mean()
            if len(machine_defects) > 1:
                worst_machine = machine_defects.idxmax()
                findings.append({
                    'equipment': worst_machine,
                    'avg_defects': float(machine_defects[worst_machine]),
                    'pattern': 'This equipment has the highest average defect count'
                })
        
        return findings
    
    def _analyze_operator_correlations(self, df):
        """Analyze operator correlations"""
        if 'operator_id' not in df.columns:
            return None
        
        findings = []
        
        operator_counts = df['operator_id'].value_counts()
        if len(operator_counts) > 1:
            problematic_operator = operator_counts.index[0]
            avg_count = operator_counts.mean()
            if operator_counts.iloc[0] > avg_count * 1.5:
                findings.append({
                    'operator': problematic_operator,
                    'issue_count': int(operator_counts.iloc[0]),
                    'avg_issue_count': float(avg_count),
                    'ratio': float(operator_counts.iloc[0] / avg_count)
                })
        
        return findings
    
    def _analyze_environmental_factors(self, df):
        """Analyze environmental factors"""
        findings = []
        
        # Temperature analysis
        if 'temperature' in df.columns and 'defect_count' in df.columns:
            high_temp = df[df['temperature'] > df['temperature'].quantile(0.75)]
            if len(high_temp) > 0:
                high_temp_defects = high_temp['defect_count'].mean()
                normal_defects = df[df['temperature'] <= df['temperature'].quantile(0.75)]['defect_count'].mean()
                if high_temp_defects > normal_defects * 1.2:
                    findings.append({
                        'factor': 'Temperature',
                        'pattern': 'Higher defect rate under high temperature conditions',
                        'evidence': f'Average defects at high temp: {high_temp_defects:.2f}, normal temp: {normal_defects:.2f}'
                    })
        
        # Vibration analysis
        if 'vibration' in df.columns and 'defect_count' in df.columns:
            high_vib = df[df['vibration'] > df['vibration'].quantile(0.75)]
            if len(high_vib) > 0:
                high_vib_defects = high_vib['defect_count'].mean()
                normal_defects = df[df['vibration'] <= df['vibration'].quantile(0.75)]['defect_count'].mean()
                if high_vib_defects > normal_defects * 1.2:
                    findings.append({
                        'factor': 'Vibration',
                        'pattern': 'Higher defect rate under high vibration conditions',
                        'evidence': f'Average defects at high vibration: {high_vib_defects:.2f}, normal vibration: {normal_defects:.2f}'
                    })
        
        return findings
    
    def generate_insights(self, filters=None):
        """Generate insights"""
        df_filtered = self._apply_filters(filters)
        
        insights = []
        
        # Trend insights
        if 'timestamp' in df_filtered.columns and 'defect_count' in df_filtered.columns:
            df_filtered = df_filtered.sort_values('timestamp')
            recent_trend = df_filtered.tail(100)['defect_count'].mean()
            previous_trend = df_filtered.head(100)['defect_count'].mean() if len(df_filtered) > 100 else recent_trend
            
            if recent_trend > previous_trend * 1.1:
                insights.append({
                    'type': 'trend',
                    'severity': 'high',
                    'title': 'Rising Defect Rate Trend',
                    'description': f'Recent defect rate is {(recent_trend/previous_trend - 1)*100:.1f}% higher than before',
                    'score': 8.5
                })
        
        # Anomaly insights
        if 'defect_count' in df_filtered.columns:
            mean_defects = df_filtered['defect_count'].mean()
            std_defects = df_filtered['defect_count'].std()
            outliers = df_filtered[df_filtered['defect_count'] > mean_defects + 2 * std_defects]
            
            if len(outliers) > 0:
                insights.append({
                    'type': 'anomaly',
                    'severity': 'critical',
                    'title': f'Found {len(outliers)} records with abnormally high defects',
                    'description': f'These records exceed mean {mean_defects:.1f} + 2σ',
                    'score': 9.0
                })
        
        # Correlation insights
        if 'temperature' in df_filtered.columns and 'defect_count' in df_filtered.columns:
            correlation = df_filtered['temperature'].corr(df_filtered['defect_count'])
            if abs(correlation) > 0.5:
                insights.append({
                    'type': 'correlation',
                    'severity': 'medium',
                    'title': 'Strong Correlation Between Temperature and Defects',
                    'description': f'Correlation coefficient: {correlation:.2f}',
                    'score': 7.5
                })
        
        # Sort by score
        insights.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'insights': insights,
            'total_insights': len(insights),
            'generated_at': datetime.now().isoformat()
        }
    
    def suggest_actions(self, root_cause, issue_type=None):
        """Suggest corrective actions"""
        actions = []
        
        if root_cause.get('type') == 'equipment':
            actions.append({
                'priority': 'high',
                'action': 'Equipment Maintenance',
                'description': 'Perform preventive maintenance check on problematic equipment',
                'steps': [
                    'Check equipment operating parameters',
                    'Review maintenance history',
                    'Perform calibration and adjustment',
                    'Replace worn components'
                ],
                'estimated_impact': 'Can reduce 30-50% of equipment-related defects'
            })
        
        if root_cause.get('type') == 'time_pattern':
            actions.append({
                'priority': 'medium',
                'action': 'Adjust Production Schedule',
                'description': 'Increase quality checks during peak issue periods',
                'steps': [
                    'Increase inspection frequency during peak hours',
                    'Assign experienced operators',
                    'Add monitoring equipment',
                    'Implement real-time alert system'
                ],
                'estimated_impact': 'Can reduce 20-40% of time-related defects'
            })
        
        if root_cause.get('type') == 'environmental':
            findings = root_cause.get('findings', [])
            for finding in findings:
                if finding.get('factor') == 'Temperature':
                    actions.append({
                        'priority': 'high',
                        'action': 'Temperature Control',
                        'description': 'Implement stricter temperature monitoring and control',
                        'steps': [
                            'Install temperature sensors and alarms',
                            'Set temperature thresholds',
                            'Optimize cooling system',
                            'Train operators to identify temperature anomalies'
                        ],
                        'estimated_impact': 'Can reduce 25-45% of temperature-related defects'
                    })
                elif finding.get('factor') == 'Vibration':
                    actions.append({
                        'priority': 'high',
                        'action': 'Vibration Control',
                        'description': 'Reduce equipment vibration',
                        'steps': [
                            'Check equipment balance',
                            'Replace worn bearings',
                            'Reinforce equipment foundation',
                            'Implement vibration monitoring system'
                        ],
                        'estimated_impact': 'Can reduce 20-35% of vibration-related defects'
                    })
        
        # General recommendations
        if not actions:
            actions.append({
                'priority': 'medium',
                'action': 'Data Collection and Analysis',
                'description': 'Collect more data to identify root causes',
                'steps': [
                    'Increase data collection frequency',
                    'Record more relevant parameters',
                    'Conduct detailed incident investigations',
                    'Establish data-driven decision process'
                ],
                'estimated_impact': 'Can improve root cause identification accuracy'
            })
        
        return {
            'actions': actions,
            'root_cause': root_cause,
            'generated_at': datetime.now().isoformat()
        }

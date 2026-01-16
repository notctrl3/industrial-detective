# Industrial Detective - Project Documentation

## Project Overview

**Industrial Detective** is an AI-powered manufacturing failure root cause analysis system designed to help manufacturing companies:
- 🔍 Discover hidden correlations and patterns
- 🎯 Identify root causes to avoid recalls or downtime
- 💡 Provide actionable insights and corrective action recommendations
- 👥 Provide an intuitive UI for factory operators and analysts

## Core Features

### 1. Exploratory Dashboard
- **Real-time Statistics**: Display key metrics such as total records, defect statistics, averages
- **Multi-dimensional Views**: Support viewing data by production line, shift, equipment, etc.
- **Interactive Charts**: Time series charts, correlation matrices, distribution charts, etc.

### 2. Time Series Analysis
- **Flexible Aggregation**: Support aggregating data by hour, day, week
- **Trend Identification**: Automatically identify rising/falling trends
- **Anomaly Detection**: Mark anomalous time periods

### 3. Correlation Analysis
- **Automatic Detection**: Calculate correlations between all numeric variables
- **Significance Testing**: Provide p-values to assess statistical significance
- **Strength Classification**: Classify correlations as very strong, strong, moderate, weak

### 4. Anomaly Detection
- **Isolation Forest Algorithm**: Use unsupervised learning to detect anomalies
- **Anomaly Scoring**: Provide anomaly scores for each record
- **Detailed Analysis**: Display key features of anomaly records

### 5. AI Insight Generation
- **Automatic Analysis**: Automatically identify trends, anomalies, and correlations
- **Intelligent Scoring**: Provide 0-10 scores for each insight
- **Severity Levels**: Classify as critical, high, medium, low

### 6. Root Cause Analysis
The system analyzes potential root causes from multiple dimensions:

#### Time Pattern Analysis
- Identify peak issue periods
- Analyze shift correlations
- Detect periodic patterns

#### Equipment Correlation Analysis
- Identify problematic equipment
- Analyze equipment-defect correlations
- Calculate equipment failure frequency

#### Operator Correlation Analysis
- Identify problematic operators
- Analyze operator-defect correlations
- Assess operator skill levels

#### Environmental Factors Analysis
- Temperature impact analysis
- Vibration impact analysis
- Pressure impact analysis
- Other environmental parameters

### 7. Corrective Action Recommendations
- **Root Cause Based**: Provide targeted recommendations based on analysis results
- **Priority Sorting**: Classify by high, medium, low priority
- **Implementation Steps**: Provide detailed implementation steps
- **Expected Impact**: Assess expected effects after implementation

## Technical Architecture

### Backend Architecture (Python Flask)

```
backend/
├── app.py              # Flask main application, API routes
├── analysis.py         # Data analysis module
├── ml_models.py        # Machine learning models
└── requirements.txt    # Python dependencies
```

#### Core Module Descriptions

**app.py**
- Define all API endpoints
- Handle HTTP requests and responses
- Data loading and initialization

**analysis.py**
- `DataAnalyzer`: Data overview, statistics, time series analysis
- `RootCauseAnalyzer`: Root cause analysis, insight generation, action recommendations

**ml_models.py**
- `CorrelationDetector`: Correlation detection
- `AnomalyDetector`: Anomaly detection (Isolation Forest)

### Frontend Architecture (Next.js + TypeScript)

```
frontend/
├── src/
│   ├── app/            # Next.js pages
│   │   ├── layout.tsx  # Root layout
│   │   ├── page.tsx    # Main page
│   │   └── globals.css # Global styles
│   ├── components/     # React components
│   │   ├── Dashboard.tsx
│   │   ├── StatsCards.tsx
│   │   ├── TimeSeriesChart.tsx
│   │   ├── CorrelationMatrix.tsx
│   │   ├── InsightsPanel.tsx
│   │   ├── AnomalyDetection.tsx
│   │   └── RootCauseAnalysis.tsx
│   └── lib/
│       └── api.ts      # API client
```

## Data Flow

1. **Data Loading**: Load from Excel file or generate sample data
2. **Data Preprocessing**: Clean, transform, standardize
3. **Feature Engineering**: Extract time features, categorical features
4. **Analysis Processing**: 
   - Statistical analysis
   - Correlation calculation
   - Anomaly detection
   - Root cause analysis
5. **Result Display**: Return via API, frontend visualization

## Machine Learning Models

### Isolation Forest (Anomaly Detection)
- **Principle**: Random forest-based anomaly detection algorithm
- **Advantages**: No labeled data required, suitable for unsupervised scenarios
- **Parameters**: contamination=0.1 (assumes 10% of data is anomalous)

### Correlation Analysis
- **Method**: Pearson correlation coefficient
- **Significance**: Calculate p-values to assess statistical significance
- **Threshold**: Default 0.5, adjustable

## API Design

### RESTful API Endpoints

#### Data Endpoints
- `GET /api/data/overview` - Get data overview
- `GET /api/data/columns` - Get column information
- `GET /api/data/sample` - Get sample data
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/time-series` - Get time series data

#### Analysis Endpoints
- `GET /api/analysis/correlations` - Correlation analysis
- `GET /api/analysis/anomalies` - Anomaly detection
- `POST /api/analysis/root-cause` - Root cause analysis
- `POST /api/insights/generate` - Generate insights
- `POST /api/actions/suggest` - Suggest actions

## Data Format

### Input Data Requirements
Excel file should contain the following columns (optional):
- `timestamp` / `date`: Timestamp
- `production_line`: Production line
- `machine_id`: Equipment ID
- `operator_id`: Operator ID
- `temperature`: Temperature
- `pressure`: Pressure
- `vibration`: Vibration
- `quality_score`: Quality score
- `defect_count`: Defect count
- `ncr_type`: NCR type
- `severity`: Severity
- `shift`: Shift
- `material_batch`: Material batch

### API Response Format
```json
{
  "status": "success",
  "data": {...},
  "timestamp": "2024-01-01T00:00:00"
}
```

## Use Cases

### Use Case 1: Daily Monitoring
Operators use the dashboard to monitor production status and promptly identify anomalies.

### Use Case 2: Problem Investigation
When quality issues occur, analysts use root cause analysis to quickly identify causes.

### Use Case 3: Preventive Maintenance
Through trend analysis and anomaly detection, identify equipment problems in advance.

### Use Case 4: Quality Improvement
Through correlation analysis, identify key factors affecting quality.

## Advantages

1. **AI-Driven**: Use machine learning to automatically discover patterns and anomalies
2. **Easy to Use**: Intuitive UI, no professional knowledge required
3. **Real-time Analysis**: Fast response, instant feedback
4. **Extensible**: Modular design, easy to extend with new features
5. **Data-Driven**: Based on actual data, provides objective analysis

## Future Improvements

1. **Predictive Analysis**: Add prediction models to predict future problems
2. **Real-time Data Streams**: Integrate real-time data sources
3. **Advanced Visualization**: Add more chart types
4. **Report Generation**: Automatically generate analysis reports
5. **User Permissions**: Add user authentication and permission management
6. **Model Optimization**: Integrate more ML models (LSTM, XGBoost, etc.)
7. **Multi-language Support**: Support multi-language interface

## Performance Optimization

- Data Caching: Cache frequently used query results
- Async Processing: Use async processing for large datasets
- Pagination: Paginate large amounts of data
- Index Optimization: Optimize database queries (if using database)

## Security Considerations

- CORS Configuration: Restrict cross-origin access
- Input Validation: Validate all user inputs
- Error Handling: Handle errors gracefully, don't expose sensitive information
- Data Privacy: Protect sensitive data

## Deployment Recommendations

### Development Environment
- Backend: `python app.py` (development mode)
- Frontend: `npm run dev` (development server)

### Production Environment
- Backend: Use Gunicorn + Nginx
- Frontend: `npm run build` + `npm start` or deploy to Vercel
- Database: Consider using PostgreSQL to store historical data
- Cache: Use Redis to cache query results

## Summary

Industrial Detective is a complete manufacturing failure analysis solution that combines data analysis, machine learning, and modern web technologies to provide powerful root cause analysis tools for manufacturing companies. The system is flexibly designed, easy to extend, and can be customized and optimized according to actual needs.

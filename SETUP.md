# Industrial Detective Setup Guide

## System Architecture

This application uses a frontend-backend separation architecture:
- **Backend**: Python Flask API (Port 5000)
- **Frontend**: Next.js React Application (Port 3000)

## Quick Start

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies (if not already installed)
pip install -r requirements.txt

# Start Flask server
python app.py
```

Backend service will start at `http://localhost:5000`

### 2. Frontend Setup

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies (first time only)
npm install

# Start development server
npm run dev
```

Frontend application will start at `http://localhost:3000`

## Data Files

The system will automatically try to load Excel data files from the following paths:
1. `../../Master Data for Hackathon .xlsx`
2. `../Master Data for Hackathon .xlsx`
3. `./data/Master Data for Hackathon .xlsx`

If no data file is found, the system will automatically generate sample data for demonstration.

## Features

### 1. Dashboard Overview
- Display key metrics such as total records, defect statistics
- Real-time data visualization

### 2. Time Series Analysis
- Aggregate data by hour/day/week
- Identify trends and patterns

### 3. Correlation Analysis
- Detect correlations between variables
- Display correlation strength and statistical significance

### 4. Anomaly Detection
- Use Isolation Forest algorithm to detect anomalies
- Display anomaly records and anomaly scores

### 5. AI Insight Generation
- Automatically identify trends, anomalies, and correlations
- Provide insight scores and severity levels

### 6. Root Cause Analysis
- Analyze time patterns, equipment correlations, operator correlations, environmental factors
- Provide confidence scores

### 7. Corrective Action Recommendations
- Provide specific recommendations based on root cause analysis results
- Include implementation steps and expected impact

## API Endpoints

### Data Related
- `GET /api/data/overview` - Data overview
- `GET /api/data/columns` - Column information
- `GET /api/data/sample` - Sample data
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/time-series` - Time series data

### Analysis Related
- `GET /api/analysis/correlations` - Correlation analysis
- `GET /api/analysis/anomalies` - Anomaly detection
- `POST /api/analysis/root-cause` - Root cause analysis
- `POST /api/insights/generate` - Generate insights
- `POST /api/actions/suggest` - Suggest actions

## Tech Stack

### Backend
- Flask - Web framework
- Pandas - Data processing
- Scikit-learn - Machine learning
- NumPy - Numerical computing

### Frontend
- Next.js 14 - React framework
- TypeScript - Type safety
- Tailwind CSS - Styling framework
- Recharts - Data visualization
- Axios - HTTP client

## Troubleshooting

### Backend Won't Start
1. Check Python version (requires Python 3.8+)
2. Ensure all dependencies are installed: `pip install -r requirements.txt`
3. Check if port 5000 is occupied

### Frontend Can't Connect to Backend
1. Ensure backend service is running
2. Check API address in `frontend/src/lib/api.ts`
3. Check CORS settings

### Data Loading Failed
1. Check Excel file path
2. Ensure file format is correct
3. System will automatically generate sample data as fallback

## Development Suggestions

1. **Data Preparation**: Place Excel file in project root or backend/data directory
2. **Custom Analysis**: Modify `backend/analysis.py` to add custom analysis logic
3. **UI Customization**: Modify components in `frontend/src/components/`
4. **Model Optimization**: Adjust model parameters in `backend/ml_models.py`

## Next Steps for Improvement

- [ ] Add user authentication and permission management
- [ ] Implement data export functionality
- [ ] Add more visualization chart types
- [ ] Implement real-time data stream processing
- [ ] Add predictive analysis functionality
- [ ] Integrate more machine learning models
- [ ] Add report generation functionality

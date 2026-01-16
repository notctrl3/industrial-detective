import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const api = {
  // Health check
  healthCheck: () => apiClient.get('/health'),

  // Data overview
  getDataOverview: () => apiClient.get('/data/overview'),
  getColumns: () => apiClient.get('/data/columns'),
  getSampleData: (limit = 100) => apiClient.get(`/data/sample?limit=${limit}`),

  // Dashboard statistics
  getDashboardStats: () => apiClient.get('/dashboard/stats'),

  // Time series
  getTimeSeries: (column: string, startDate?: string, endDate?: string, groupBy = 'hour') => {
    const params = new URLSearchParams({ column, group_by: groupBy })
    if (startDate) params.append('start_date', startDate)
    if (endDate) params.append('end_date', endDate)
    return apiClient.get(`/time-series?${params.toString()}`)
  },

  // Correlation analysis
  getCorrelations: (threshold = 0.5) =>
    apiClient.get(`/analysis/correlations?threshold=${threshold}`),

  // Anomaly detection
  getAnomalies: (limit = 50) => apiClient.get(`/analysis/anomalies?limit=${limit}`),

  // Root cause analysis
  analyzeRootCause: (issueType?: string, filters?: any) =>
    apiClient.post('/analysis/root-cause', { issue_type: issueType, filters }),

  // Generate insights
  generateInsights: (filters?: any) =>
    apiClient.post('/insights/generate', { filters }),

  // Suggest actions
  suggestActions: (rootCause: any, issueType?: string) =>
    apiClient.post('/actions/suggest', { root_cause: rootCause, issue_type: issueType }),
}

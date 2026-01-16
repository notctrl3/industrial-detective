'use client'

import { useState } from 'react'
import { Search, Filter } from 'lucide-react'
import { api } from '@/lib/api'

export default function RootCauseAnalysis() {
  const [issueType, setIssueType] = useState('')
  const [filters, setFilters] = useState<any>({})
  const [analysis, setAnalysis] = useState<any>(null)
  const [actions, setActions] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async () => {
    setLoading(true)
    try {
      const response = await api.analyzeRootCause(issueType || undefined, filters)
      setAnalysis(response.data)

      // Get suggested actions
      if (response.data.root_causes && response.data.root_causes.length > 0) {
        const actionsResponse = await api.suggestActions(
          response.data.root_causes[0],
          issueType || undefined
        )
        setActions(actionsResponse.data.actions || [])
      }
    } catch (error) {
      console.error('Root cause analysis failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="bg-gray-50 rounded-lg p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              NCR Type
            </label>
            <select
              value={issueType}
              onChange={(e) => setIssueType(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">All</option>
              <option value="Dimensional">Dimensional</option>
              <option value="Surface">Surface</option>
              <option value="Material">Material</option>
              <option value="Assembly">Assembly</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Production Line
            </label>
            <select
              value={filters.production_line || ''}
              onChange={(e) => setFilters({ ...filters, production_line: e.target.value || undefined })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">All</option>
              <option value="Line A">Line A</option>
              <option value="Line B">Line B</option>
              <option value="Line C">Line C</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Severity
            </label>
            <select
              value={filters.severity || ''}
              onChange={(e) => setFilters({ ...filters, severity: e.target.value || undefined })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">All</option>
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
              <option value="Critical">Critical</option>
            </select>
          </div>
        </div>
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="w-full bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <Search className="h-4 w-4" />
              <span>Start Analysis</span>
            </>
          )}
        </button>
      </div>

      {analysis && (
        <div className="space-y-4">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-semibold text-blue-900 mb-2">Analysis Results</h4>
            <p className="text-sm text-blue-700">
              Found {analysis.total_issues} issues, identified {analysis.root_causes.length} potential root causes
            </p>
          </div>

          <div className="space-y-3">
            {analysis.root_causes.map((cause: any, index: number) => (
              <div
                key={index}
                className="bg-white border border-gray-200 rounded-lg p-4"
              >
                <div className="flex items-center justify-between mb-2">
                  <h5 className="font-semibold text-gray-900">{cause.description}</h5>
                  <span className="text-xs px-2 py-1 bg-primary-100 text-primary-800 rounded">
                    Confidence: {(cause.confidence * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="space-y-2">
                  {cause.findings?.map((finding: any, idx: number) => (
                    <div key={idx} className="text-sm text-gray-700 pl-4 border-l-2 border-gray-200">
                      {finding.pattern && <p className="font-medium">{finding.pattern}</p>}
                      {finding.evidence && <p className="text-gray-600">{finding.evidence}</p>}
                      {finding.equipment && (
                        <p>Equipment: {finding.equipment} - Issue Count: {finding.issue_count}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {actions.length > 0 && (
            <div className="mt-6">
              <h4 className="font-semibold text-gray-900 mb-4">Suggested Corrective Actions</h4>
              <div className="space-y-3">
                {actions.map((action: any, index: number) => (
                  <div
                    key={index}
                    className="bg-green-50 border border-green-200 rounded-lg p-4"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h5 className="font-semibold text-green-900">{action.action}</h5>
                      <span className={`text-xs px-2 py-1 rounded ${
                        action.priority === 'high' ? 'bg-red-100 text-red-800' :
                        action.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {action.priority === 'high' ? 'High Priority' :
                         action.priority === 'medium' ? 'Medium Priority' : 'Low Priority'}
                      </span>
                    </div>
                    <p className="text-sm text-green-700 mb-3">{action.description}</p>
                    <div className="mb-3">
                      <p className="text-xs font-medium text-green-900 mb-1">Implementation Steps:</p>
                      <ol className="list-decimal list-inside space-y-1 text-sm text-green-700">
                        {action.steps?.map((step: string, idx: number) => (
                          <li key={idx}>{step}</li>
                        ))}
                      </ol>
                    </div>
                    <p className="text-xs text-green-600 italic">{action.estimated_impact}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

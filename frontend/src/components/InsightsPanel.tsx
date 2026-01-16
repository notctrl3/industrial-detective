'use client'

import { useEffect, useState } from 'react'
import { AlertCircle, TrendingUp, Activity } from 'lucide-react'
import { api } from '@/lib/api'

export default function InsightsPanel() {
  const [insights, setInsights] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadInsights()
  }, [])

  const loadInsights = async () => {
    try {
      const response = await api.generateInsights()
      setInsights(response.data.insights || [])
    } catch (error) {
      console.error('Failed to load insights:', error)
    } finally {
      setLoading(false)
    }
  }

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <AlertCircle className="h-5 w-5 text-red-500" />
      case 'high':
        return <TrendingUp className="h-5 w-5 text-orange-500" />
      default:
        return <Activity className="h-5 w-5 text-yellow-500" />
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'border-red-500 bg-red-50'
      case 'high':
        return 'border-orange-500 bg-orange-50'
      case 'medium':
        return 'border-yellow-500 bg-yellow-50'
      default:
        return 'border-gray-500 bg-gray-50'
    }
  }

  if (loading) {
    return <div className="h-64 flex items-center justify-center">Loading...</div>
  }

  if (insights.length === 0) {
    return <div className="h-64 flex items-center justify-center text-gray-500">No insights available</div>
  }

  return (
    <div className="space-y-3 max-h-96 overflow-y-auto">
      {insights.map((insight, index) => (
        <div
          key={index}
          className={`border-l-4 p-4 rounded ${getSeverityColor(insight.severity)}`}
        >
          <div className="flex items-start space-x-3">
            {getSeverityIcon(insight.severity)}
            <div className="flex-1">
              <div className="flex items-center justify-between mb-1">
                <h4 className="font-semibold text-gray-900">{insight.title}</h4>
                <span className="text-xs font-medium text-gray-600">
                  Score: {insight.score}/10
                </span>
              </div>
              <p className="text-sm text-gray-700">{insight.description}</p>
              <span className="inline-block mt-2 text-xs px-2 py-1 bg-white rounded text-gray-600">
                {insight.type}
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

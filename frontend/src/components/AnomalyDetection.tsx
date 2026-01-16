'use client'

import { useEffect, useState } from 'react'
import { AlertTriangle } from 'lucide-react'
import { api } from '@/lib/api'

export default function AnomalyDetection() {
  const [anomalies, setAnomalies] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [anomalyRate, setAnomalyRate] = useState(0)

  useEffect(() => {
    loadAnomalies()
  }, [])

  const loadAnomalies = async () => {
    try {
      const response = await api.getAnomalies(10)
      setAnomalies(response.data.anomalies || [])
      setAnomalyRate(response.data.anomaly_rate || 0)
    } catch (error) {
      console.error('Failed to load anomaly data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="h-64 flex items-center justify-center">Loading...</div>
  }

  return (
    <div className="space-y-4">
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <div className="flex items-center space-x-2">
          <AlertTriangle className="h-5 w-5 text-yellow-600" />
          <div>
            <p className="font-semibold text-yellow-900">Anomaly Rate: {anomalyRate.toFixed(2)}%</p>
            <p className="text-sm text-yellow-700">Detected {anomalies.length} anomaly records</p>
          </div>
        </div>
      </div>

      <div className="space-y-2 max-h-64 overflow-y-auto">
        {anomalies.map((anomaly, index) => (
          <div
            key={index}
            className="p-3 bg-red-50 border border-red-200 rounded-lg"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-red-900">
                Record #{anomaly.index}
              </span>
              <span className="text-xs text-red-700">
                Anomaly Score: {anomaly.anomaly_score.toFixed(3)}
              </span>
            </div>
            <div className="text-xs text-red-700 space-y-1">
              {anomaly.data.machine_id && (
                <p>Equipment: {anomaly.data.machine_id}</p>
              )}
              {anomaly.data.defect_count !== undefined && (
                <p>Defects: {anomaly.data.defect_count}</p>
              )}
              {anomaly.data.temperature !== undefined && (
                <p>Temperature: {anomaly.data.temperature.toFixed(1)}°C</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

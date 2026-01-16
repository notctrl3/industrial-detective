'use client'

import { useEffect, useState } from 'react'
import StatsCards from './StatsCards'
import TimeSeriesChart from './TimeSeriesChart'
import CorrelationMatrix from './CorrelationMatrix'
import InsightsPanel from './InsightsPanel'
import RootCauseAnalysis from './RootCauseAnalysis'
import AnomalyDetection from './AnomalyDetection'
import { api } from '@/lib/api'

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      const data = await api.getDashboardStats()
      setStats(data)
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Dashboard Overview</h2>
        <StatsCards stats={stats} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Time Series Analysis</h3>
          <TimeSeriesChart />
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Correlation Analysis</h3>
          <CorrelationMatrix />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">AI Insights</h3>
          <InsightsPanel />
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Anomaly Detection</h3>
          <AnomalyDetection />
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4">Root Cause Analysis</h3>
        <RootCauseAnalysis />
      </div>
    </div>
  )
}

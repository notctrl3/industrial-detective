'use client'

import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { api } from '@/lib/api'

export default function TimeSeriesChart() {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadTimeSeriesData()
  }, [])

  const loadTimeSeriesData = async () => {
    try {
      const response = await api.getTimeSeries('defect_count', undefined, undefined, 'hour')
      const chartData = response.data.data.map((item: any) => ({
        time: item.timestamp?.split(' ')[1] || item.timestamp,
        value: item.mean || item.value || 0,
      }))
      setData(chartData.slice(-50)) // Show last 50 data points
    } catch (error) {
      console.error('Failed to load time series data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="h-64 flex items-center justify-center">Loading...</div>
  }

  if (data.length === 0) {
    return <div className="h-64 flex items-center justify-center text-gray-500">No data available</div>
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="value"
          stroke="#0ea5e9"
          strokeWidth={2}
          name="Defect Count"
        />
      </LineChart>
    </ResponsiveContainer>
  )
}

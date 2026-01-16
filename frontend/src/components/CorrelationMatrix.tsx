'use client'

import { useEffect, useState } from 'react'
import { api } from '@/lib/api'

export default function CorrelationMatrix() {
  const [correlations, setCorrelations] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadCorrelations()
  }, [])

  const loadCorrelations = async () => {
    try {
      const response = await api.getCorrelations(0.5)
      setCorrelations(response.data.correlations || [])
    } catch (error) {
      console.error('Failed to load correlation data:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStrengthColor = (strength: string) => {
    switch (strength) {
      case 'very_strong':
        return 'bg-red-100 text-red-800'
      case 'strong':
        return 'bg-orange-100 text-orange-800'
      case 'moderate':
        return 'bg-yellow-100 text-yellow-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getStrengthText = (strength: string) => {
    switch (strength) {
      case 'very_strong':
        return 'Very Strong'
      case 'strong':
        return 'Strong'
      case 'moderate':
        return 'Moderate'
      default:
        return 'Weak'
    }
  }

  if (loading) {
    return <div className="h-64 flex items-center justify-center">Loading...</div>
  }

  if (correlations.length === 0) {
    return <div className="h-64 flex items-center justify-center text-gray-500">No significant correlations found</div>
  }

  return (
    <div className="space-y-2 max-h-96 overflow-y-auto">
      {correlations.slice(0, 10).map((corr, index) => (
        <div
          key={index}
          className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
        >
          <div className="flex-1">
            <div className="font-medium text-gray-900">
              {corr.variable1} ↔ {corr.variable2}
            </div>
            <div className="text-sm text-gray-600">
              Correlation: {corr.correlation.toFixed(3)}
            </div>
          </div>
          <div className={`px-3 py-1 rounded-full text-xs font-medium ${getStrengthColor(corr.strength)}`}>
            {getStrengthText(corr.strength)}
          </div>
        </div>
      ))}
    </div>
  )
}

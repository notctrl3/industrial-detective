'use client'

import { TrendingUp, AlertTriangle, Activity, BarChart3 } from 'lucide-react'

interface StatsCardsProps {
  stats: any
}

export default function StatsCards({ stats }: StatsCardsProps) {
  if (!stats) {
    return <div className="text-gray-500">Loading statistics...</div>
  }

  const cards = [
    {
      title: 'Total Records',
      value: stats.total_records?.toLocaleString() || '0',
      icon: BarChart3,
      color: 'bg-blue-500',
    },
    {
      title: 'Total Defects',
      value: stats.total_defects?.toLocaleString() || '0',
      icon: AlertTriangle,
      color: 'bg-red-500',
    },
    {
      title: 'Avg Defects',
      value: stats.avg_defects?.toFixed(2) || '0',
      icon: TrendingUp,
      color: 'bg-yellow-500',
    },
    {
      title: 'Max Defects',
      value: stats.max_defects?.toLocaleString() || '0',
      icon: Activity,
      color: 'bg-green-500',
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card, index) => {
        const Icon = card.icon
        return (
          <div
            key={index}
            className="bg-white rounded-lg shadow p-6 border-l-4 border-primary-500"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{card.title}</p>
                <p className="text-2xl font-bold text-gray-900 mt-2">{card.value}</p>
              </div>
              <div className={`${card.color} p-3 rounded-full`}>
                <Icon className="h-6 w-6 text-white" />
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}

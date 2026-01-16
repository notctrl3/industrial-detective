'use client'

import { useEffect, useState } from 'react'
import Dashboard from '@/components/Dashboard'
import Header from '@/components/Header'
import LoadingSpinner from '@/components/LoadingSpinner'

export default function Home() {
  const [loading, setLoading] = useState(true)
  const [dataLoaded, setDataLoaded] = useState(false)

  useEffect(() => {
    // Check backend connection
    fetch('http://localhost:5000/api/health')
      .then(res => res.json())
      .then(() => {
        setDataLoaded(true)
        setLoading(false)
      })
      .catch(() => {
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <LoadingSpinner />
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <Header />
      <div className="container mx-auto px-4 py-8">
        {dataLoaded ? (
          <Dashboard />
        ) : (
          <div className="text-center py-12">
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 max-w-md mx-auto">
              <h2 className="text-xl font-semibold text-yellow-800 mb-2">
                Backend Service Not Connected
              </h2>
              <p className="text-yellow-700">
                Please ensure backend service is running (http://localhost:5000)
              </p>
              <p className="text-sm text-yellow-600 mt-2">
                Run: cd backend && python app.py
              </p>
            </div>
          </div>
        )}
      </div>
    </main>
  )
}

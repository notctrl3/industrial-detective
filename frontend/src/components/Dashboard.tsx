'use client'

import { useEffect, useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts"

export default function Dashboard() {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [clearing, setClearing] = useState(false)

  useEffect(() => {
    checkData()
  }, [])

  const checkData = async () => {
    setLoading(true)
    try {
      const res = await fetch("http://localhost:5000/api/dashboard")
      if (!res.ok) {
        setData(null)
      } else {
        const json = await res.json()
        setData(json)
      }
    } catch (err) {
      console.error("Failed to fetch dashboard:", err)
      setData(null)
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      setUploading(true)
      const res = await fetch('http://localhost:5000/api/upload-excel', {
        method: 'POST',
        body: formData
      })
      if (!res.ok) throw new Error('Upload failed')
      await fetchDashboard()
    } catch (err) {
      console.error(err)
      alert('Excel upload failed')
    } finally {
      setUploading(false)
      e.target.value = ''
    }
  }

  const fetchDashboard = async () => {
    setLoading(true)
    try {
      const res = await fetch("http://localhost:5000/api/dashboard")
      const json = await res.json()
      setData(json)
    } catch (err) {
      console.error(err)
      setData(null)
    } finally {
      setLoading(false)
    }
  }

  const clearData = async () => {
    if (!confirm("Are you sure you want to clear all dashboard data?")) return
    try {
      setClearing(true)
      const res = await fetch("http://localhost:5000/api/clear-data", {
        method: "POST"
      })
      if (!res.ok) throw new Error("Failed to clear data")
      setData(null)
    } catch (err) {
      console.error(err)
      alert("Failed to clear data")
    } finally {
      setClearing(false)
    }
  }

  if (loading) return <div className="p-8">Loading dashboard...</div>

  // 没有数据只显示上传
  if (!data) {
    return (
      <div className="p-8 flex flex-col items-start gap-4">
        <h1 className="text-3xl font-bold">Industrial Detective Dashboard</h1>
        <label className="cursor-pointer">
          <input
            type="file"
            accept=".xlsx,.xls"
            id="excel-upload"
            className="hidden"
            onChange={handleFileUpload}
          />
          <button
            onClick={() => document.getElementById('excel-upload')?.click()}
            className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
            disabled={uploading}
          >
            {uploading ? 'Uploading...' : 'Upload Excel'}
          </button>
        </label>
      </div>
    )
  }

  // 有数据就显示 Dashboard
  return (
    <div className="p-8 space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Industrial Detective Dashboard</h1>
        <div className="flex gap-2">
          <label className="cursor-pointer">
            <input
              type="file"
              accept=".xlsx,.xls"
              id="excel-upload"
              className="hidden"
              onChange={handleFileUpload}
            />
            <button
              onClick={() => document.getElementById('excel-upload')?.click()}
              className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
              disabled={uploading}
            >
              {uploading ? 'Uploading...' : 'Upload Excel'}
            </button>
          </label>
          <button
            onClick={clearData}
            className="px-4 py-2 rounded bg-red-600 text-white hover:bg-red-700 disabled:opacity-50"
            disabled={clearing}
          >
            {clearing ? "Clearing..." : "Clear Dashboard Data"}
          </button>
        </div>
      </div>

      {/* Overview */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <Stat title="Total NCR" value={data.overview.total_ncr} />
        <Stat title="Today NCR" value={data.overview.today_ncr} />
        <Stat title="This Week NCR" value={data.overview.week_ncr} />
        <Stat title="Out-of-Tolerance Ratio" value={`${Math.round(data.overview.out_of_tolerance_ratio * 100)}%`} />
        <Stat title="Out-of-Tolerance Count" value={data.quality.out_of_tolerance_count} />
      </div>

      {/* Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <BarBlock title="NCR by NC Code" data={data.distribution.by_nc_code} />
        <BarBlock title="NCR by Part Type" data={data.distribution.by_part_type} />
        <BarBlock title="NCR by Machine" data={data.distribution.by_machine} />
      </div>

      {/* Trend */}
      <Card>
        <CardContent className="p-6">
          <h3 className="font-semibold mb-4">NCR Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data.trend}>
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="count" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Quality Deviation Distribution */}
      <Card>
        <CardContent className="p-6">
          <h3 className="font-semibold mb-4">Deviation Distribution</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={data.quality.deviation_distribution}>
              <XAxis dataKey="index" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="deviation" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}

function Stat({ title, value }: { title: string; value: any }) {
  return (
    <Card>
      <CardContent className="p-6">
        <p className="text-sm text-gray-500">{title}</p>
        <p className="text-2xl font-bold">{value}</p>
      </CardContent>
    </Card>
  )
}

function BarBlock({ title, data }: { title: string; data: Record<string, number> }) {
  const chartData = Object.entries(data).map(([k, v]) => ({ name: k, value: v }))
  return (
    <Card>
      <CardContent className="p-6">
        <h3 className="font-semibold mb-4">{title}</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={chartData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}

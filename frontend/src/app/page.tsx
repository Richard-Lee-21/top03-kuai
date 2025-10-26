'use client'

import { useState } from 'react'
import Head from 'next/head'
import SearchComponent from '@/components/SearchComponent'
import ResultsComponent from '@/components/ResultsComponent'
import { Top3Recommendation } from '@/types'

export default function Home() {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [results, setResults] = useState<Top3Recommendation[]>([])

  const handleSubmit = async (keyword: string) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await fetch('/api/v1/top3', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ keyword }),
      })
      
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      
      const data = await response.json()
      
      if (data.status === 'success') {
        setResults(data.data)
      } else {
        throw new Error(data.message || 'Failed to get recommendations')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setResults([])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      <Head>
        <title>Top03-Kuai - 动态商品推荐引擎</title>
        <meta name="description" content="基于实时网络搜索和AI分析的智能商品推荐系统" />
        <meta name="keywords" content="商品推荐,AI推荐,智能搜索,Top3,购物推荐" />
      </Head>
      
      <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">T3</span>
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">Top03-Kuai</h1>
                  <p className="text-sm text-gray-600">智能商品推荐引擎</p>
                </div>
              </div>
              <div className="hidden md:flex items-center space-x-4">
                <a href="/admin" className="text-gray-600 hover:text-primary-600 transition-colors">
                  管理后台
                </a>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Hero Section */}
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                发现全网最佳商品
              </h2>
              <p className="text-xl text-gray-600 mb-8">
                输入商品关键词，AI将为您分析全网信息，推荐Top 3最佳选择
              </p>
            </div>

            {/* Search Component */}
            <div className="mb-8">
              <SearchComponent 
                onSubmit={handleSubmit}
                isLoading={isLoading}
                error={error}
              />
            </div>

            {/* Results Component */}
            <div>
              <ResultsComponent 
                data={results}
                isLoading={isLoading}
                error={error}
              />
            </div>
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-gray-50 border-t border-gray-200 py-8">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-600">
            <p>&copy; 2025 Top03-Kuai. 基于AI的智能推荐系统。</p>
          </div>
        </footer>
      </div>
    </>
  )
}
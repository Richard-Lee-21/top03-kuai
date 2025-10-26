'use client'

import React, { useState } from 'react'

interface SearchComponentProps {
  onSubmit: (keyword: string) => void
  isLoading: boolean
  error: string | null
}

export default function SearchComponent({ onSubmit, isLoading, error }: SearchComponentProps) {
  const [keyword, setKeyword] = useState('')

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (keyword.trim()) {
      onSubmit(keyword.trim())
    }
  }

  return (
    <div className="card">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="keyword" className="block text-sm font-medium text-gray-700 mb-2">
            商品关键词
          </label>
          <div className="flex space-x-4">
            <input
              type="text"
              id="keyword"
              value={keyword}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setKeyword(e.target.value)}
              placeholder="例如：无线耳机、智能手表、笔记本电脑..."
              disabled={isLoading}
              className="flex-1 input focus:outline-none"
              style={{ minWidth: '300px' }}
            />
            <button
              type="submit"
              disabled={!keyword.trim() || isLoading}
              className={`btn btn-primary whitespace-nowrap ${
                (!keyword.trim() || isLoading) ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              {isLoading ? (
                <div className="flex items-center space-x-2">
                  <div className="loading-spinner w-4 h-4"></div>
                  <span>正在分析...</span>
                </div>
              ) : (
                '获取Top3推荐'
              )}
            </button>
          </div>
        </div>
        
        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}
        
        <div className="text-sm text-gray-500">
          <p>💡 提示：输入具体商品名称或型号可以获得更精准的推荐结果</p>
        </div>
      </form>
    </div>
  )
}
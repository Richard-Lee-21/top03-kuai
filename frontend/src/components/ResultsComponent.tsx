'use client'

import { Top3Recommendation } from '@/types'

interface ResultsComponentProps {
  data: Top3Recommendation[]
  isLoading: boolean
  error: string | null
}

export default function ResultsComponent({ data, isLoading, error }: ResultsComponentProps) {
  if (isLoading) {
    return (
      <div className="text-center py-12">
        <div className="loading-spinner w-8 h-8 mx-auto mb-4"></div>
        <p className="text-gray-600">正在分析全网信息，为您寻找最佳推荐...</p>
        <p className="text-sm text-gray-500 mt-2">这可能需要30-60秒，请耐心等待</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-4xl mb-4">❌</div>
        <p className="text-red-600 text-lg">获取推荐失败</p>
        <p className="text-gray-600 mt-2">{error}</p>
      </div>
    )
  }

  if (data.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-4xl mb-4">🔍</div>
        <p className="text-gray-600">请输入商品关键词开始搜索</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h3 className="text-2xl font-bold text-gray-900 mb-2">🎉 智能推荐结果</h3>
        <p className="text-gray-600">基于全网信息分析的Top 3推荐</p>
      </div>
      
      <div className="grid gap-6 md:grid-cols-3">
        {data.map((product, index) => (
          <ProductCard key={product.rank} product={product} index={index} />
        ))}
      </div>
      
      <div className="text-center mt-8 text-sm text-gray-500">
        <p>💡 这些推荐基于实时网络搜索和AI分析，数据更新时间为最近24小时</p>
      </div>
    </div>
  )
}

interface ProductCardProps {
  product: Top3Recommendation
  index: number
  key?: string | number
}

function ProductCard({ product, index }: ProductCardProps) {
  const getRankColor = (rank: number) => {
    switch (rank) {
      case 1: return 'border-yellow-400 bg-yellow-50'
      case 2: return 'border-gray-300 bg-gray-50'
      case 3: return 'border-orange-300 bg-orange-50'
      default: return 'border-gray-200 bg-white'
    }
  }

  const getRankBadge = (rank: number) => {
    switch (rank) {
      case 1: return '🥇'
      case 2: return '🥈'
      case 3: return '🥉'
      default: return `#${rank}`
    }
  }

  return (
    <div className={`product-card border-2 ${getRankColor(product.rank)} animate-fade-in`}>
      <div className="flex items-center justify-between mb-4">
        <span className="text-2xl font-bold text-gray-900">
          {getRankBadge(product.rank)}
        </span>
        {index === 0 && (
          <span className="px-3 py-1 bg-yellow-400 text-yellow-900 text-xs font-medium rounded-full">
            推荐之王
          </span>
        )}
      </div>
      
      <h4 className="font-semibold text-gray-900 mb-3 line-clamp-2">
        {product.product_name}
      </h4>
      
      <p className="text-gray-700 text-sm mb-4 line-clamp-4 leading-relaxed">
        {product.description}
      </p>
      
      <div className="mt-auto">
        <a
          href={product.source_link}
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn-secondary w-full text-center text-sm"
        >
          查看详情
        </a>
      </div>
    </div>
  )
}
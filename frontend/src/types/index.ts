export interface Top3Recommendation {
  rank: number
  product_name: string
  description: string
  source_link: string
}

export interface KeywordRequest {
  keyword: string
}

export interface Top3Response {
  status: string
  data: Top3Recommendation[]
}

export interface ApiResponse<T> {
  status: string
  data?: T
  message?: string
}

export interface SearchState {
  keyword: string
  isLoading: boolean
  error: string | null
  results: Top3Recommendation[]
}
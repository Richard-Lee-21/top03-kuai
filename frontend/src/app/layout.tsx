import './globals.css'

export const metadata = {
  title: 'Top03-Kuai - 动态商品推荐引擎',
  description: '基于实时网络搜索和AI分析的智能商品推荐系统',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body className="font-sans antialiased">
        <div className="min-h-screen bg-gray-50">
          {children}
        </div>
      </body>
    </html>
  )
}
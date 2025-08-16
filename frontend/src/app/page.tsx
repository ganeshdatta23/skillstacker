import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="text-xl font-bold text-blue-600">SkillStacker</div>
          <div className="space-x-4">
            <Link href="/data" className="text-gray-700 hover:text-blue-600">Data Explorer</Link>
            <Link href="/products" className="text-gray-700 hover:text-blue-600">Products</Link>
            <Link href="/login" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Login</Link>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-6">
            Welcome to SkillStacker
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            A modern full-stack application showcasing enterprise-grade development practices with Next.js and FastAPI.
          </p>
          
          <div className="space-x-4">
            <Link 
              href="/data" 
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 inline-block"
            >
              Explore Data
            </Link>
            <Link 
              href="/products" 
              className="border border-blue-600 text-blue-600 px-6 py-3 rounded-lg hover:bg-blue-50 inline-block"
            >
              Browse Products
            </Link>
          </div>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-3">🎬 1,000 Films</h3>
            <p className="text-gray-600">Explore our complete film database with titles, ratings, and detailed information.</p>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-3">📚 364K Publications</h3>
            <p className="text-gray-600">Search through hundreds of thousands of research publications and academic papers.</p>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-3">🗄️ Dual Database</h3>
            <p className="text-gray-600">PostgreSQL for structured data and MongoDB for flexible document storage.</p>
          </div>
        </div>

        <div className="mt-12 bg-blue-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-3">🚀 Demo Accounts</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="font-medium">Regular User:</p>
              <p className="text-sm text-gray-600">demo@skillstacker.com / demo123</p>
            </div>
            <div>
              <p className="font-medium">Admin User:</p>
              <p className="text-sm text-gray-600">admin@skillstacker.com / admin123</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
import React from 'react';
import { Search, BarChart3, FileText, Users, CheckCircle, TrendingUp, Award, Zap, Shield, Globe, Settings, Download, Wallet, Lock, Database, ArrowRight, Star } from 'lucide-react';

const FeatureSection: React.FC = () => {
  const features = [
    {
      icon: Search,
      title: 'Technical SEO Audit',
      description: 'Comprehensive analysis of 140+ technical SEO factors including crawlability, indexability, and site structure.',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      gradient: 'from-blue-500 to-blue-600',
      badge: 'Most Popular'
    },
    {
      icon: BarChart3,
      title: 'Performance Analysis',
      description: 'Detailed performance metrics including Core Web Vitals, page speed, and optimization recommendations.',
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      gradient: 'from-green-500 to-green-600',
      badge: 'Fast'
    },
    {
      icon: Shield,
      title: 'Security & SSL',
      description: 'Security assessment including SSL certificates, security headers, and vulnerability scanning.',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      gradient: 'from-purple-500 to-purple-600',
      badge: 'Secure'
    },
    {
      icon: Zap,
      title: 'Mobile Optimization',
      description: 'Mobile-friendliness testing, responsive design analysis, and mobile performance optimization.',
      color: 'text-orange-600',
      bgColor: 'bg-orange-50',
      gradient: 'from-orange-500 to-orange-600',
      badge: 'Mobile'
    },
    {
      icon: Wallet,
      title: 'Web3 Integration',
      description: 'Secure wallet-based authentication with MetaMask. No traditional accounts needed.',
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-50',
      gradient: 'from-indigo-500 to-indigo-600',
      badge: 'Web3'
    },
    {
      icon: Lock,
      title: 'Decentralized Storage',
      description: 'Audit results stored securely on blockchain with immutable verification.',
      color: 'text-red-600',
      bgColor: 'bg-red-50',
      gradient: 'from-red-500 to-red-600',
      badge: 'Blockchain'
    }
  ];

  const stats = [
    { icon: CheckCircle, value: '140+', label: 'Technical Checks', color: 'text-blue-600' },
    { icon: TrendingUp, value: '99%', label: 'Accuracy Rate', color: 'text-green-600' },
    { icon: Users, value: '50,000+', label: 'Websites Audited', color: 'text-purple-600' },
    { icon: Award, value: '24/7', label: 'Support Available', color: 'text-orange-600' }
  ];

  const tools = [
    'Site Crawler',
    'Backlink Analysis', 
    'Keyword Research',
    'Competitor Analysis',
    'Rank Tracking'
  ];

  return (
    <div id="seo" className="pt-8 pb-24 bg-gradient-to-br from-gray-50 via-white to-blue-50 relative overflow-hidden">
      {/* Background Decorations */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-64 h-64 bg-blue-200/20 rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 right-10 w-80 h-80 bg-purple-200/20 rounded-full blur-3xl"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-indigo-200/10 rounded-full blur-3xl"></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Main Features */}
        <div className="text-center mb-24">
          <div className="inline-flex items-center space-x-2 bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-medium mb-6">
            <Star className="w-4 h-4 fill-current" />
            <span>Professional Suite</span>
          </div>
          <h2 className="text-5xl md:text-6xl font-bold text-gray-900 mb-8 bg-gradient-to-r from-gray-900 via-blue-900 to-indigo-900 bg-clip-text text-transparent">
            AUDIT Guardian Professional Suite
          </h2>
          <p className="text-xl text-gray-600 max-w-4xl mx-auto leading-relaxed font-light">
            Comprehensive SEO platform with advanced tools for technical analysis, performance optimization, and competitive research.
            <span className="block mt-2 text-blue-600 font-semibold">Powered by Web3 technology for enhanced security and transparency.</span>
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-24">
          {features.map((feature, index) => (
            <div
              key={index}
              className="group bg-white/80 backdrop-blur-sm p-8 rounded-3xl shadow-xl hover:shadow-2xl transition-all duration-500 border border-gray-200/50 hover:border-gray-300 relative overflow-hidden cursor-pointer transform hover:-translate-y-3 hover:scale-105"
            >
              {/* Badge */}
              {feature.badge && (
                <div className="absolute top-4 right-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white text-xs font-bold px-3 py-1 rounded-full">
                  {feature.badge}
                </div>
              )}

              {/* Hover background effect */}
              <div className={`absolute inset-0 bg-gradient-to-br ${feature.gradient} opacity-0 group-hover:opacity-5 transition-opacity duration-500`}></div>
              
              <div className={`inline-flex p-4 rounded-2xl ${feature.bgColor} mb-6 group-hover:scale-110 transition-transform duration-300 relative z-10 shadow-lg`}>
                <feature.icon className={`w-8 h-8 ${feature.color} group-hover:animate-pulse`} />
              </div>
              
              <h3 className="text-xl font-bold text-gray-900 mb-4 group-hover:text-gray-800 transition-colors duration-300 relative z-10">
                {feature.title}
              </h3>
              
              <p className="text-gray-600 leading-relaxed mb-6 group-hover:text-gray-700 transition-colors duration-300 relative z-10">
                {feature.description}
              </p>
              
              <div className="flex items-center justify-between relative z-10">
                <div className={`h-1 w-20 bg-gradient-to-r ${feature.gradient} rounded-full group-hover:w-32 transition-all duration-500`}></div>
                <ArrowRight className={`w-5 h-5 ${feature.color} group-hover:translate-x-2 transition-transform duration-300`} />
              </div>
            </div>
          ))}
        </div>

        {/* Web3 Benefits Section */}
        <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 rounded-3xl p-16 text-white mb-24 relative overflow-hidden shadow-2xl">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 via-purple-600/20 to-indigo-600/20"></div>
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(255,255,255,0.1)_0%,transparent_50%)]"></div>
          <div className="relative z-10">
            <div className="text-center mb-16">
              <div className="inline-flex items-center justify-center w-20 h-20 bg-white/20 backdrop-blur-sm rounded-3xl mb-8 shadow-2xl">
                <Wallet className="w-10 h-10 text-white" />
              </div>
              <h3 className="text-4xl md:text-5xl font-bold mb-8">
                Web3-Powered Security
              </h3>
              <p className="text-xl text-blue-100 max-w-3xl mx-auto">
                AUDIT Guardian leverages blockchain technology for enhanced security, transparency, and user control.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center group">
                <div className="bg-white/20 backdrop-blur-sm p-6 rounded-2xl mb-6 inline-block group-hover:scale-110 transition-transform duration-300 shadow-xl">
                  <Shield className="w-10 h-10 text-white" />
                </div>
                <h4 className="text-xl font-bold mb-4">Secure Authentication</h4>
                <p className="text-blue-100">MetaMask wallet-based login with no traditional accounts or passwords</p>
              </div>
              
              <div className="text-center group">
                <div className="bg-white/20 backdrop-blur-sm p-6 rounded-2xl mb-6 inline-block group-hover:scale-110 transition-transform duration-300 shadow-xl">
                  <Database className="w-10 h-10 text-white" />
                </div>
                <h4 className="text-xl font-bold mb-4">Immutable Records</h4>
                <p className="text-blue-100">Audit results stored on blockchain for permanent verification</p>
              </div>
              
              <div className="text-center group">
                <div className="bg-white/20 backdrop-blur-sm p-6 rounded-2xl mb-6 inline-block group-hover:scale-110 transition-transform duration-300 shadow-xl">
                  <Lock className="w-10 h-10 text-white" />
                </div>
                <h4 className="text-xl font-bold mb-4">User Control</h4>
                <p className="text-blue-100">Complete control over your data with decentralized storage</p>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Section (Security anchor) */}
        <div id="security" className="bg-white/80 backdrop-blur-sm rounded-3xl p-16 border border-gray-200/50 shadow-2xl relative overflow-hidden mb-24">
          <div className="absolute inset-0 bg-gradient-to-br from-blue-50/50 via-white to-purple-50/50"></div>
          <div className="relative z-10">
            <div className="text-center mb-16">
              <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-blue-100 to-purple-100 text-blue-800 px-4 py-2 rounded-full text-sm font-medium mb-6">
                <Award className="w-4 h-4" />
                <span>Trusted Worldwide</span>
              </div>
              <h3 className="text-4xl md:text-5xl font-bold text-gray-900 mb-8">
                Trusted by SEO Professionals Worldwide
              </h3>
              <p className="text-xl text-gray-600 font-light">
                Join thousands of professionals who rely on AUDIT Guardian for their SEO success
              </p>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {stats.map((stat, index) => (
                <div key={index} className="text-center group cursor-pointer">
                  <div className="inline-flex p-6 bg-gradient-to-br from-blue-500 to-purple-600 rounded-3xl mb-6 group-hover:scale-110 group-hover:shadow-2xl transition-all duration-300 shadow-xl">
                    <stat.icon className="w-10 h-10 text-white group-hover:animate-bounce" />
                  </div>
                  <div className={`text-4xl md:text-5xl font-bold text-gray-900 mb-3 group-hover:scale-110 transition-transform duration-300 ${stat.color}`}>{stat.value}</div>
                  <div className="text-gray-600 font-medium group-hover:text-gray-800 transition-colors duration-300">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Additional Tools Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center space-x-2 bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-medium mb-6">
            <Zap className="w-4 h-4" />
            <span>Additional Tools</span>
          </div>
          <h3 className="text-4xl md:text-5xl font-bold text-gray-900 mb-8">
            AUDIT Guardian Additional Tools
          </h3>
          <p className="text-xl text-gray-600 mb-12 font-light max-w-3xl mx-auto">
            Complete your SEO toolkit with AUDIT Guardian's additional professional tools and features
          </p>
          
          <div className="grid grid-cols-2 md:grid-cols-5 gap-6 max-w-5xl mx-auto">
            {tools.map((tool, index) => (
              <div 
                key={index} 
                className="group bg-white/80 backdrop-blur-sm p-6 rounded-2xl border border-gray-200/50 hover:border-blue-300 hover:shadow-xl transition-all duration-500 cursor-pointer transform hover:-translate-y-2 relative overflow-hidden"
              >
                {/* Hover background effect */}
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-indigo-600 opacity-0 group-hover:opacity-5 transition-opacity duration-500"></div>
                
                <span className="text-base font-semibold text-gray-900 group-hover:text-blue-600 transition-colors duration-300 relative z-10">
                  {tool}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center">
          <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 rounded-3xl p-16 text-white relative overflow-hidden shadow-2xl">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 via-purple-600/20 to-indigo-600/20"></div>
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,rgba(255,255,255,0.1)_0%,transparent_50%)]"></div>
            <div className="relative z-10">
              <h3 className="text-4xl md:text-5xl font-bold mb-8">
                Ready to Improve Your SEO with AUDIT Guardian?
              </h3>
              <p className="text-xl text-blue-100 mb-12 max-w-2xl mx-auto">
                Connect your MetaMask wallet and start your comprehensive site audit today. Get actionable insights to boost your search rankings.
              </p>
              <button className="bg-white text-blue-600 font-bold py-5 px-10 rounded-2xl hover:bg-gray-100 transition-all duration-300 transform hover:scale-105 shadow-2xl hover:shadow-white/25 relative overflow-hidden group">
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent group-hover:animate-shimmer"></div>
                <span className="relative z-10 flex items-center space-x-3">
                  <Wallet className="w-6 h-6" />
                  <span>Connect Wallet & Start Free Analysis</span>
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FeatureSection;
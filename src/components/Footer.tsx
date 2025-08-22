import React from 'react';
import { Shield, Mail, Phone, MapPin, Twitter, Linkedin, Instagram, Youtube, ExternalLink, ArrowRight, Star, Zap, Lock } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer id="contacts" className="bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 text-white relative overflow-hidden">
      {/* Background Decorations */}
      <div className="absolute inset-0">
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-blue-500 to-transparent"></div>
        <div className="absolute top-20 left-10 w-64 h-64 bg-blue-500/5 rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 right-10 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-indigo-500/5 rounded-full blur-3xl"></div>
      </div>

      {/* Grid Pattern Overlay */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:50px_50px]"></div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
          {/* Brand Section */}
          <div className="lg:col-span-2">
            <div className="flex items-center space-x-4 mb-8 group">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 via-purple-500 to-indigo-600 rounded-2xl flex items-center justify-center shadow-2xl group-hover:scale-110 transition-transform duration-300 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
                <Shield className="w-8 h-8 text-white relative z-10" />
              </div>
              <div>
                <h3 className="text-3xl font-bold bg-gradient-to-r from-white via-blue-100 to-purple-100 bg-clip-text text-transparent">
                  AUDIT Guardian
                </h3>
                <p className="text-blue-200 text-sm font-medium">Professional SEO Analysis</p>
              </div>
            </div>
            <p className="text-blue-100 text-lg leading-relaxed mb-8 max-w-md">
              AUDIT Guardian provides clear, actionable recommendations to improve your search engine rankings and online presence.
            </p>
            
            {/* Social Icons */}
            <div className="flex items-center space-x-4">
              <a href="#" className="group">
                <div className="w-12 h-12 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl flex items-center justify-center hover:bg-white/20 hover:border-blue-400 transition-all duration-300 shadow-lg hover:shadow-blue-500/25 group-hover:scale-110">
                  <Linkedin className="w-5 h-5 text-white group-hover:text-blue-300 transition-colors" />
                </div>
              </a>
              <a href="#" className="group">
                <div className="w-12 h-12 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl flex items-center justify-center hover:bg-white/20 hover:border-blue-400 transition-all duration-300 shadow-lg hover:shadow-blue-500/25 group-hover:scale-110">
                  <Twitter className="w-5 h-5 text-white group-hover:text-blue-300 transition-colors" />
                </div>
              </a>
              <a href="#" className="group">
                <div className="w-12 h-12 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl flex items-center justify-center hover:bg-white/20 hover:border-purple-400 transition-all duration-300 shadow-lg hover:shadow-purple-500/25 group-hover:scale-110">
                  <Instagram className="w-5 h-5 text-white group-hover:text-purple-300 transition-colors" />
                </div>
              </a>
              <a href="#" className="group">
                <div className="w-12 h-12 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl flex items-center justify-center hover:bg-white/20 hover:border-red-400 transition-all duration-300 shadow-lg hover:shadow-red-500/25 group-hover:scale-110">
                  <Youtube className="w-5 h-5 text-white group-hover:text-red-300 transition-colors" />
                </div>
              </a>
            </div>
          </div>

          {/* Features */}
          <div>
            <h4 className="text-xl font-bold mb-8 bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
              Features
            </h4>
            <ul className="space-y-4">
              {[
                'Technical SEO Audit',
                'Performance Analysis',
                'Security & SSL',
                'Mobile Optimization',
                'Web3 Integration',
                'Decentralized Storage'
              ].map((feature, index) => (
                <li key={index} className="group">
                  <a 
                    href="#" 
                    className="flex items-center space-x-3 text-blue-100 hover:text-white transition-all duration-300 group-hover:translate-x-2"
                  >
                    <div className="w-2 h-2 bg-blue-400 rounded-full group-hover:bg-white transition-colors"></div>
                    <span className="group-hover:underline">{feature}</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="text-xl font-bold mb-8 bg-gradient-to-r from-white to-purple-200 bg-clip-text text-transparent">
              Resources
            </h4>
            <ul className="space-y-4">
              {[
                'Documentation',
                'API Reference',
                'Tutorials',
                'Case Studies',
                'Blog',
                'Support'
              ].map((resource, index) => (
                <li key={index} className="group">
                  <a 
                    href="#" 
                    className="flex items-center space-x-3 text-blue-100 hover:text-white transition-all duration-300 group-hover:translate-x-2"
                  >
                    <div className="w-2 h-2 bg-purple-400 rounded-full group-hover:bg-white transition-colors"></div>
                    <span className="group-hover:underline">{resource}</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Web3 Features Section */}
        <div className="mt-20 bg-white/5 backdrop-blur-sm border border-white/10 rounded-3xl p-12 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 via-purple-500/5 to-indigo-500/5"></div>
          <div className="relative z-10">
            <div className="text-center mb-12">
              <div className="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-sm border border-white/20 px-4 py-2 rounded-full text-sm font-medium mb-6">
                <Zap className="w-4 h-4 text-blue-300" />
                <span>Web3 Technology</span>
              </div>
              <h3 className="text-3xl md:text-4xl font-bold mb-6">
                Powered by Web3 Technology
              </h3>
              <p className="text-blue-100 text-lg max-w-3xl mx-auto">
                AUDIT Guardian leverages blockchain technology for enhanced security, transparency, and user control.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center group">
                <div className="bg-white/10 backdrop-blur-sm p-6 rounded-2xl mb-6 inline-block group-hover:scale-110 transition-transform duration-300 shadow-xl">
                  <Shield className="w-10 h-10 text-blue-300" />
                </div>
                <h4 className="text-xl font-bold mb-4">Secure Authentication</h4>
                <p className="text-blue-100">MetaMask wallet-based login with no traditional accounts or passwords</p>
              </div>
              
              <div className="text-center group">
                <div className="bg-white/10 backdrop-blur-sm p-6 rounded-2xl mb-6 inline-block group-hover:scale-110 transition-transform duration-300 shadow-xl">
                  <Lock className="w-10 h-10 text-purple-300" />
                </div>
                <h4 className="text-xl font-bold mb-4">Immutable Records</h4>
                <p className="text-blue-100">Audit results stored on blockchain for permanent verification</p>
              </div>
              
              <div className="text-center group">
                <div className="bg-white/10 backdrop-blur-sm p-6 rounded-2xl mb-6 inline-block group-hover:scale-110 transition-transform duration-300 shadow-xl">
                  <Star className="w-10 h-10 text-indigo-300" />
                </div>
                <h4 className="text-xl font-bold mb-4">User Control</h4>
                <p className="text-blue-100">Complete control over your data with decentralized storage</p>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-16 pt-8 border-t border-white/10">
          <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
            <div className="flex items-center space-x-6 text-sm text-blue-200">
              <span>© 2025 AUDIT Guardian. All rights reserved.</span>
              <div className="flex items-center space-x-4">
                <a href="#" className="hover:text-white transition-colors duration-300 hover:underline">
                  Privacy Policy
                </a>
                <a href="#" className="hover:text-white transition-colors duration-300 hover:underline">
                  Terms of Service
                </a>
                <a href="#" className="hover:text-white transition-colors duration-300 hover:underline">
                  Cookie Policy
                </a>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full border border-white/20">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-sm text-green-300 font-medium">Secure & Verified</span>
              </div>
              <div className="flex items-center space-x-1">
                <Star className="w-4 h-4 text-yellow-400 fill-current" />
                <Star className="w-4 h-4 text-yellow-400 fill-current" />
                <Star className="w-4 h-4 text-yellow-400 fill-current" />
                <Star className="w-4 h-4 text-yellow-400 fill-current" />
                <Star className="w-4 h-4 text-yellow-400 fill-current" />
                <span className="text-sm text-blue-200 ml-2">5.0 Rating</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
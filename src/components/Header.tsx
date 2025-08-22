import React, { useState, useEffect } from 'react';
import { Search, BarChart3, FileText, Users, Settings, TrendingUp, Shield, Zap, Wallet, LogOut, ChevronDown, Sparkles, Star, ArrowRight } from 'lucide-react';

const Header: React.FC = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [walletAddress, setWalletAddress] = useState('');
  const [isConnecting, setIsConnecting] = useState(false);

  // Check if MetaMask is installed
  const isMetaMaskInstalled = () => {
    return typeof window !== 'undefined' && window.ethereum && window.ethereum.isMetaMask;
  };

  // Connect to MetaMask
  const connectWallet = async () => {
    if (!isMetaMaskInstalled()) {
      alert('Please install MetaMask to use AUDIT Guardian');
      return;
    }

    setIsConnecting(true);
    try {
      const accounts = await window.ethereum.request({
        method: 'eth_requestAccounts',
      });
      
      if (accounts.length > 0) {
        setWalletAddress(accounts[0]);
        setIsConnected(true);
        localStorage.setItem('auditGuardianWallet', accounts[0]);
      }
    } catch (error) {
      console.error('Error connecting to MetaMask:', error);
      alert('Failed to connect to MetaMask. Please try again.');
    } finally {
      setIsConnecting(false);
    }
  };

  // Disconnect wallet
  const disconnectWallet = () => {
    setWalletAddress('');
    setIsConnected(false);
    localStorage.removeItem('auditGuardianWallet');
  };

  // Format wallet address for display
  const formatAddress = (address: string) => {
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
  };

  // Check for existing connection on component mount
  useEffect(() => {
    const savedWallet = localStorage.getItem('auditGuardianWallet');
    if (savedWallet) {
      setWalletAddress(savedWallet);
      setIsConnected(true);
    }
  }, []);

  return (
    <header className="bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 text-white relative overflow-hidden min-h-screen">
      {/* Animated Background Elements */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-blue-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute top-40 right-20 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute bottom-20 left-1/3 w-80 h-80 bg-indigo-500/10 rounded-full blur-3xl animate-pulse delay-2000"></div>
      </div>

      {/* Grid Pattern Overlay */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:50px_50px]"></div>

      {/* Top Navigation Bar */}
      <div className="bg-black/20 backdrop-blur-xl border-b border-white/10 relative z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            <div className="flex items-center space-x-6 text-sm">
              <div className="flex items-center space-x-3 group">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 via-purple-500 to-indigo-600 rounded-xl flex items-center justify-center shadow-2xl group-hover:scale-110 transition-transform duration-300 relative overflow-hidden">
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
                  <Shield className="w-5 h-5 text-white relative z-10" />
                </div>
                <span className="font-bold text-white text-xl tracking-tight group-hover:text-blue-300 transition-colors">AUDIT Guardian</span>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <a
                href="http://127.0.0.1:5000"
                className="hidden sm:inline-flex items-center text-sm px-5 py-2.5 rounded-xl border border-white/20 bg-white/5 text-white/80 hover:text-white hover:border-blue-400 hover:bg-blue-500/10 transition-all duration-300 shadow-lg hover:shadow-blue-500/25 backdrop-blur-sm group"
              >
                <span>Search Engine Optimization</span>
                <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
              </a>
              <a
                href="http://localhost:8501"
                className="hidden sm:inline-flex items-center text-sm px-5 py-2.5 rounded-xl border border-white/20 bg-white/5 text-white/80 hover:text-white hover:border-purple-400 hover:bg-purple-500/10 transition-all duration-300 shadow-lg hover:shadow-purple-500/25 backdrop-blur-sm group"
              >
                <span>SECURITY CHECKUP</span>
                <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
              </a>
              <a
                href="http://localhost:8502"
                className="hidden sm:inline-flex items-center text-sm px-5 py-2.5 rounded-xl border border-white/20 bg-white/5 text-white/80 hover:text-white hover:border-gray-400 hover:bg-gray-500/10 transition-all duration-300 shadow-lg hover:shadow-gray-500/25 backdrop-blur-sm group"
              >
                <span>Bug Fixer</span>
                <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
              </a>
              {isConnected ? (
                <div className="flex items-center space-x-3">
                  <div className="flex items-center space-x-2 bg-green-500/20 backdrop-blur-sm px-4 py-2.5 rounded-xl border border-green-500/30 shadow-lg">
                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                    <span className="text-sm text-green-300 font-medium">Connected</span>
                  </div>
                  <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-sm px-4 py-2.5 rounded-xl border border-white/20 shadow-lg">
                    <Wallet className="w-4 h-4 text-blue-300" />
                    <span className="text-sm text-white/90 font-mono">{formatAddress(walletAddress)}</span>
                  </div>
                  <button
                    onClick={disconnectWallet}
                    className="flex items-center space-x-2 text-sm text-white/70 hover:text-red-400 transition-colors duration-300 hover:scale-105"
                  >
                    <LogOut className="w-4 h-4" />
                    <span>Disconnect</span>
                  </button>
                </div>
              ) : (
                <button
                  onClick={connectWallet}
                  disabled={isConnecting}
                  className="flex items-center space-x-2 bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 text-white px-6 py-2.5 rounded-xl text-sm font-medium hover:from-blue-700 hover:via-purple-700 hover:to-indigo-700 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-2xl hover:shadow-blue-500/50 transform hover:scale-105 relative overflow-hidden group"
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent group-hover:animate-shimmer"></div>
                  {isConnecting ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent relative z-10"></div>
                      <span className="relative z-10">Connecting...</span>
                    </>
                  ) : (
                    <>
                      <Wallet className="w-4 h-4 relative z-10" />
                      <span className="relative z-10">Connect Wallet</span>
                    </>
                  )}
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Enhanced Hero */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 relative z-10">
        <div className="text-center">
          {/* Enhanced Badge */}
          <div className="inline-flex items-center space-x-3 bg-white/10 backdrop-blur-xl border border-white/20 px-6 py-3 rounded-full mb-6 shadow-2xl hover:bg-white/15 transition-all duration-300 group">
            <div className="flex items-center space-x-2">
              <Sparkles className="w-5 h-5 text-blue-400 group-hover:animate-pulse" />
              <span className="text-sm text-white/90 font-medium">Audit Platform</span>
            </div>
            <div className="flex items-center space-x-1">
              <Star className="w-3 h-3 text-yellow-400 fill-current" />
              <Star className="w-3 h-3 text-yellow-400 fill-current" />
              <Star className="w-3 h-3 text-yellow-400 fill-current" />
              <Star className="w-3 h-3 text-yellow-400 fill-current" />
              <Star className="w-3 h-3 text-yellow-400 fill-current" />
            </div>
          </div>

          {/* Main Title with Enhanced Styling */}
          <h1 className="text-8xl md:text-9xl font-black tracking-tight mb-6 text-white relative">
            <span className="relative">
              AUDIT Guardian
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500/20 via-purple-500/20 to-indigo-500/20 blur-3xl"></div>
            </span>
          </h1>
          
          {/* Enhanced Subtitle */}
          <p className="text-2xl md:text-3xl text-white/80 max-w-4xl mx-auto mb-8 font-light leading-relaxed">
            Precision audit platform for clear insights and rapid action.
          </p>
          
          {/* Enhanced Quote */}
          <div className="relative mb-8">
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent rounded-2xl"></div>
            <div className="relative z-10 bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 shadow-2xl">
              <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto italic">
                "Audit what matters. Improve what counts." — AUDIT Guardian
              </p>
            </div>
          </div>

          {/* Enhanced Stats */}
          <div className="grid grid-cols-3 gap-8 max-w-3xl mx-auto mb-12">
            <div className="text-center group">
              <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl p-6 shadow-xl hover:bg-white/15 transition-all duration-300 transform hover:scale-105">
                <div className="text-3xl md:text-4xl font-bold text-white mb-2 group-hover:text-blue-300 transition-colors">140+</div>
                <div className="text-sm text-white/60">Technical Checks</div>
              </div>
            </div>
            <div className="text-center group">
              <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl p-6 shadow-xl hover:bg-white/15 transition-all duration-300 transform hover:scale-105">
                <div className="text-3xl md:text-4xl font-bold text-white mb-2 group-hover:text-green-300 transition-colors">99%</div>
                <div className="text-sm text-white/60">Accuracy Rate</div>
              </div>
            </div>
            <div className="text-center group">
              <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl p-6 shadow-xl hover:bg-white/15 transition-all duration-300 transform hover:scale-105">
                <div className="text-3xl md:text-4xl font-bold text-white mb-2 group-hover:text-purple-300 transition-colors">24/7</div>
                <div className="text-sm text-white/60">Support</div>
              </div>
            </div>
          </div>

          {/* Enhanced CTA */}
          <div className="flex flex-col sm:flex-row items-center justify-center space-y-6 sm:space-y-0 sm:space-x-8">
            <a 
              href="#seo" 
              className="inline-flex items-center text-white/80 hover:text-white transition-all duration-300 group bg-white/10 backdrop-blur-sm border border-white/20 px-8 py-4 rounded-2xl hover:bg-white/15 hover:border-blue-400 shadow-xl hover:shadow-blue-500/25"
            >
              <span className="mr-3 text-sm uppercase tracking-widest font-medium">Scroll Down To Continue</span>
              <ChevronDown className="w-5 h-5 group-hover:translate-y-1 transition-transform duration-300" />
            </a>
            
            {!isConnected && (
              <button
                onClick={connectWallet}
                className="bg-white text-slate-900 px-8 py-4 rounded-2xl font-bold hover:bg-gray-100 transition-all duration-300 transform hover:scale-105 shadow-2xl hover:shadow-white/25 relative overflow-hidden group"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent group-hover:animate-shimmer"></div>
                <span className="relative z-10">Get Started Now</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Bottom Gradient */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-gray-50 to-transparent"></div>
    </header>
  );
};

export default Header;
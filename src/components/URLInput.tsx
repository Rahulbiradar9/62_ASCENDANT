import React, { useState, useEffect } from 'react';
import { Search, Globe, AlertCircle, Settings, Play, Clock, CheckCircle, Wallet, Shield } from 'lucide-react';

interface URLInputProps {
  onAudit: (url: string) => void;
  isLoading: boolean;
}

const URLInput: React.FC<URLInputProps> = ({ onAudit, isLoading }) => {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const [auditType, setAuditType] = useState('full');
  const [isConnected, setIsConnected] = useState(false);
  const [walletAddress, setWalletAddress] = useState('');

  // Check for existing wallet connection
  useEffect(() => {
    const savedWallet = localStorage.getItem('auditGuardianWallet');
    if (savedWallet) {
      setWalletAddress(savedWallet);
      setIsConnected(true);
    }
  }, []);

  const validateURL = (url: string): boolean => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!isConnected) {
      setError('Please connect your MetaMask wallet to start an audit');
      return;
    }

    if (!url.trim()) {
      setError('Please enter a website URL');
      return;
    }

    const formattedURL = url.startsWith('http') ? url : `https://${url}`;
    
    if (!validateURL(formattedURL)) {
      setError('Please enter a valid URL (e.g., https://example.com)');
      return;
    }

    onAudit(formattedURL);
  };

  const connectWallet = async () => {
    if (typeof window === 'undefined' || !window.ethereum || !window.ethereum.isMetaMask) {
      alert('Please install MetaMask to use AUDIT Guardian');
      return;
    }

    try {
      const accounts = await window.ethereum.request({
        method: 'eth_requestAccounts',
      });
      
      if (accounts.length > 0) {
        setWalletAddress(accounts[0]);
        setIsConnected(true);
        localStorage.setItem('auditGuardianWallet', accounts[0]);
        setError('');
      }
    } catch (error) {
      console.error('Error connecting to MetaMask:', error);
      alert('Failed to connect to MetaMask. Please try again.');
    }
  };

  const formatAddress = (address: string) => {
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 -mt-8 relative z-20">
      <div className="bg-white rounded-2xl shadow-xl p-10 border border-gray-200">
        <div className="text-center mb-10">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
            Start Your AUDIT Guardian Analysis
          </h2>
          
          <p className="text-lg text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Enter your website URL to get a comprehensive technical SEO analysis with 140+ checks. 
            AUDIT Guardian will identify issues that impact your search rankings and user experience.
          </p>
        </div>

        {/* Wallet Connection Status */}
        <div className="mb-8">
          {isConnected ? (
            <div className="bg-green-50 border border-green-200 rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="bg-green-100 p-3 rounded-lg">
                    <Shield className="w-6 h-6 text-green-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-green-800">Wallet Connected</h3>
                    <p className="text-green-600 text-sm">You're ready to start your audit</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2 bg-white px-3 py-2 rounded-lg border border-green-200">
                  <Wallet className="w-4 h-4 text-green-600" />
                  <span className="text-sm text-green-700 font-mono">{formatAddress(walletAddress)}</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="bg-blue-100 p-3 rounded-lg">
                    <Wallet className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-blue-800">Connect Your Wallet</h3>
                    <p className="text-blue-600 text-sm">Connect MetaMask to start your audit</p>
                  </div>
                </div>
                <button
                  onClick={connectWallet}
                  className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold flex items-center space-x-2"
                >
                  <Wallet className="w-5 h-5" />
                  <span>Connect MetaMask</span>
                </button>
              </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* URL Input */}
          <div className="space-y-4">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Website URL
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <Globe className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://example.com"
                className="w-full pl-12 pr-4 py-4 text-lg border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-300 bg-white hover:border-gray-300"
                disabled={isLoading || !isConnected}
              />
            </div>
          </div>

          {/* Audit Type Selection */}
          <div className="space-y-4">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Audit Type
            </label>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div 
                className={`p-4 rounded-xl border-2 cursor-pointer transition-all duration-300 ${
                  auditType === 'full' 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                } ${!isConnected ? 'opacity-50 cursor-not-allowed' : ''}`}
                onClick={() => isConnected && setAuditType('full')}
              >
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-lg ${auditType === 'full' ? 'bg-blue-100' : 'bg-gray-100'}`}>
                    <Search className={`w-5 h-5 ${auditType === 'full' ? 'text-blue-600' : 'text-gray-600'}`} />
                  </div>
                  <div>
                    <div className="font-semibold text-gray-900">Full Audit</div>
                    <div className="text-sm text-gray-600">140+ checks</div>
                  </div>
                </div>
              </div>
              
              <div 
                className={`p-4 rounded-xl border-2 cursor-pointer transition-all duration-300 ${
                  auditType === 'quick' 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                } ${!isConnected ? 'opacity-50 cursor-not-allowed' : ''}`}
                onClick={() => isConnected && setAuditType('quick')}
              >
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-lg ${auditType === 'quick' ? 'bg-blue-100' : 'bg-gray-100'}`}>
                    <Clock className={`w-5 h-5 ${auditType === 'quick' ? 'text-blue-600' : 'text-gray-600'}`} />
                  </div>
                  <div>
                    <div className="font-semibold text-gray-900">Quick Scan</div>
                    <div className="text-sm text-gray-600">50+ checks</div>
                  </div>
                </div>
              </div>
              
              <div 
                className={`p-4 rounded-xl border-2 cursor-pointer transition-all duration-300 ${
                  auditType === 'custom' 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                } ${!isConnected ? 'opacity-50 cursor-not-allowed' : ''}`}
                onClick={() => isConnected && setAuditType('custom')}
              >
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-lg ${auditType === 'custom' ? 'bg-blue-100' : 'bg-gray-100'}`}>
                    <Settings className={`w-5 h-5 ${auditType === 'custom' ? 'text-blue-600' : 'text-gray-600'}`} />
                  </div>
                  <div>
                    <div className="font-semibold text-gray-900">Custom</div>
                    <div className="text-sm text-gray-600">Select checks</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {error && (
            <div className="flex items-center space-x-4 text-red-600 bg-red-50 p-4 rounded-xl border border-red-200">
              <AlertCircle className="w-5 h-5 flex-shrink-0" />
              <span className="text-sm font-medium">{error}</span>
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading || !isConnected}
            className="w-full bg-blue-600 text-white font-semibold py-4 px-8 rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-200 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-[1.02] active:scale-[0.98] flex items-center justify-center space-x-3"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                <span>Running AUDIT Guardian Analysis...</span>
              </>
            ) : !isConnected ? (
              <>
                <Wallet className="w-5 h-5" />
                <span>Connect Wallet to Start</span>
              </>
            ) : (
              <>
                <Play className="w-5 h-5" />
                <span>Start AUDIT Guardian Analysis</span>
              </>
            )}
          </button>
        </form>

        {/* Features List */}
        <div className="mt-12 pt-8 border-t border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex items-center space-x-3">
              <CheckCircle className="w-5 h-5 text-green-600" />
              <span className="text-sm text-gray-600">140+ Technical Checks</span>
            </div>
            <div className="flex items-center space-x-3">
              <CheckCircle className="w-5 h-5 text-green-600" />
              <span className="text-sm text-gray-600">Detailed Reports</span>
            </div>
            <div className="flex items-center space-x-3">
              <CheckCircle className="w-5 h-5 text-green-600" />
              <span className="text-sm text-gray-600">Actionable Insights</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default URLInput;
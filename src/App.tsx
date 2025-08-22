import React, { useState } from 'react';
import Header from './components/Header';
import FeatureSection from './components/FeatureSection';
import Footer from './components/Footer';
import { CheckCircle, RefreshCw } from 'lucide-react';

function App() {
  const [auditComplete, setAuditComplete] = useState(false);
  const [auditedUrl, setAuditedUrl] = useState('');

  const handleNewAudit = () => {
    setAuditComplete(false);
    setAuditedUrl('');
  };

  if (auditComplete) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="bg-white rounded-lg shadow-lg p-8 border border-gray-200 text-center">
            <div className="w-16 h-16 bg-blue-600 rounded-lg mx-auto mb-6 flex items-center justify-center">
              <CheckCircle className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              AUDIT Guardian Analysis Complete!
            </h1>
            <p className="text-gray-600 mb-6">
              Your comprehensive SEO analysis for <span className="text-blue-600 font-medium">{auditedUrl}</span> is ready.
            </p>
            
            <div className="bg-gray-50 rounded-lg p-6 mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">What AUDIT Guardian analyzed:</h3>
              <ul className="text-left space-y-2 text-gray-600">
                <li className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-600" />
                  <span>Technical SEO analysis</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-600" />
                  <span>On-page optimization check</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-600" />
                  <span>Content quality assessment</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-600" />
                  <span>Mobile-friendliness test</span>
                </li>
              </ul>
            </div>
            
            <button
              onClick={handleNewAudit}
              className="bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors duration-200 flex items-center space-x-2 mx-auto"
            >
              <RefreshCw className="w-5 h-5" />
              <span>Audit Another Website</span>
            </button>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <FeatureSection />
      <Footer />
    </div>
  );
}

export default App;
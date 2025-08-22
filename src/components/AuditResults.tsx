import React from 'react';
import { Search, FileText, BarChart3, Users, Download, RefreshCw, AlertTriangle, CheckCircle, Info, Clock } from 'lucide-react';
import AuditCard from './AuditCard';

interface AuditResultsProps {
  url: string;
  onNewAudit: () => void;
}

const AuditResults: React.FC<AuditResultsProps> = ({ url, onNewAudit }) => {
  // Mock SEO audit data - in a real app, this would come from actual website analysis
  const auditData = {
    technical: {
      score: 78,
      issues: [
        {
          title: 'Missing Meta Description',
          severity: 'medium' as const,
          description: 'Page is missing meta description tag',
          recommendation: 'Add descriptive meta description (150-160 characters) for better search results'
        },
        {
          title: 'No Alt Text on Images',
          severity: 'medium' as const,
          description: '8 images are missing alt attributes',
          recommendation: 'Add descriptive alt text to all images for better accessibility and SEO'
        },
        {
          title: 'Missing H1 Tag',
          severity: 'low' as const,
          description: 'Page is missing H1 heading tag',
          recommendation: 'Add a single, descriptive H1 tag to improve page structure'
        }
      ]
    },
    performance: {
      score: 65,
      issues: [
        {
          title: 'Large Image Files',
          severity: 'high' as const,
          description: 'Images are not optimized, causing slow load times',
          recommendation: 'Compress images using WebP format and implement lazy loading'
        },
        {
          title: 'Unused CSS',
          severity: 'medium' as const,
          description: '45% of CSS is unused on this page',
          recommendation: 'Remove unused CSS rules and consider code splitting'
        },
        {
          title: 'No Caching Headers',
          severity: 'medium' as const,
          description: 'Static resources lack proper cache headers',
          recommendation: 'Implement cache-control headers for static assets'
        }
      ]
    },
    mobile: {
      score: 82,
      issues: [
        {
          title: 'Mobile Usability Issues',
          severity: 'medium' as const,
          description: 'Some elements may be difficult to use on mobile',
          recommendation: 'Test and optimize for mobile user experience'
        },
        {
          title: 'Slow Mobile Loading',
          severity: 'low' as const,
          description: 'Page loads slowly on mobile devices',
          recommendation: 'Optimize images and resources for mobile performance'
        }
      ]
    },
    security: {
      score: 71,
      issues: [
        {
          title: 'Missing Security Headers',
          severity: 'high' as const,
          description: 'Security headers are not properly configured',
          recommendation: 'Implement Content Security Policy and other security headers'
        },
        {
          title: 'Mixed Content Warning',
          severity: 'medium' as const,
          description: 'Some resources are loaded over HTTP instead of HTTPS',
          recommendation: 'Update all resource URLs to use HTTPS protocol'
        }
      ]
    }
  };

  const overallScore = Math.round(
    (auditData.technical.score + auditData.performance.score + auditData.mobile.score + auditData.security.score) / 4
  );

  const getOverallScoreColor = () => {
    if (overallScore >= 80) return 'text-green-600';
    if (overallScore >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const handleExportReport = () => {
    // In a real app, this would generate and download a PDF report
    alert('Export functionality would generate a detailed AUDIT Guardian report here');
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Results Header */}
      <div className="bg-white rounded-3xl shadow-2xl p-10 border border-gray-100 mb-12">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-3">
              AUDIT Guardian Results
            </h2>
            <p className="text-gray-600 break-all font-medium">{url}</p>
            <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
              <div className="flex items-center space-x-1">
                <Clock className="w-4 h-4" />
                <span>Completed 2 minutes ago</span>
              </div>
              <div className="flex items-center space-x-1">
                <CheckCircle className="w-4 h-4 text-green-600" />
                <span>140 checks performed by AUDIT Guardian</span>
              </div>
            </div>
          </div>
          <div className="flex space-x-4 mt-6 md:mt-0">
            <button
              onClick={handleExportReport}
              className="flex items-center space-x-3 bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              <Download className="w-5 h-5" />
              <span className="font-semibold">Export AUDIT Guardian Report</span>
            </button>
            <button
              onClick={onNewAudit}
              className="flex items-center space-x-3 bg-gray-600 text-white px-6 py-3 rounded-xl hover:bg-gray-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              <RefreshCw className="w-5 h-5" />
              <span className="font-semibold">New AUDIT Guardian Analysis</span>
            </button>
          </div>
        </div>

        {/* Overall Score */}
        <div className="text-center">
          <div className={`text-6xl font-bold mb-4 ${getOverallScoreColor()}`}>
            {overallScore}
          </div>
          <p className="text-2xl text-gray-600 mb-6 font-light">AUDIT Guardian Health Score</p>
          <div className="w-48 h-3 bg-gray-200 rounded-full mx-auto overflow-hidden">
            <div
              className={`h-3 rounded-full transition-all duration-1000 ease-out ${
                overallScore >= 80 ? 'bg-gradient-to-r from-green-500 to-green-600' : 
                overallScore >= 60 ? 'bg-gradient-to-r from-yellow-500 to-yellow-600' : 
                'bg-gradient-to-r from-red-500 to-red-600'
              } shadow-sm`}
              style={{ width: `${overallScore}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
        <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-lg">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-red-100 rounded-lg">
              <AlertTriangle className="w-6 h-6 text-red-600" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">12</div>
              <div className="text-sm text-gray-600">Critical Issues</div>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-lg">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-yellow-100 rounded-lg">
              <Info className="w-6 h-6 text-yellow-600" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">28</div>
              <div className="text-sm text-gray-600">Warnings</div>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-lg">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-green-100 rounded-lg">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">95</div>
              <div className="text-sm text-gray-600">Passed Checks</div>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-lg">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-blue-100 rounded-lg">
              <BarChart3 className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">135</div>
              <div className="text-sm text-gray-600">Total Checks</div>
            </div>
          </div>
        </div>
      </div>

      {/* Audit Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <AuditCard
          title="Technical SEO"
          icon={Search}
          score={auditData.technical.score}
          issues={auditData.technical.issues}
          color="blue"
        />
        <AuditCard
          title="Performance"
          icon={BarChart3}
          score={auditData.performance.score}
          issues={auditData.performance.issues}
          color="green"
        />
        <AuditCard
          title="Mobile Optimization"
          icon={Users}
          score={auditData.mobile.score}
          issues={auditData.mobile.issues}
          color="yellow"
        />
        <AuditCard
          title="Security"
          icon={FileText}
          score={auditData.security.score}
          issues={auditData.security.issues}
          color="red"
        />
      </div>

      {/* Summary and Recommendations */}
      <div className="bg-white rounded-3xl shadow-2xl p-10 border border-gray-100">
        <h3 className="text-2xl md:text-3xl font-bold text-gray-900 mb-8">
          AUDIT Guardian Key Recommendations
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-red-50 border-l-4 border-red-400 p-6 rounded-r-xl hover:shadow-lg transition-shadow duration-300">
            <h4 className="text-xl font-bold text-red-800 mb-4">
              🚨 Critical Issues (12)
            </h4>
            <ul className="text-red-700 space-y-3 text-sm">
              <li className="flex items-start space-x-2">
                <span className="text-red-500 mt-1">•</span>
                <span>Implement security headers (CSP, HSTS)</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-red-500 mt-1">•</span>
                <span>Optimize large image files for faster loading</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-red-500 mt-1">•</span>
                <span>Fix mobile usability issues</span>
              </li>
            </ul>
          </div>
          <div className="bg-blue-50 border-l-4 border-blue-400 p-6 rounded-r-xl hover:shadow-lg transition-shadow duration-300">
            <h4 className="text-xl font-bold text-blue-800 mb-4">
              💡 Quick Wins (28)
            </h4>
            <ul className="text-blue-700 space-y-3 text-sm">
              <li className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span>Add meta descriptions to improve SEO</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span>Include alt text for all images</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span>Remove unused CSS to improve performance</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuditResults;
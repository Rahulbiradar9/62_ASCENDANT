import React from 'react';
import { DivideIcon as LucideIcon } from 'lucide-react';
import ProgressBar from './ProgressBar';

interface Issue {
  title: string;
  severity: 'high' | 'medium' | 'low';
  description: string;
  recommendation: string;
}

interface AuditCardProps {
  title: string;
  icon: LucideIcon;
  score: number;
  issues: Issue[];
  color: 'green' | 'yellow' | 'red' | 'blue';
}

const AuditCard: React.FC<AuditCardProps> = ({ title, icon: Icon, score, issues, color }) => {
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'text-red-600 bg-red-50 border-red-200';
      case 'medium':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      default:
        return 'text-blue-600 bg-blue-50 border-blue-200';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'high':
        return '🔴';
      case 'medium':
        return '🟡';
      default:
        return '🔵';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center space-x-3 mb-4">
        <div className={`p-2 rounded-lg bg-${color}-50`}>
          <Icon className={`w-5 h-5 text-${color}-600`} />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          <p className="text-sm text-gray-600">
            {issues.length} issue{issues.length !== 1 ? 's' : ''} found
          </p>
        </div>
      </div>

      <div className="mb-4">
        <ProgressBar score={score} label="Score" color={color} />
      </div>

      <div className="space-y-3">
        {issues.slice(0, 3).map((issue, index) => (
          <div
            key={index}
            className={`p-3 rounded-lg border ${getSeverityColor(issue.severity)}`}
          >
            <div className="flex items-start space-x-2">
              <span className="text-sm">{getSeverityIcon(issue.severity)}</span>
              <div className="flex-1 min-w-0">
                <h4 className="font-medium text-gray-900 mb-1 text-sm">
                  {issue.title}
                </h4>
                <p className="text-xs text-gray-600 mb-2">
                  {issue.description}
                </p>
                <div className="bg-white p-2 rounded border border-gray-200">
                  <p className="text-xs font-medium text-gray-700 mb-1">
                    💡 Recommendation:
                  </p>
                  <p className="text-xs text-gray-600">
                    {issue.recommendation}
                  </p>
                </div>
              </div>
            </div>
          </div>
        ))}
        
        {issues.length > 3 && (
          <div className="text-center">
            <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
              View {issues.length - 3} more issues
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default AuditCard;
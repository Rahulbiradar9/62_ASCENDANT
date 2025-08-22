import React from 'react';

interface ProgressBarProps {
  score: number;
  label: string;
  color?: 'green' | 'yellow' | 'red' | 'blue';
}

const ProgressBar: React.FC<ProgressBarProps> = ({ score, label, color = 'blue' }) => {
  const getColorClasses = () => {
    switch (color) {
      case 'green':
        return 'bg-green-500';
      case 'yellow':
        return 'bg-yellow-500';
      case 'red':
        return 'bg-red-500';
      default:
        return 'bg-blue-500';
    }
  };

  const getScoreColor = () => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center">
        <span className="text-sm font-medium text-gray-700">{label}</span>
        <span className={`text-sm font-bold ${getScoreColor()}`}>
          {score}/100
        </span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className={`h-2 rounded-full transition-all duration-1000 ease-out ${getColorClasses()}`}
          style={{ width: `${score}%` }}
        ></div>
      </div>
    </div>
  );
};

export default ProgressBar;
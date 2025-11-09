import React from 'react';

const EntityCard = ({ icon, title, items, color }) => {
  const colorClasses = {
    blue: 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800',
    purple: 'bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-800',
    green: 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300 border-green-200 dark:border-green-800'
  };

  return (
    <div className={`p-4 rounded-lg border-2 transition-colors ${colorClasses[color]}`}>
      <div className="flex items-center gap-2 mb-3">
        {icon}
        <h5 className="font-semibold">{title}</h5>
      </div>
      <ul className="space-y-1">
        {items.slice(0, 5).map((item, index) => (
          <li key={index} className="text-sm">• {item}</li>
        ))}
      </ul>
    </div>
  );
};

export default EntityCard;
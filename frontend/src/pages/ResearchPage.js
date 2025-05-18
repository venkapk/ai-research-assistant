import React from 'react';
import { useApp } from '../contexts/AppContext';
import { 
  LightbulbIcon, 
  DocumentIcon, 
  PeopleIcon, 
  CurrencyIcon, 
  NewsIcon, 
  InsightIcon 
} from '../components/icons';

const ResearchSection = ({ title, items, icon, bgColor = false }) => {
  const Icon = icon;
  
  return (
    <div className={`${bgColor ? 'bg-gray-50' : ''} px-4 py-5 sm:px-6`}>
      <div className="flex items-center mb-4">
        <div className={`bg-${bgColor ? 'white' : 'gray-50'} rounded-md p-2 mr-3`}>
          <Icon />
        </div>
        <h3 className="text-lg font-medium leading-6 text-gray-900">{title}</h3>
      </div>
      {items.length > 0 ? (
        <ul className={`mt-3 ${
          title === 'Projects & Publications' || title === 'Funding History' || title === 'Strategic Insights' 
            ? 'space-y-3' 
            : 'grid grid-cols-1 gap-3 sm:gap-4 sm:grid-cols-2'
        }`}>
          {items.map((item, index) => (
            <li 
              key={index} 
              className={`text-sm text-gray-700 ${
                title === 'Projects & Publications' || title === 'Funding History' || title === 'Strategic Insights'
                  ? 'bg-white shadow-sm'
                  : 'bg-gray-50'
              } px-4 py-3 rounded-md`}
            >
              {item}
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-gray-500 italic">No data available</p>
      )}
    </div>
  );
};

const ResearchPage = () => {
  const { verificationResult, researchResult } = useApp();

  if (!researchResult) {
    return (
      <div className="bg-white shadow overflow-hidden sm:rounded-lg p-6 text-center">
        <p className="text-gray-500">No research data available. Please verify an entity first.</p>
      </div>
    );
  }

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
      <div className="px-4 py-5 sm:px-6">
        <h2 className="text-lg leading-6 font-medium text-gray-900">Research Results</h2>
        <p className="mt-1 text-sm text-gray-500">
          Comprehensive research for {verificationResult?.full_name || 'the entity'}
        </p>
      </div>

      <div className="border-t border-gray-200">
        <ResearchSection 
          title="Research Focus" 
          items={researchResult.research_focus} 
          icon={LightbulbIcon} 
        />
        
        <ResearchSection 
          title="Projects & Publications" 
          items={researchResult.projects_publications} 
          icon={DocumentIcon} 
          bgColor
        />
        
        <ResearchSection 
          title="Institutional Connections" 
          items={researchResult.institutional_connections} 
          icon={PeopleIcon} 
        />
        
        <ResearchSection 
          title="Funding History" 
          items={researchResult.funding_history} 
          icon={CurrencyIcon} 
          bgColor
        />
        
        <ResearchSection 
          title="Public Mentions" 
          items={researchResult.public_mentions} 
          icon={NewsIcon} 
        />
        
        <ResearchSection 
          title="Strategic Insights" 
          items={researchResult.strategic_insights} 
          icon={InsightIcon} 
          bgColor
        />
      </div>
    </div>
  );
};

export default ResearchPage;
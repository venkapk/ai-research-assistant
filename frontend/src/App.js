import React from 'react';
import { AppProvider, useApp } from './contexts/AppContext';
import Header from './components/Header';
import Footer from './components/Footer';
import VerifyPage from './pages/VerifyPage';
import ResearchPage from './pages/ResearchPage';

const MainContent = () => {
  const { activePage, researchResult } = useApp();
  
  return (
    <div className="min-h-screen bg-gray-50">
      <Header 
        activePage={activePage} 
        setActivePage={useApp().setActivePage} 
        hasResearchResults={!!researchResult}
      />
      
      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activePage === 'verify' ? <VerifyPage /> : <ResearchPage />}
      </main>
      
      <Footer />
    </div>
  );
};

const App = () => {
  return (
    <AppProvider>
      <MainContent />
    </AppProvider>
  );
};

export default App;
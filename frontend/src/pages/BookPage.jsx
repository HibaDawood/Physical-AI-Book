// frontend/src/pages/BookPage.jsx
import React, { useState, useEffect } from 'react';
import BookNavigation from '../components/BookNavigation/BookNavigation';
import ChapterDisplay from '../components/ChapterDisplay/ChapterDisplay';
import ChatWidget from '../components/ChatWidget/ChatWidget';
import LanguageToggle from '../components/LanguageToggle/LanguageToggle';
import apiService from '../services/api';
import './BookPage.css';

const BookPage = () => {
  const [chapters, setChapters] = useState([]);
  const [currentChapter, setCurrentChapter] = useState(null);
  const [selectedText, setSelectedText] = useState('');
  const [language, setLanguage] = useState('en');

  // Load chapters on component mount
  useEffect(() => {
    loadChapters();
  }, [language]);

  const loadChapters = async () => {
    try {
      const chapterData = await apiService.getBookChapters();
      setChapters(chapterData);
      
      // Load the first chapter if available
      if (chapterData && chapterData.length > 0) {
        loadChapterContent(chapterData[0]);
      }
    } catch (error) {
      console.error('Error loading chapters:', error);
    }
  };

  const loadChapterContent = async (chapter) => {
    try {
      const content = await apiService.getBookContent(chapter.id);
      setCurrentChapter(content);
    } catch (error) {
      console.error('Error loading chapter content:', error);
    }
  };

  const handleChapterChange = (chapter) => {
    loadChapterContent(chapter);
  };

  const handleTextSelect = (text) => {
    setSelectedText(text);
  };

  const handleLanguageChange = (newLanguage) => {
    setLanguage(newLanguage);
    // In a real implementation, we would update content based on language
  };

  return (
    <div className="book-page">
      <header className="book-header">
        <h1>Physical AI Book</h1>
        <LanguageToggle 
          currentLanguage={language} 
          onLanguageChange={handleLanguageChange} 
        />
      </header>

      <div className="book-content-area">
        <div className="navigation-panel">
          <BookNavigation 
            chapters={chapters} 
            currentChapter={currentChapter}
            onChapterChange={handleChapterChange} 
          />
        </div>

        <div className="chapter-panel">
          <ChapterDisplay 
            content={currentChapter}
            onTextSelect={handleTextSelect}
          />
        </div>
      </div>

      <ChatWidget selectedText={selectedText} />
    </div>
  );
};

export default BookPage;
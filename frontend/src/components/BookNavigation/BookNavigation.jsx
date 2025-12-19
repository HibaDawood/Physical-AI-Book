// frontend/src/components/BookNavigation/BookNavigation.jsx
import React, { useState, useEffect } from 'react';
import './BookNavigation.css';

const BookNavigation = ({ chapters, currentChapter, onChapterChange }) => {
  const [expandedChapters, setExpandedChapters] = useState({});

  const toggleChapter = (chapterId) => {
    setExpandedChapters(prev => ({
      ...prev,
      [chapterId]: !prev[chapterId]
    }));
  };

  const renderChapterTree = (chaptersList, level = 0) => {
    if (!chaptersList || chaptersList.length === 0) return null;

    return (
      <ul className={`chapter-list level-${level}`}>
        {chaptersList.map(chapter => {
          const hasChildren = chapter.children && chapter.children.length > 0;
          const isExpanded = expandedChapters[chapter.id] || false;

          return (
            <li key={chapter.id} className="chapter-item">
              <div 
                className={`chapter-link ${currentChapter?.id === chapter.id ? 'active' : ''}`}
                onClick={() => {
                  if (hasChildren) {
                    toggleChapter(chapter.id);
                  } else {
                    onChapterChange(chapter);
                  }
                }}
              >
                <span className="chapter-title">{chapter.title}</span>
                {hasChildren && (
                  <span className={`expand-icon ${isExpanded ? 'expanded' : ''}`}>
                    {isExpanded ? '▼' : '▶'}
                  </span>
                )}
              </div>
              
              {hasChildren && isExpanded && (
                <div className="sub-chapters">
                  {renderChapterTree(chapter.children, level + 1)}
                </div>
              )}
            </li>
          );
        })}
      </ul>
    );
  };

  return (
    <div className="book-navigation">
      <h3>Book Contents</h3>
      {renderChapterTree(chapters)}
    </div>
  );
};

export default BookNavigation;
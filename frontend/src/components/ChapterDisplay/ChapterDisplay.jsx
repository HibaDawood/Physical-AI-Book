// frontend/src/components/ChapterDisplay/ChapterDisplay.jsx
import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './ChapterDisplay.css';

const ChapterDisplay = ({ content, onTextSelect }) => {
  const [selectedText, setSelectedText] = useState('');

  const handleTextSelection = () => {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
      setSelectedText(selectedText);
    }
  };

  const handleAskAboutSelection = () => {
    if (selectedText) {
      onTextSelect && onTextSelect(selectedText);
      // Clear selection after sending
      window.getSelection().removeAllRanges();
      setSelectedText('');
    }
  };

  if (!content) {
    return (
      <div className="chapter-display placeholder">
        <p>Select a chapter from the navigation to begin reading.</p>
      </div>
    );
  }

  return (
    <div className="chapter-display">
      <div className="chapter-header">
        <h1>{content.title}</h1>
        {selectedText && (
          <div className="selection-actions">
            <button className="ask-selection-btn" onClick={handleAskAboutSelection}>
              Ask AI about this text
            </button>
          </div>
        )}
      </div>

      <div className="chapter-content" onMouseUp={handleTextSelection}>
        <ReactMarkdown className="markdown-content">
          {content.content}
        </ReactMarkdown>
      </div>

      {content.metadata && Object.keys(content.metadata).length > 0 && (
        <div className="chapter-meta">
          <h4>Chapter Information</h4>
          <ul>
            {Object.entries(content.metadata).map(([key, value]) => (
              <li key={key}>
                <strong>{key}:</strong> {typeof value === 'object' ? JSON.stringify(value) : String(value)}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ChapterDisplay;
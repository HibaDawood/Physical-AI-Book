// frontend/src/components/LanguageToggle/LanguageToggle.jsx
import React from 'react';
import './LanguageToggle.css';

const LanguageToggle = ({ currentLanguage, onLanguageChange }) => {
  const languages = [
    { code: 'en', name: 'English' },
    { code: 'ur', name: 'Urdu' }
  ];

  return (
    <div className="language-toggle">
      <label htmlFor="language-select">Language:</label>
      <select 
        id="language-select"
        value={currentLanguage} 
        onChange={(e) => onLanguageChange(e.target.value)}
        className="language-select"
      >
        {languages.map(lang => (
          <option key={lang.code} value={lang.code}>
            {lang.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default LanguageToggle;
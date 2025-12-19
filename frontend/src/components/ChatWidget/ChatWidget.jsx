// frontend/src/components/ChatWidget/ChatWidget.jsx
import React, { useState, useEffect } from 'react';
import { FiMessageSquare, FiX, FiSend, FiMinimize2, FiMaximize2 } from 'react-icons/fi';
import './ChatWidget.css';
import apiService from '../../services/api';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      setIsMinimized(false);
    }
  };

  const toggleMinimize = () => {
    setIsMinimized(!isMinimized);
  };

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { text: inputValue, sender: 'user', timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get response from backend
      const response = await apiService.chatQuery({ 
        query: inputValue,
        language: 'en'
      });

      const botMessage = { 
        text: response.response_text, 
        sender: 'bot', 
        sources: response.sources || [],
        timestamp: new Date() 
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error getting chat response:', error);
      const errorMessage = { 
        text: 'Sorry, I encountered an error. Please try again.', 
        sender: 'bot', 
        timestamp: new Date() 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Auto scroll to bottom when messages change
  useEffect(() => {
    const chatBody = document.querySelector('.chat-body');
    if (chatBody) {
      chatBody.scrollTop = chatBody.scrollHeight;
    }
  }, [messages]);

  return (
    <div className={`chat-widget-container ${isOpen ? 'open' : ''}`}>
      {!isOpen ? (
        <button className="chat-toggle-btn" onClick={toggleChat}>
          <FiMessageSquare size={24} />
        </button>
      ) : (
        <div className={`chat-widget ${isMinimized ? 'minimized' : ''}`}>
          <div className="chat-header">
            <div className="chat-header-controls">
              <button className="chat-minimize-btn" onClick={toggleMinimize}>
                {isMinimized ? <FiMaximize2 /> : <FiMinimize2 />}
              </button>
              <button className="chat-close-btn" onClick={toggleChat}>
                <FiX />
              </button>
            </div>
            <h3>Physical AI Assistant</h3>
          </div>

          {!isMinimized && (
            <>
              <div className="chat-body">
                {messages.length === 0 ? (
                  <div className="chat-welcome">
                    <p>Ask me anything about Physical AI, Robotics, Agentic AI, Sensors, or Edge AI!</p>
                  </div>
                ) : (
                  messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender}`}>
                      <div className="message-text">{msg.text}</div>
                      {msg.sources && msg.sources.length > 0 && (
                        <div className="message-sources">
                          <small>Sources: {msg.sources.map(s => s.title).join(', ')}</small>
                        </div>
                      )}
                    </div>
                  ))
                )}
                {isLoading && (
                  <div className="message bot">
                    <div className="typing-indicator">
                      <div className="typing-dot"></div>
                      <div className="typing-dot"></div>
                      <div className="typing-dot"></div>
                    </div>
                  </div>
                )}
              </div>

              <div className="chat-input-area">
                <textarea
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask about the book content..."
                  disabled={isLoading}
                  rows="2"
                />
                <button 
                  onClick={handleSend} 
                  disabled={!inputValue.trim() || isLoading}
                  className="send-btn"
                >
                  <FiSend />
                </button>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default ChatWidget;
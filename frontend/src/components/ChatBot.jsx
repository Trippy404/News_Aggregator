import React, { useState, useRef, useEffect } from 'react';
import './ChatBot.css';

const ChatBot = () => {
    const [messages, setMessages] = useState([
        { 
            type: 'bot', 
            text: 'Hi! I can answer questions about current news. Ask me anything about markets, economy, or specific companies!' 
        }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [isOpen, setIsOpen] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMessage = input;
        setMessages(prev => [...prev, { type: 'user', text: userMessage }]);
        setInput('');
        setLoading(true);

        try {
            const response = await fetch('http://localhost:8000/api/chat/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: userMessage })
            });

            const data = await response.json();
            
            setMessages(prev => [...prev, { 
                type: 'bot', 
                text: data.answer,
                sources: data.sources
            }]);
        } catch (error) {
            setMessages(prev => [...prev, { 
                type: 'bot', 
                text: 'Sorry, I encountered an error. Please make sure the backend is running.' 
            }]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !loading) {
            sendMessage();
        }
    };

    return (
        <>
            <button className="chat-button" onClick={() => setIsOpen(!isOpen)}>
                💬
            </button>

            {isOpen && (
                <div className="chat-window">
                    <div className="chat-header">
                        <h3>📰 News Assistant</h3>
                        <button onClick={() => setIsOpen(false)}>✕</button>
                    </div>

                    <div className="chat-messages">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`message ${msg.type}`}>
                                <div className="message-content">
                                    <strong>{msg.type === 'user' ? 'You' : 'AI'}:</strong>
                                    <p>{msg.text}</p>
                                    
                                    {msg.sources && msg.sources.length > 0 && (
                                        <div className="sources">
                                            <small>Sources:</small>
                                            {msg.sources.slice(0, 3).map((src, i) => (
                                                <a key={i} href={src.source_url} target="_blank" rel="noopener noreferrer">
                                                    {src.title.substring(0, 50)}...
                                                </a>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                        
                        {loading && (
                            <div className="message bot">
                                <div className="typing-indicator">
                                    <span></span><span></span><span></span>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    <div className="chat-input">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Ask about news..."
                            disabled={loading}
                        />
                        <button onClick={sendMessage} disabled={loading}>
                            Send
                        </button>
                    </div>
                </div>
            )}
        </>
    );
};

export default ChatBot;
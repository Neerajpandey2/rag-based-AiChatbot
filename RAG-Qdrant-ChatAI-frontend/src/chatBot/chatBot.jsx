import React, { useState, useRef, useEffect } from "react";
import { searchQA } from "../Apis/api";
import "./chatBot.css"; // Importing CSS

export default function Chatbot() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello 👋! How can I help you today?" },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const COLLECTION = "CustomAi"; // default collection

  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput(""); // clear input
    setIsTyping(true);

    try {
      const res = await searchQA(COLLECTION, input);
      const botReply =
        res?.human_like_answer || "🤖 Sorry, I couldn't find an answer.";

      setMessages((prev) => [...prev, { sender: "bot", text: botReply }]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "⚠️ Error fetching response" },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">AI Chat Assistant</div>

      {/* Chat messages */}
      <div className="chatbot-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`chat-message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}

        {isTyping && <div className="chat-message bot typing">Thinking...</div>}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="chatbot-input">
        <input
          type="text"
          placeholder="Ask me anything..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}


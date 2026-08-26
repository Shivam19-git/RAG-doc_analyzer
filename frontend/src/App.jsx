import React, { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm"; // 1. Add this import
import {
  Paperclip,
  Send,
  Bot,
  User,
  FileText,
  Loader2,
  Sparkles,
  X
} from "lucide-react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello! I can analyze your documents or answer general questions. Upload a PDF or ask me anything.",
    },
  ]);
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");

  const chatEndRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.type !== "application/pdf") {
      setUploadStatus("Please upload a PDF file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setUploading(true);
    setUploadStatus("Processing and indexing document...");

    try {
      const res = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");

      setUploadedFile(file.name);
      setUploadStatus("Indexed");

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `📁 **${file.name}** has been uploaded and indexed. You can now ask specific questions about it!`,
        },
      ]);
    } catch (err) {
      console.error(err);
      setUploadStatus("Error processing file.");
    } finally {
      setUploading(false);
    }
  };

  const handleSend = async (e) => {
    e?.preventDefault();
    if (!prompt.trim() || loading) return;

    const userMessage = prompt.trim();
    setPrompt("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setLoading(true);

    try {
      const res = await fetch(
        `${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: userMessage }),
      });

      if (!res.ok) throw new Error("Chat request failed");

      const data = await res.json();
      const reply = typeof data === "string" ? data : data.response || data.reply || JSON.stringify(data);

      setMessages((prev) => [...prev, { role: "assistant", content: reply }]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "⚠️ *Error communicating with backend. Please ensure the server is running.*",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="header-title">
          <Sparkles size={20} color="#a8c7fa" />
          <span>RAG Document Analyzer</span>
        </div>
        {uploadedFile && (
          <div className="file-badge">
            <FileText size={14} color="#a8c7fa" />
            <span>{uploadedFile}</span>
            <X
              size={14}
              className="close-icon"
              onClick={() => { setUploadedFile(null); setUploadStatus(""); }}
            />
          </div>
        )}
      </header>

      {/* Main Conversation Stream */}
      <main className="chat-area">
        <div className="message-list">
          {messages.map((msg, index) => (
            <div key={index} className={`message-row ${msg.role}`}>
              {msg.role === "assistant" && (
                <div className="avatar bot">
                  <Bot size={18} color="#a8c7fa" />
                </div>
              )}

              <div className={`message-bubble ${msg.role === "user" ? "user-bubble" : "assistant-bubble"}`}>
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {msg.content}
                </ReactMarkdown>
              </div>

              {msg.role === "user" && (
                <div className="avatar user">
                  <User size={18} color="#e3e3e3" />
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="message-row assistant">
              <div className="avatar bot">
                <Bot size={18} color="#a8c7fa" />
              </div>
              <div className="message-bubble assistant-bubble thinking-bubble">
                <Loader2 size={16} className="spin" color="#a8c7fa" />
                <span>Thinking...</span>
              </div>
            </div>
          )}

          <div ref={chatEndRef} />
        </div>
      </main>

      {/* Floating Bottom Input Bar */}
      <footer className="app-footer">
        <form onSubmit={handleSend} className="input-container">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileUpload}
            accept="application/pdf"
            style={{ display: "none" }}
          />

          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="icon-button"
            title="Upload PDF Document"
            disabled={uploading}
          >
            {uploading ? (
              <Loader2 size={20} color="#a8c7fa" className="spin" />
            ) : (
              <Paperclip size={20} color="#c4c7c5" />
            )}
          </button>

          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            placeholder={uploadedFile ? `Ask anything about ${uploadedFile}...` : "Ask anything or attach a PDF..."}
            className="chat-textarea"
            rows={1}
          />

          <button
            type="submit"
            disabled={!prompt.trim() || loading}
            className={`send-button ${prompt.trim() && !loading ? "active" : "disabled"}`}
          >
            <Send size={18} color="#131314" />
          </button>
        </form>

        <div className="footer-note">
          {uploadStatus && <span className="status-tag">{uploadStatus}</span>}
          <span>LLM-generated responses can vary. Verify technical specifications.</span>
        </div>
      </footer>
    </div>
  );
}
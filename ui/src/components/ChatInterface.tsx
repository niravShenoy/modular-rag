"use client";
// src/components/ChatInterface.tsx
import React, { useState, useEffect } from 'react';
import { Card, CardBody, Input, Button, Divider } from '@heroui/react';

const ChatInterface = () => {
  const [query, setQuery] = useState('');
  const [currentChat, setCurrentChat] = useState<{ query: string; response: string }[]>([]);
  const [history, setHistory] = useState<{ id: string; title: string; messages: { query: string; response: string }[] }[]>([]);
  const [selectedChat, setSelectedChat] = useState<string | null>(null);

  useEffect(() => {
    // Load history from localStorage
    const saved = localStorage.getItem('chatHistory');
    if (saved) setHistory(JSON.parse(saved));
  }, []);

  useEffect(() => {
    // Save to localStorage (MVP; replace with DB API)
    localStorage.setItem('chatHistory', JSON.stringify(history));
  }, [history]);

  const sendQuery = async () => {
    try {
      const res = await fetch('http://localhost:8000/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, history: currentChat.map(h => ({ user: h.query, assistant: h.response })) }),
      });
      const data = await res.json();
      const newMessages = [...currentChat, { query, response: data.response }];
      setCurrentChat(newMessages);

      if (selectedChat) {
        setHistory(history.map(chat => chat.id === selectedChat ? { ...chat, messages: newMessages } : chat));
      } else {
        const newId = Date.now().toString();
        setHistory([...history, { id: newId, title: query.slice(0, 20), messages: newMessages }]);
        setSelectedChat(newId);
      }
      setQuery('');
    } catch (error) {
      // Handle error
    }
  };

  const startNewChat = () => {
    setSelectedChat(null);
    setCurrentChat([]);
  };

  const loadChat = (id: string) => {
    const chat = history.find(h => h.id === id);
    if (chat) {
      setSelectedChat(id);
      setCurrentChat(chat.messages);
    }
  };

  return (
    <div className="flex h-screen">
      <div className="w-1/4 p-4 border-r">
        <Button onPress={startNewChat}>New Chat</Button>
        <ul className="mt-4">
          {history.map(chat => (
            <li key={chat.id} onClick={() => loadChat(chat.id)} className="cursor-pointer p-2 hover:bg-gray-100">
              {chat.title}
            </li>
          ))}
        </ul>
      </div>
      <div className="w-3/4 p-4">
        <Card className="h-full">
          <CardBody className="flex flex-col h-full">
            <div className="flex-1 overflow-y-auto space-y-2">
              {currentChat.map((msg, i) => (
                <div key={i}>
                  <p className="text-right"><strong>You:</strong> {msg.query}</p>
                  <p><strong>AI:</strong> {msg.response}</p>
                </div>
              ))}
            </div>
            <Divider />
            <div className="flex mt-2">
              <Input className="flex-1" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Type your message" />
              <Button onPress={sendQuery}>Send</Button>
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
};

export default ChatInterface;
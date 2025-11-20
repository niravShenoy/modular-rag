"use client";
// src/components/ChatTester.tsx
import React, { useState } from 'react';
import { Card, CardHeader, CardBody, Input, Button } from '@heroui/react';

const ChatTester = () => {
  const [query, setQuery] = useState('');
  const [history, setHistory] = useState<{ query: string; response: string }[]>([]);
  const [response, setResponse] = useState('');

  const sendQuery = async () => {
    try {
      const res = await fetch('http://localhost:8000/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, history: history.map(h => ({ user: h.query, assistant: h.response })) }),
      });
      const data = await res.json();
      console.log(data);
      setResponse(data.response);
      setHistory([...history, { query, response: data.response }]);
      setQuery('');
    } catch (error) {
      setResponse('Error');
    }
  };

  return (
    <Card>
      <CardHeader>Test Chatbot</CardHeader>
      <CardBody className="space-y-4">
        <div className="h-64 overflow-y-auto">
          {history.map((msg, i) => (
            <div key={i}>
              <p><strong>User:</strong> {msg.query}</p>
              <p><strong>AI:</strong> {msg.response}</p>
            </div>
          ))}
          {response && <p><strong>Latest:</strong> {response}</p>}
        </div>
        <Input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Enter query" />
        <Button onPress={sendQuery}>Send</Button>
      </CardBody>
    </Card>
  );
};

export default ChatTester;
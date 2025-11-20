"use client";
// src/app/admin/page.tsx
import React, { useState } from 'react';
import { Card, CardHeader, CardBody, Button, Input, Select, SelectItem, Divider } from '@heroui/react';
import ChatTester from '@/components/ChatTester';
import FileUploadPanel from '@/components/FileUploadPanel';

const embeddingProviders = ['huggingface', 'openai'];
const vectorProviders = ['chroma', 'pinecone', 'weaviate', 'faiss'];
// Add options for other fields similarly

const AdminPage = () => {
  const [config, setConfig] = useState({
    embedding_provider: 'huggingface',
    model_name: 'sentence-transformers/all-MiniLM-L6-v2',
    vector_store_provider: 'chroma',
    chunk_size: 1000,
    chunk_overlap: 200,
    chunking_strategy: 'recursive',
    top_k: 5,
    reranker_model: 'cross-encoder/ms-marco-MiniLM-L-6-v2',
    persist_directory: './data/vector_store',
    collection_name: 'default_collection',
    retrieval_strategy: 'advanced',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setConfig({ ...config, [e.target.name]: e.target.value });
  };

  const updateConfig = async () => {
    try {
      await fetch('http://localhost:8000/v1/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ updates: config }),
      });
      alert('Config updated');
    } catch (error) {
      alert('Error updating config');
    }
  };

  return (
    <div className="p-4">
      <Card>
        <CardHeader>Admin Configuration</CardHeader>
        <CardBody className="space-y-4">
          <Select label="Embedding Provider" name="embedding_provider" value={config.embedding_provider} onChange={handleChange}>
            {embeddingProviders.map((prov) => <SelectItem key={prov}>{prov}</SelectItem>)}
          </Select>
          <Input label="Model Name" name="model_name" value={config.model_name} onChange={handleChange} />
          {/* Add similar for other fields: Select for strategies, Input for numbers/text */}
          <Button onPress={updateConfig}>Update Config</Button>
        </CardBody>
      </Card>
      <Divider className="my-4" />
      <FileUploadPanel />
      <Divider className="my-4" />
      <ChatTester />
    </div>
  );
};

export default AdminPage;
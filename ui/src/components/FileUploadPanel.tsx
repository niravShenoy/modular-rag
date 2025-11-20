"use client";
// src/components/FileUploadPanel.tsx
import React, { useState } from 'react';
import { Card, CardHeader, CardBody, Button, Input, Select, SelectItem } from '@heroui/react';

const collections = ['default_collection']; // Fetch from API later

const FileUploadPanel = () => {
  const [selectedCollection, setSelectedCollection] = useState(collections[0]);
  const [files, setFiles] = useState<FileList | null>(null);
  const [uploadedFiles, setUploadedFiles] = useState<string[]>([]); // Placeholder for list

  const handleUpload = async () => {
    if (!files) return;
    const formData = new FormData();
    Array.from(files).forEach(file => formData.append('files', file));
    try {
      await fetch(`http://localhost:8000/v1/ingest?collection=${selectedCollection}`, { // Assume param for collection
        method: 'POST',
        body: formData,
      });
      alert('Files uploaded');
      // Update uploadedFiles via GET /files?collection=... (placeholder)
    } catch (error) {
      alert('Upload error');
    }
  };

  const handleDelete = (fileName: string) => {
    // Call DELETE /files/{fileName}?collection=... (placeholder)
    alert(`Delete ${fileName}`);
  };

  return (
    <Card>
      <CardHeader>File Upload to Collection</CardHeader>
      <CardBody className="space-y-4">
        <Select label="Collection" value={selectedCollection} onChange={(e) => setSelectedCollection(e.target.value)}>
          {collections.map((col) => <SelectItem key={col}>{col}</SelectItem>)}
        </Select>
        <Input type="file" multiple onChange={(e) => setFiles(e.target.files)} />
        <Button onPress={handleUpload}>Upload</Button>
        <div>
          <h3>Uploaded Files:</h3>
          <ul>
            {uploadedFiles.map((file) => (
              <li key={file}>
                {file} <Button size="sm" onPress={() => handleDelete(file)}>Delete</Button>
              </li>
            ))}
          </ul>
        </div>
      </CardBody>
    </Card>
  );
};

export default FileUploadPanel;
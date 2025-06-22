import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import API from '../services/api';
import type { FileItem } from '../types';

const Dashboard: React.FC = () => {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [search, setSearch] = useState<string>('');
  const [fileUpload, setFileUpload] = useState<File | null>(null);

  const fetchFiles = async () => {
    const { data } = await API.get<FileItem[]>('/files');
    setFiles(data);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFileUpload(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!fileUpload) return;
    const formData = new FormData();
    formData.append('file', fileUpload);
    await API.post('/upload', formData);
    setFileUpload(null);
    fetchFiles();
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  const filtered = files.filter((f) => f.filename.toLowerCase().includes(search.toLowerCase()));

  return (
    <div>
      <div className="flex items-center gap-4 mb-4">
        <input
          type="text"
          placeholder="Search files..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-grow p-2 rounded bg-cream text-dark"
        />
        <input type="file" onChange={handleFileChange} className="text-dark" />
        <button onClick={handleUpload} className="px-4 py-2 bg-dark text-cream rounded">
          Upload
        </button>
      </div>
      <ul className="space-y-2">
        {filtered.map((f) => (
          <li key={f.file_id}>
            <Link to={`/file/${f.file_id}`} className="block p-4 bg-cream rounded shadow hover:bg-dark hover:text-cream">
              {f.filename}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
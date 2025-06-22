import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import API from '../services/api';
import type { QueryReply } from '../types';

const FileDetail: React.FC = () => {
  const { fileId } = useParams<{ fileId: string }>();
  const [history, setHistory] = useState<QueryReply[]>([]);
  const [question, setQuestion] = useState<string>('');
  const [error, setError] = useState<string>('');

  const fetchHistory = async () => {
    const { data } = await API.get<QueryReply[]>('/history', { params: { user_id: 'me', file_id: fileId } });
    setHistory(data);
  };

  useEffect(() => {
    fetchHistory();
  }, [fileId]);

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const { data } = await API.get<{ query: string; response: string }>('/query', { params: { user_id: 'me', file_id: fileId, question } });
      setHistory((prev) => [{ query: data.query, response: data.response }, ...prev]);
      setQuestion('');
    } catch {
      setError('Failed to get answer');
    }
  };

  return (
    <div>
      <div className="space-y-4 mb-6">
        {history.map((h, i) => (
          <div key={i} className="p-4 bg-dark text-cream rounded-lg">
            <p className="font-semibold">Q: {h.query}</p>
            <p>A: {h.response}</p>
          </div>
        ))}
      </div>
      <form onSubmit={handleAsk} className="flex items-center">
        <input
          type="text"
          placeholder="Ask a question..."
          required
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="flex-grow p-2 rounded bg-cream text-dark"
        />
        <button type="submit" className="ml-2 p-2 bg-dark text-cream rounded">Ask</button>
      </form>
      {error && <p className="mt-2 text-red-500">{error}</p>}
    </div>
  );
};

export default FileDetail;
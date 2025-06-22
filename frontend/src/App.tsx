import React, { useEffect, useState } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import FileDetail from './components/FileDetail';

const App: React.FC = () => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const navigate = useNavigate();

 useEffect(() => {
  const publicRoutes = ['/login', '/register'];
  const isPublic = publicRoutes.includes(window.location.pathname);

  if (!token && !isPublic) {
    navigate('/login');
  }
  }, [token, navigate]);

  const handleLogin = (tok: string) => {
    setToken(tok);
    localStorage.setItem('token', tok);
    navigate('/');
  };

  const logout = () => {
    setToken(null);
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#f8f4e3] text-[#1a1a1a]">
      {token && (
        <nav className="p-4 bg-dark text-cream flex justify-between">
          <span className="font-bold">RAG App</span>
          <button onClick={logout} className="hover:underline">Logout</button>
        </nav>
      )}
      <div className="flex-grow container mx-auto p-4">
        <Routes>
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={token ? <Dashboard /> : <Login onLogin={handleLogin} />} />
          <Route path="/file/:fileId" element={token ? <FileDetail /> : <Login onLogin={handleLogin} />} />
        </Routes>
      </div>
    </div>
  );
};

export default App;
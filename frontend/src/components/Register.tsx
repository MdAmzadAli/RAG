import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import API from '../services/api';

const Register: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string>('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await API.post('/auth/register', { email, password });
      navigate('/login');
    } catch {
      setError('Registration failed');
    }
  };

  return (
    <div className="max-w-md mx-auto bg-dark p-8 rounded-2xl shadow-lg text-cream">
      <h2 className="text-2xl mb-4">Register</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="email"
          placeholder="Email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-2 rounded bg-cream text-dark"
        />
        <input
          type="password"
          placeholder="Password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-2 rounded bg-cream text-dark"
        />
        {error && <p className="text-red-500">{error}</p>}
        <button type="submit" className="w-full py-2 bg-cream text-dark rounded hover:opacity-90 hover:cursor-pointer">Register</button>
      </form>
      <p className="mt-4">Already have an account? <Link to="/login" className="underline">Login</Link></p>
    </div>
  );
};

export default Register;
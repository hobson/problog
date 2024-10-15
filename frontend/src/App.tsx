import React, { ReactNode } from 'react';
import Home from './pages/Home';
import Conversations from './pages/Conversations';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { Login, Register } from './components';
import DownloadConversations from './pages/DownloadConversations';

interface PRP {
  children: ReactNode;
}

const PR:React.FC<PRP> = ({ children }) => {
  const username = localStorage.getItem("username");
  return username ? children : <Navigate to="/login" />;
}


const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<PR><Home /></PR>} />
        <Route path='/conversations' element={<PR><Conversations /></PR>} />
        <Route path='/admin/download/conversations' element={<PR><DownloadConversations /></PR>} />
        <Route path='/login' element={<Login />} />
        <Route path='/register' element={<Register />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;

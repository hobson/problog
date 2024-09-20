import React from 'react';
import Home from './pages/Home';
import Conversations from './pages/Conversations';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/conversations' element={<Conversations />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;

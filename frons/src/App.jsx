import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage'; 
import NovelsPage from './pages/NovelsPage'; 
import UpdatedNovelsPage from './pages/UpdatedNovelsPage'; 
import SearchPage from './pages/SearchPage'; 
import LogIn from './pages/LogIn';
import SignIn from './pages/SignIn';
import styles from './App.module.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/novels" element={<NovelsPage />} />
        <Route path="/updated-novels" element={<UpdatedNovelsPage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/login" element={<LogIn />} />
        <Route path="/signin" element={<SignIn />} />
      </Routes>
    </Router>
  );
}

export default App;

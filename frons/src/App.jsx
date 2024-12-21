import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage'; 
import NovelsPage from './pages/NovelsPage'; 
import UpdatedNovelsPage from './pages/UpdatedNovelsPage'; 
import SearchPage from './pages/SearchPage'; 
import LogIn from './pages/LogIn';
import SignIn from './pages/SignIn';
import ChapterPage from './pages/chapterpage';
import NovelsList from './pages/novellist';
import NotFoundPage from './pages/notfoundpage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/novels/:id" element={<NovelsPage />} />
        <Route path="/novels/:novelId/:chapterId" element={<ChapterPage />} />
        <Route path="/updated-novels" element={<UpdatedNovelsPage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/login" element={<LogIn />} />
        <Route path="/signin" element={<SignIn />} />
        <Route path="/novels/popular" element={<NovelsList />} />
        <Route path="/novels/latest" element={<NovelsList />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
}

export default App;

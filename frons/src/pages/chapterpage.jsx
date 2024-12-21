import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import AppNavbar from '../components/navbar';
import './chapterpage.css';

const ChapterPage = () => {
  const { novelId, chapterId } = useParams();
  const navigate = useNavigate();
  const [chapterData, setChapterData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchChapter = async () => {
      try {
        const response = await fetch(`http://localhost:5000/novel/${novelId}/${chapterId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch chapter data');
        }
        const data = await response.json();
        setChapterData(data[0]);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchChapter();
  }, [novelId, chapterId]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!chapterData) {
    return <div>No chapter data available</div>;
  }
  
  const {
    chapter_title,      
    content,           
    date_edited,      
    id,                
    next_chapter_id,   
    novel_id,          
    previous_chapter_id 
    } = chapterData;

  const handleNavigation = (nextChapterId) => {
    if (nextChapterId !== null && nextChapterId !== undefined) {
      navigate(`/novels/${novelId}/${nextChapterId}`);
    }
  };

  return (
    <>
      <AppNavbar />
      <div className="chapter-page-container">
        {/* Navigation (Top) */}
        <div className="navigation-buttons">
          {previous_chapter_id !== null && previous_chapter_id !== undefined && (
            <button onClick={() => handleNavigation(previous_chapter_id)}>Previous</button>
          )}
          <button onClick={() => navigate(`/novels/${novelId}`)}>Index</button>
          {next_chapter_id !== null && next_chapter_id !== undefined && (
            <button onClick={() => handleNavigation(next_chapter_id)}>Next</button>
          )}
        </div>

        {/* Chapter Content */}
        <div className="chapter-content" style={{ margin: '20px 0' }}>
          <h2>{chapter_title}</h2>
          <p>{content}</p>
        </div>

        {/* Navigation (Bottom) */}
        <div className="navigation-buttons">
          {previous_chapter_id !== null && previous_chapter_id !== undefined && (
            <button onClick={() => handleNavigation(previous_chapter_id)}>Previous</button>
          )}
          <button onClick={() => navigate(`/novels/${novelId}`)}>Index</button>
          {next_chapter_id !== null && next_chapter_id !== undefined && (
            <button onClick={() => handleNavigation(next_chapter_id)}>Next</button>
          )}
        </div>
      </div>
    </>
  );
};

export default ChapterPage;
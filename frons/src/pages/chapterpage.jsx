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
        console.log("Fetched Chapter Data:", data);
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
    chapter_title,      // "Chapter 3"
    content,           // "This is the content of Chapter 3 for Novel 1."
    date_edited,       // "2024-12-19T22:38:42.798502"
    id,                // 3
    next_chapter_id,   // 4
    novel_id,          // 1
    previous_chapter_id // 2
    } = chapterData;
   console.log("Chapter Data:", chapterData);
   console.log("Chapter title:", chapter_title);
   console.log("Content:", content);
   console.log("Date edited:", date_edited);
   console.log("ID:", id);
   console.log("Next chapter ID:", next_chapter_id);
   console.log("Novel ID:", novel_id);
   console.log("Previous chapter ID:", previous_chapter_id);

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
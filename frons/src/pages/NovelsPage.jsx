import AppNavbar from "../components/navbar";
import './novelspage.css';
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

function NovelsPage() {
    const { id } = useParams();

    const [novel, setNovel] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const chaptersPerPage = 100;

    useEffect(() => {
        const fetchNovel = async () => {
            try {
                const response = await fetch(`http://localhost:5000/novel/${id}/all`);
                console.log(response);
                if (!response.ok) {
                    throw new Error('Failed to fetch novel');
                }
                const result = await response.json();
                setNovel(result);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        fetchNovel();
    }, [id]);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>Error: {error}</p>;
    }

    if (!novel) {
        return <p>No novel found.</p>;
    }

    // Pagination logic
    const indexOfLastChapter = currentPage * chaptersPerPage;
    const indexOfFirstChapter = indexOfLastChapter - chaptersPerPage;
    const currentChapters = novel.slice(indexOfFirstChapter, indexOfLastChapter);

    const paginate = (pageNumber) => setCurrentPage(pageNumber);

    const totalPages = Math.ceil(novel.length / chaptersPerPage);
    const pageNumbers = [];
    for (let i = 1; i <= totalPages; i++) {
        pageNumbers.push(i);
    }

    return (
        <>
            <AppNavbar />
            <div className="container">
                <div className="novel-details">
                    <div className="novel-image">
                        <img
                            src={novel[0].picture || "https://via.placeholder.com/200x300"}
                            alt={novel[0].name || "Novel Image"}
                        />
                    </div>
                    <div className="novel-info">
                        <h1 className="novel-title">{novel[0].name}</h1>
                        <p className="novel-description">{novel[0].description}</p>
                    </div>
                </div>

                <div className="chapter-list">
                    <h2>Chapters</h2>
                    <ul>
                        {currentChapters.map((novel, index) => (
                            <li key={novel.chapter_id || index}>
                                <a href={`/novels/${novel.novel_id}/${novel.chapter_id}`}>
                                    {novel.chapter_title}
                                </a>
                            </li>
                        ))}

                    </ul>

                    <div className="pagination">
                        {pageNumbers.map((number) => (
                            <a
                                key={number}
                                href="#!"
                                onClick={() => paginate(number)}
                                className={`page-number ${currentPage === number ? 'active' : ''}`}
                            >
                                {number}
                            </a>
                        ))}
                    </div>
                </div>
            </div>
        </>
    );
}

export default NovelsPage;

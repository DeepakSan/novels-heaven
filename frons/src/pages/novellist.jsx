import React, { useState, useEffect } from 'react';
import CardComponent from '../components/cardcomponent';
import AppNavbar from '../components/navbar';
import './novellist.css';

function NovelsList({ searchResults }) {
    const [novels, setNovels] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const novelsPerPage = 20;

    useEffect(() => {
        if (!searchResults || searchResults.length === 0) {
            fetchNovels(currentPage); // Fetch regular novels if no search results
        }
    }, [currentPage, searchResults]);

    const fetchNovels = async (page) => {
        try {
            const response = await fetch(`http://localhost:5000/novel/paginated?page=${page}&limit=${novelsPerPage}`);
            if (!response.ok) {
                throw new Error('Failed to fetch novels');
            }
            const data = await response.json();
            setNovels(data);
            setTotalPages(Math.ceil(data.length / novelsPerPage)); // Calculate total pages
        } catch (err) {
            console.error(err.message);
        }
    };

    // Ensure that searchResults is an array and use it if available, otherwise fallback to regular novels
    const novelsToDisplay = Array.isArray(searchResults) && searchResults.length > 0 ? searchResults : novels;

    return (
        <div>
            {!searchResults ? (
                <AppNavbar></AppNavbar>
            ) : (
                <p></p>
            )}
            <div className="container">
                <h1 className="section-title">Novels</h1>
                <div className="card-grid">
                    {novelsToDisplay.length > 0 ? (
                        novelsToDisplay.map((novel) => (
                            <CardComponent
                                key={novel.id}
                                image={novel.picture ? `data:image/jpeg;base64,${novel.picture}` : "https://picsum.photos/200/300"}
                                link={`/novels/${novel.id}`}
                                title={novel.name}
                            />
                        ))
                    ) : (
                        <p>No novels found</p> // Display message if no novels are available
                    )}
                </div>
                <div className="pagination-container">
                    <button
                        className="pagination-btn"
                        onClick={() => setCurrentPage(currentPage - 1)}
                        disabled={currentPage === 1}
                    >
                        Previous
                    </button>
                    <span className="page-info">Page {currentPage} of {totalPages}</span>
                    <button
                        className="pagination-btn"
                        onClick={() => setCurrentPage(currentPage + 1)}
                        disabled={currentPage === totalPages}
                    >
                        Next
                    </button>
                </div>
            </div>
        </div>
    );
}

export default NovelsList;

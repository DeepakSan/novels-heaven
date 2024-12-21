import './updatednovel.css';
import React, { useState, useEffect } from "react";

function UpdatedNovels() {
    const [novels, setNovels] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchUpdatedNovels = async () => {
            try {
                const response = await fetch('http://localhost:5000/novel/last');
                if (!response.ok) {
                    throw new Error('Failed to fetch novels');
                }
                const result = await response.json();
                setNovels(result);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchUpdatedNovels();
    }, []);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>Error: {error}</p>;
    }

    return (
        <div>
            <div className="container">
                <h2 className="section-title">New Updates</h2>
                <div className="updates-table">
                    <table>
                        <thead>
                            <tr>
                                <th>Novel</th>
                                <th>Chapter Number</th>
                                <th>Time Ago</th>
                            </tr>
                        </thead>
                        <tbody>
                            {novels.map((update, index) => (
                                <tr key={index}>
                                    <td>
                                        <a href={`/novels/${update.novel_id}`}>{update.name}</a>
                                    </td>
                                    <td>
                                        <a href={`/novels/${update.novel_id}/${update.chapter_id}`}>{update.chapter_title}</a>
                                    </td>
                                    <td>{update.date_edited}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

export default UpdatedNovels;

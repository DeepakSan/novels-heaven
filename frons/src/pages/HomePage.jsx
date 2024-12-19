import React from "react";
import AppNavbar from "../components/navbar";
import CardComponent from "../components/cardcomponent";
import "./homepage.css"; // Import the external CSS file
import UpdatedNovels from "../components/updatednovel";
import { useState, useEffect } from "react";

function HomePage() {
    const [novels, setNovels] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [novelsbydate, setNovelsByDate] = useState([]);
    const [loadingbydate, setLoadingByDate] = useState(true);
    const [errorbydate, setErrorByDate] = useState(null);
  
    useEffect(() => {
      const fetchNovels = async () => {
        try {
          const response = await fetch('http://localhost:5000/novel');
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
  
      fetchNovels();

      const fetchNovelsByDate = async () => {
        try {
          const responsebymod = await fetch('http://localhost:5000/novel/mod');
          if (!responsebymod.ok) {
            throw new Error('Failed to fetch novels');
          }
          const resultbydate = await responsebymod.json();
          setNovelsByDate(resultbydate);
        } catch (err) {
          setErrorByDate(err.message);
        } finally {
          setLoadingByDate(false);
        }
      };
  
      fetchNovelsByDate();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }
    
    if (error) {
        return <div>Error: {error}</div>;
    }
    if (loadingbydate) {
      return <div>Loading...</div>;
    }
  
    if (errorbydate) {
      return <div>Error: {error}</div>;
    }

    return (
        <div>
            <AppNavbar />
            <h1 className="home-title">Home Page</h1>
            <div className="container">
                <h2 className="section-title">Popular Novels</h2>
                <div className="card-grid">
                    {novels.map(novel => (
                        <CardComponent
                            key={novel.id}
                            image={novel.picture ? `data:image/jpeg;base64,${novel.picture}` : "https://picsum.photos/200/300"}
                            link={`/novels/${novel.id}`}
                            title={novel.name}
                        />
                    ))}
                </div>
            </div>
            <div className="container">
                <h2 className="section-title">Latest Novels</h2>
                <div className="card-grid">
                    {novelsbydate.map(novel => (
                        <CardComponent
                            key={novel.id}
                            image={novel.picture ? `data:image/jpeg;base64,${novel.picture}` : "https://picsum.photos/200/300"}
                            link={`/novels/${novel.id}`}
                            title={novel.name}
                        />
                    ))}
                </div>
            </div>
            <UpdatedNovels />
        </div>
    );
}

export default HomePage;

import { useEffect, useState } from "react";
import AppNavbar from "../components/navbar";
import UpdatedNovels from "../components/updatednovel";


function UpdatedNovelsPage() {
    const [novels, setNovels] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchupdatednovels = async () => {
            try {
                const response = await fetch('http://localhost:5000/novel');
                console.log(response);
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
        }
        fetchupdatednovels();
    }, []);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>Error: {error}</p>;       
    }


    return (
        <div>
            <AppNavbar />
            <UpdatedNovels lastUpdatedNovels={novels} />
        </div>
    );  
}   

export default UpdatedNovelsPage
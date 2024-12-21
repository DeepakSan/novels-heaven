import AppNavbar from "../components/navbar";
import './searchpage.css'
import { useState } from "react";
import NovelsList from './novellist'; // Import the NovelsList component

function SearchPage() {
    const [searchTerm, setSearchTerm] = useState("");
    const [searchResults, setSearchResults] = useState([]); // State to hold the search results
    const [loading, setLoading] = useState(false); // State for loading status

    const handleSearch = (e) => {
        e.preventDefault(); // Prevent default form behavior
        console.log("Searching for:", searchTerm);

        setLoading(true); // Set loading to true while the data is being fetched

        // Fetch search results
        fetch(`http://localhost:5000/search?query=${encodeURIComponent(searchTerm)}`)
            .then((response) => response.json())
            .then((data) => {
                setSearchResults(data); // Set the search results to the state
                setLoading(false); // Set loading to false when data is fetched
            })
            .catch((error) => {
                console.error("Error:", error);
                setLoading(false); // Set loading to false if there's an error
            });
    };

    return (
        <>
            <AppNavbar />
            <form className="search-form" onSubmit={handleSearch}>
                <input
                    type="text"
                    placeholder="Search for a novel..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
                <button type="submit">Search</button>
            </form>

            {loading ? (
                <p>Loading...</p> 
            ) : (
                <NovelsList searchResults={searchResults} />
            )}
        </>
    );
}

export default SearchPage;

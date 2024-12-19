import AppNavbar from "../components/navbar";
import './searchpage.css'
import { useState } from "react";

function SearchPage() {
    const [searchTerm, setSearchTerm] = useState("");

    const handleSearch = (e) => {
        e.preventDefault(); // Prevent default form behavior
        console.log("Searching for:", searchTerm);

        fetch(`/api/search?query=${encodeURIComponent(searchTerm)}`)
            .then((response) => response.json())
            .then((data) => {
                console.log("Search results:", data);
            })
            .catch((error) => {
                console.error("Error:", error);
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
        </>
    );
}

export default SearchPage
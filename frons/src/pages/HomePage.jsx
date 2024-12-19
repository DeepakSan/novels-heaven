import React from "react";
import AppNavbar from "../components/navbar";
import CardComponent from "../components/cardcomponent";
import "./homepage.css"; // Import the external CSS file
import UpdatedNovels from "../components/updatednovel";

function HomePage() {
    return (
        <div>
            <AppNavbar />
            <h1 className="home-title">Home Page</h1>
            <div className="container">
                <h2 className="section-title">Popular Novels</h2>
                <div className="card-grid">
                    <CardComponent image="https://picsum.photos/200/300" link="/novels/1" title="The Complete Sherlock Holmes" />
                    <CardComponent image="https://picsum.photos/200/300" link="/novels/2" title="Pride and Prejudice" />
                    <CardComponent image="https://picsum.photos/200/300" link="/novels/3" title="Moby Dick" />
                    <CardComponent image="https://picsum.photos/200/300" link="/novels/4" title="1984" />
                    <CardComponent image="https://picsum.photos/200/300" link="/novels/5" title="To Kill a Mockingbird" />
                    <CardComponent image="https://picsum.photos/200/300" link="/novels/6" title="The Great Gatsby" />
                    <CardComponent image="https://picsum.photos/200/300" link="/novels/7" title="War and Peace" />
                    <CardComponent image="https://picsum.photos/200/300" link="/novels/8" title="The Catcher in the Rye" />
                </div>
            </div>
            <div className="container">
                <h2 className="section-title">Latest Novels</h2>
                <div className="card-grid">
                    <CardComponent image="https://picsum.photos/200/300" link="/novels/1" title="The Complete Sherlock Holmes" />
                    <CardComponent image="https://picsum.photos/200/300" link="/novels/2" title="Pride and Prejudice" />
                    <CardComponent image="https://picsum.photos/200/300" link="/novels/3" title="Moby Dick" />
                    <CardComponent image="https://picsum.photos/200/300" link="/novels/4" title="1984" />
                    <CardComponent image="https://picsum.photos/200/300" link="/novels/5" title="To Kill a Mockingbird" />
                    <CardComponent image="https://picsum.photos/200/300" link="/novels/6" title="The Great Gatsby" />
                    <CardComponent image="https://picsum.photos/200/300" link="/novels/7" title="War and Peace" />
                    <CardComponent image="https://picsum.photos/200/300" link="/novels/8" title="The Catcher in the Rye" />
                </div>
            </div>
            <UpdatedNovels />
        </div>
    );
}

export default HomePage;

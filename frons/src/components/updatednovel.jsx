import './updatednovel.css'

function  UpdatedNovels() { 
    const newUpdates = [
        { novel: "The Complete Sherlock Holmes", chapter: "Chapter 5", timeAgo: "2 hours ago", link: "/novels/1/chapter/5" },
        { novel: "Pride and Prejudice", chapter: "Chapter 10", timeAgo: "5 hours ago", link: "/novels/2/chapter/10" },
        { novel: "Moby Dick", chapter: "Chapter 3", timeAgo: "1 day ago", link: "/novels/3/chapter/3" },
        { novel: "1984", chapter: "Chapter 7", timeAgo: "2 days ago", link: "/novels/4/chapter/7" },
        { novel: "To Kill a Mockingbird", chapter: "Chapter 4", timeAgo: "3 days ago", link: "/novels/5/chapter/4" },
        { novel: "The Great Gatsby", chapter: "Chapter 2", timeAgo: "4 days ago", link: "/novels/6/chapter/2" },
        { novel: "War and Peace", chapter: "Chapter 12", timeAgo: "5 days ago", link: "/novels/7/chapter/12" },
        { novel: "The Catcher in the Rye", chapter: "Chapter 6", timeAgo: "1 week ago", link: "/novels/8/chapter/6" },
        { novel: "Brave New World", chapter: "Chapter 9", timeAgo: "1 week ago", link: "/novels/9/chapter/9" },
        { novel: "Crime and Punishment", chapter: "Chapter 8", timeAgo: "2 weeks ago", link: "/novels/10/chapter/8" },
    ];

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
                            {newUpdates.map((update, index) => (
                                <tr key={index}>
                                    <td>
                                        <a href={update.link}>{update.novel}</a>
                                    </td>
                                    <td>
                                        <a href={update.link}>{update.chapter}</a>
                                    </td>
                                    <td>{update.timeAgo}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

export default UpdatedNovels
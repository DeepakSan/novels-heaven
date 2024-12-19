import './updatednovel.css'

function  UpdatedNovels({ lastUpdatedNovels }) { 

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
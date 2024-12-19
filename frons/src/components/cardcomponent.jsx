

function CardComponent(props) {
    return (
        <div className="card">
            <img src={props.image} className="card-img-top" alt="..." />
            <div className="card-body">
                <a href={props.link} className="btn btn-primary"><h5 className="card-title">{props.title}</h5></a>
            </div>
        </div>
    );
}

export default CardComponent
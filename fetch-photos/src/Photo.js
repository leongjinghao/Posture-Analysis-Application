import React from 'react';

const Photo = (props) => {
    return (
        <section>
            <img src={props.url} alt="doggo photo" />
        </section>
    )
}

export default Photo
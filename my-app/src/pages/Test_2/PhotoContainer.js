import React, { Component } from "react";
import './PhotoContainer.css';

const PhotoContainer = props => {
    const displayPhotos = () => {
        return props.videos.map(video => {
            return <div className='video-container'>
                <video className='AI_Videos' preload='metadata' controls>
                    <source src={video} type='video/mp4' />
                </video>
            </div>
        });
    };

    return (<div>{displayPhotos()}</div>)
}



export default PhotoContainer
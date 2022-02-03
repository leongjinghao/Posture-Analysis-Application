import React from 'react';
import './Modal.css';

function Modal({ url, closeModal }) {
    return (
        <div className='modal-background'>
            <div className='modal-content'>
                <button id='close' onClick={() => closeModal(false)}> X </button>
                <div className='modal-header'></div>
                <h1>{url}</h1>
                <div className='modal-body'>
                    <video className='posture-video' preload='metadata' controls><source src={url} type='video/mp4' /></video>
                </div>
                <div className='modal-footer'>
                    <button id='export-button'>Export</button>
                    <button id='delete-button'>Delete</button>
                </div>
            </div>
        </div>
    )
}

export default Modal
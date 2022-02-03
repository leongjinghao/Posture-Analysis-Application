import './modal.css';

const Modal = props => {
    return (
        <div className='modal'>
            <div className='modal-content'>
                <div className='modal-header'>
                    <h4 className='modal-title'>Modal title</h4>
                </div>
                <div className='modal-body'>
                    <video title="Title" className='AI_Videos' preload='metadata' controls>
                        {/* Temporary */} 
                        <source src="video_sample/video.mp4" type='video/mp4' />
                    </video>
                </div>
                <div className='modal-footer'>
                    <button className='button'>Close</button>
                </div>
            </div>
        </div>
    )
}

export default Modal
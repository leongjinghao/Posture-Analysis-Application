import React, { useState } from "react";
import Modal from './Modal';
import './VideoContainer.css';

const videolist = ['video_sample/boxing.mp4', 'video_sample/boxing2.mp4', 'video_sample/cycling.mp4',
    'video_sample/dancing.mp4', 'video_sample/dancing2.mp4',
    'video_sample/dancing3.mp4', 'video_sample/exercise.mp4',
    'video_sample/exercise2.mp4', 'video_sample/running.mp4',
    'video_sample/video.mp4']

// const VideoContainer = props => {
//     constructor() {
//         super();
//         this.state = {
//             videos: [],
//         }
//     };

//     showModal = () => {
//         this.setState({
//             displayModal: true,
//         });
//     };

//     closeModal = () => {
//         this.setState({ displayModal: false });
//     };

//     const displayVideos = () => {
//         return videolist.map(video => {// props.videos.map(video => {
//             return <div className='video-container'>
//                 <video className='video-size' preload='metadata' onClick={() => this.videoState.setState({ displayModal: true })}>
//                     <source src={video} type='video/mp4' />
//                 </video>
//                 {this.videoState.displayModal && <Modal url='video_sample/boxing.mp4' closeModal={this.closeModal} />}
//                 {/* {this.state.displayModal && <Modal url='video_sample/boxing.mp4' closeModal={this.closeModal} />} */}
//             </div>
//         });
//     };

//     return (<div>{displayVideos()}</div>)
// }


const Video = () => {
    const [displayModal, setDisplayModal] = useState(false)
    return <video className="video-size">
        <source src={video} type='video/mp4' />
    </video>
}

function VideoContainer(props) {

    const [displayModal, setDisplayModal] = useState(false)

    const displayVideos = () => {
        // const [displayModal, setDisplayModal] = useState(false)
        return videolist.map(video => {// props.videos.map(video => {
            // console.log(setDisplayModal)
            return <div className='video-container'>
                <video className='video-size' preload='metadata' onClick={() => setDisplayModal(true)}>
                    <source src={video} type='video/mp4' />
                </video>
                {displayModal && <Modal url={video} closeModal={setDisplayModal} />}
            </div>
        });
    };

    return (<div>{displayVideos()}</div>)
}

export default VideoContainer
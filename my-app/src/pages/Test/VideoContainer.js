import React, { Component } from "react";
import { Modal, Button } from 'antd';
import VideoModal from './VideoModal';
import './VideoContainer.css';

const videolist = ['video_sample/boxing',
    'video_sample/boxing2', 'video_sample/cycling',
    'video_sample/dancing', 'video_sample/dancing2',
    'video_sample/dancing3', 'video_sample/exercise',
    'video_sample/exercise2', 'video_sample/running',
    'video_sample/video']

class VideoContainer extends React.Component {
    state = {
        loading: false,
        visible: false,
    };

    showModal = () => {
        this.setState({
            visible: true,
        });
    };

    handleOk = () => {
        this.setState({ loading: true });
        setTimeout(() => {
            this.setState({ loading: false, visible: false });
        }, 3000);
    };

    handleCancel = () => {
        this.setState({ visible: false });
    };

    render() {
        const { visible, loading } = this.state;
        return videolist.map(video => {// props.videos.map(video => {
            return (<div className='video-container'>
                <video className='video-size' preload='metadata' onClick={this.showModal} >
                    <source src={video + '.mp4'} type='video/mp4' />
                </video>
                <VideoModal url={video} visible={visible} loading={loading} handleOk={this.handleOk} handleCancel={this.handleCancel} />
                <p className="video-text" >{video}<br />31/1/2022</p>
            </div>
            );
        });
    }
}

export default VideoContainer
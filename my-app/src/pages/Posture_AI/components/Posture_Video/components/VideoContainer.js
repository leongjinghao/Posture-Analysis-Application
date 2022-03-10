import React, { Component } from "react";
import './styles.css';
import VideoModal from './VideoModal';
import { Row, Col } from "antd";

const baseURL = 'https://localhost:5001/PostureVideoPath';

class VideoContainer extends React.Component {

    state = {
        loading: false,
        visible: false,
        videoUrl: '',
        vidTitle: '',
        videos: [],
    };

    componentDidMount() {
        fetch(baseURL)
            .then(response => {
                if (!response.ok) {
                    throw Error("Error fetching the posture videos")
                }
                return response.json()
                    .then(allData => {
                        this.setState({ videos: allData });
                    })
                    .catch(err => {
                        throw Error(err.message);
                    });
            });
    }

    showModal = (url, title) => {
        return () => {
            this.setState({
                visible: true,
                videoUrl: url,
                vidTitle: title
            })
        }
    }

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
        const { visible, loading, videos } = this.state;
        const displayVideos = () => {
            return videos.map(video => (
                <Col xs={12} xl={6} >
                    <div className="video-container">
                        <video className='video-size'
                            preload='metadata'
                            onClick={this.showModal(video.postureVideoPath, video.postureVideoPath)} >
                            <source src={video.postureVideoPath} type='video/mp4' />
                        </video>
                        <p className="video-text">{video.postureVideoPath.replace('posture_video_recording/', '')}
                        </p>
                    </div>
                </Col>
            )
            )
        }

        return (
            <Row>
                {displayVideos()}
                <VideoModal title={this.state.vidTitle}
                    url={this.state.videoUrl}
                    visible={visible}
                    loading={loading}
                    handleOk={this.handleOk}
                    handleCancel={this.handleCancel} />
            </Row>
        )
    }
}

export default VideoContainer;
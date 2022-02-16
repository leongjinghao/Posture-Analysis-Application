import React, { Component } from "react";
import VideoModal from './videoModal';
import { Row, Col } from "antd";

const videolist = ['video_sample/boxing',
    'video_sample/boxing2', 'video_sample/cycling',
    'video_sample/dancing', 'video_sample/dancing2',
    'video_sample/dancing3', 'video_sample/exercise',
    'video_sample/exercise2', 'video_sample/running',
    'video_sample/video']

class Video extends React.Component {

    state = {
        loading: false,
        visible: false,
        videoUrl: '',
        videoName: '',
        videos: [],
    };

    componentDidMount() {
        fetch("https://localhost:5001/VideoPath")
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

    showModal = (url, id) => {
        return () => {
            this.setState({
                visible: true,
                videoUrl: url,
                videoId: id
            })
        }
    }

    displayRightModal(url) {
        this.setState({ videolink: url });
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
        // if (!DataIsLoaded) return <div><h1>Loading ...</h1></div>;
        const displayVideos = () => {
            return videos.map(video => (
                <Col xs={12} xl={6} >
                    <div className="video-container">
                        <video className='video-size' preload='metadata' onClick={this.showModal(video.videoPath, video.id)} >
                            <source src={video.videoPath} type='video/mp4' />
                        </video>
                        <p className="video-text">{video.videoPath.replace('posture_video_recording/', '')}<br />31/1/2022</p>
                    </div>
                </Col>
            )
            )
        }

        return (
            <Row>
                {displayVideos()}
                <VideoModal id={this.state.videoId} url={this.state.videoUrl} visible={visible} loading={loading} handleOk={this.handleOk} handleCancel={this.handleCancel} />
            </Row>
        )
    }
}

export default Video
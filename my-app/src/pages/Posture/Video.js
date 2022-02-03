import React, { Component } from "react";
import VideoModal from './VideoModal';
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
        videolink: '',
    };

    showModal = (url) => {
        return () => {
            this.setState({
                visible: true,
                videolink: url,
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
        const { visible, loading } = this.state;
        const displayVideos = () => {
            return videolist.map(video => {
                return (<>
                    <Col xs={12} xl={6} >
                        <div className="video-container">
                            <video className='video-size' preload='metadata' onClick={this.showModal(video)} >
                                <source src={video + '.mp4'} type='video/mp4' />
                            </video>
                            <p className="video-text">{video}<br />31/1/2022</p>
                        </div>
                    </Col>
                </>)
            })
        }

        return (
            <Row>
                {displayVideos()}
                <VideoModal url={this.state.videolink} visible={visible} loading={loading} handleOk={this.handleOk} handleCancel={this.handleCancel} />
            </Row>
        )
    }
}

export default Video
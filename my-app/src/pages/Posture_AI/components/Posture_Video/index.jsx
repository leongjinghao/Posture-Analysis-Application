import React, { Component } from 'react';
import { Typography } from 'antd';
import VideoContainer from './components/VideoContainer';

const { Title } = Typography;

class PostureVideo extends Component {
    constructor() {
        super();
        this.state = {
            videos: []
        };
    }

    render() {
        return (
            <div className="logo" id="logos">
                <Title style={{ marginLeft: '2vw', marginTop: '1vh', fontFamily: 'Merriweather' }}>
                    <u id="page_title">List of Videos</u>
                </Title>
                <VideoContainer />
            </div>
        )
    }
}

export default PostureVideo;
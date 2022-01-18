import React, { Component } from 'react';
import ProCard from '@ant-design/pro-card';
import './videoStyle.css'

const videolink = 'http://localhost:8000/video_sample/boxing.mp4'

const Video = (props) => {
  return (
      <video className='AI_Videos'preload='metadata' controls>
        <source src={videolink} type='video/mp4' />
      </video>
  )
}

const VideoContainer = props => {
  const displayVideos = () => {
    return props.videos.map(video => {
      return <Video url={video.url} />;
    });
  };
  return (<><section>{displayVideos()}</section></>)
}

class PostureApp extends Component {
  constructor() {
    super();
    this.state = {
      videos: []
    };
  }
  componentDidMount() {
    fetch("https://api.thedogapi.com/v1/images/search?limit=12")
      .then(response => {
        if (!response.ok) {
          throw Error("Error fetching the posture videos");
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
  render() {
    return (
      <>
        <ProCard style={{ marginTop: 8 }} gutter={[16, 16]} wrap title="List of Videos" >
          <VideoContainer videos={this.state.videos} />
        </ProCard >
      </>
    )
  }
}

export default PostureApp
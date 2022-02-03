import React, { Component } from 'react';
import ProCard from '@ant-design/pro-card';
import './videoStyle.css';
import Modal from './Modal';

//const videolink = 'http://localhost:8000/video_sample/boxing.mp4'
const videolist = ['video_sample/boxing.mp4',
  'video_sample/boxing2.mp4', 'video_sample/cycling.mp4',
  'video_sample/dancing.mp4', 'video_sample/dancing2.mp4',
  'video_sample/dancing3.mp4', 'video_sample/exercise.mp4',
  'video_sample/exercise2.mp4', 'video_sample/running.mp4',
  'video_sample/video.mp4']
// const Video = (props) => {
//   return (
//     <div className='Video_Container' style={{display: isContainerVisible}}>
//       <video className='AI_Videos' preload='metadata' controls>
//         <source src={videolink} type='video/mp4' />
//       </video>
//     </div>
//   )
// }

function openModal() {
  return <div>Modal</div>
}

const VideoContainer = props => {
  const displayVideos = () => {
    return videolist.map(video => {//props.videos.map(video => {
      return <div className='Video_Container'>
        <video className='AI_Videos' preload='metadata' onClick={openModal}>
          <source src={video} type='video/mp4' />
        </video>
        <p>Video #{video}</p>
      </div>;
    });
  };
  return (<><div>{displayVideos()}</div></>)
}

class PostureApp extends Component {
  constructor() {
    super();
    this.state = {
      videos: [],
      showModal: false
    };
  }
  componentDidMount() {
    fetch("https://api.thedogapi.com/v1/images/search?limit=1")
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
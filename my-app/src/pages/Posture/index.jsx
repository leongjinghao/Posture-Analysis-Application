import React, { Component } from 'react';
import ProCard from '@ant-design/pro-card';

const Video = (props) => {
  return (
    <section>
      <video width="auto" height='326.4' controls>
        <source src={props.url} type='video/mp4' />
      </video>
    </section>
  )
}

const VideoContainer = props => {
  const displayVideos = () => {
    return props.videos.map(video => {
      return <Video url={video.url} />;
    });
  };
  return (
    <><section>{displayVideos()}</section></>
  )
}

class PostureApp extends Component {
  constructor() {
    super();
    this.state = {
      videos: []
    };
  }
  componentDidMount() {
    fetch("https://api.thedogapi.com/v1/images/search?limit=4")
      .then(response => {
        if (!response.ok) {
          throw Error("Error fetching the cute doggies");
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
      <section className='List of Videos'>
        <p>List of Videos</p>
        <div className='Video_Container'>
      <VideoContainer videos={this.state.videos} />
    </div>
      </section>
    )
  }
}

export default PostureApp
    // <>
    //   <ProCard style={{ marginTop: 8 }} gutter={[16, 16]} wrap title="List of Videos" >
    //     <video width="auto" height='326.4' controls>
    //       <source src='/video_sample/boxing.mp4' type='video/mp4'/>
    //     </video>
    //     <video width="auto" height="326.4" controls>
    //       <source src='/video_sample/boxing2.mp4' type='video/mp4'/>
    //     </video>
    //   </ProCard>
    // </>
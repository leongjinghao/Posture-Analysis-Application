import React, { Component } from "react";
import ProCard from "@ant-design/pro-card";
import './index.css';
import VideoContainer from "./VideoContainer";

// const PhotoContainer = props => {
//     const displayPhotos = () => {
//         return props.videos.map(video => {
//             return <div className='Video_Container'>
//                 {/* <video className='AI_Videos' preload='metadata' onClick={openModal}>
//                         <source src={video} type='video/mp4' />
//                     </video> */}
//                 <section>
//                     <img src={video.url} alt="doggo photo"></img>
//                 </section>
//             </div>
//         });
//     };

//     return (<div>{displayPhotos()}</div>)
// }

class App extends Component {
    constructor() {
        super();
        this.state = {
            videos: [],
        }
    }

    componentDidMount() {
        fetch("https://api.thedogapi.com/v1/images/search?limit=2")
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
            <ProCard tabs={{ type: 'card' }}>
                <ProCard.TabPane key=" tab1" tab="List of Videos">
                    <VideoContainer videos={this.state.videos} />
                    {/* <button className="openModalBtn" onClick={() => this.showModal(true)}>Open</button>
                    {this.state.displayModal && <Modal url='video_sample/boxing.mp4' closeModal={this.closeModal} />} */}
                </ProCard.TabPane>
                <ProCard.TabPane key=" tab2" tab="Live Feed">
                    Content 2
                </ProCard.TabPane>
            </ProCard>
        )
    }
}

export default App
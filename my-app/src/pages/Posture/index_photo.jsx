import React, { Component } from 'react';

const Photo = (props) => {
  return (
    <section><img src={props.url} alt="doggo photo" /></section>
  )
}

const PhotoContainer = props => {
  const displayPhotos = () => {
    return props.photos.map(photo => {
      return <Photo url={photo.url} />;
    });
  };
  return (
    <><section>{displayPhotos()}</section></>
  )
}

const Greet = (props) => {
  console.log(props)
  return <h1>Hello {props.name}</h1>
}

class PostureApp extends Component {
  constructor() {
    super();
    this.state = {
      photos: []
    };
  }
  componentDidMount() {
    fetch("https://api.thedogapi.com/v1/images/search?limit=10")
      .then(response => {
        if (!response.ok) {
          throw Error("Error fetching the cute doggies");
        }
        return response.json()
          .then(allData => {
            this.setState({ photos: allData });
          })
          .catch(err => {
            throw Error(err.message);
          });
      });
  }
  render() {
    return (
      <section className='app'>
        <p>List of videos</p>
        <div>
          <PhotoContainer photos={this.state.photos} />
        </div>
      </section>
    )
  }
}

export default PostureApp;

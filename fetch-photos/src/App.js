//import logo from './logo.svg';
import React, { Component } from "react";
import './App.css';
import PhotoContainer from "./PhotoContainer";

class App extends Component {
  constructor() {
    super();
    this.state = {
      photos: []
    };
  }

  componentDidMount() {
    fetch('https://api.thedogapi.com/v1/images/search?limit=10')
      .then(response => {
        if (!response.ok) {
          throw Error("Error fetching the cute doggie");
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
      <section className="app">
        <p>Here are some doggos</p>
        <PhotoContainer photos={this.state.photos} />
      </section>
    );
  }
}

export default App;

import React, { Component } from "react";
import ProCard from "@ant-design/pro-card";
import Video from './Video';

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
                    <Video videos={this.state.videos} />
                </ProCard.TabPane>
                <ProCard.TabPane key=" tab2" tab="Live Feed">
                </ProCard.TabPane>
            </ProCard>
        )
    }
}

export default App
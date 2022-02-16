import React, { Component, useState } from "react";
import ProCard from "@ant-design/pro-card";
import Video from './video';

class App extends Component {
    constructor() {
        super();
    }

    render() {
        return (
            <ProCard tabs={{ type: 'card' }}>
                <ProCard.TabPane key=" tab1" tab="Live Feed">
                    <div>
                        <img src="http://localhost:5003/video" width="50%" />
                    </div>
                    <div>
                        <img src="http://localhost:5003/video" width="50%" />
                    </div>
                    <div>
                        <img src="http://localhost:5003/video" width="50%" />
                    </div>
                    <div>
                        <img src="http://localhost:5003/video" width="50%" />
                    </div>
                </ProCard.TabPane>
                <ProCard.TabPane key=" tab2" tab="List of Videos">
                    <Video />
                </ProCard.TabPane>
            </ProCard>
        )
    }

}

export default App
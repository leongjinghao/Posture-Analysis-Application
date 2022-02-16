import React, { Component } from "react";
import ProCard from "@ant-design/pro-card";
import Video from './Video';

class App extends Component {
    constructor() {
        super();
    }

    render() {
        return (
            <ProCard tabs={{ type: 'card' }}>
                <ProCard.TabPane key=" tab1" tab="List of Videos">
                    {/* <Video /> */}
                </ProCard.TabPane>
                <ProCard.TabPane key=" tab2" tab="Live Feed">
                </ProCard.TabPane>
            </ProCard>
        )
    }

}

export default App
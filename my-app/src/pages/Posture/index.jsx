import React, { Component, useState } from "react";
import ProCard from "@ant-design/pro-card";
import Video from './Video';
import menuClass from "./dropdown";
import { Dropdown, Button } from 'antd';
import { DownOutlined } from '@ant-design/icons';
import './index.css';

class App extends Component {
    constructor() {
        super();
    }

    render() {
        return (
            // Fix the logic
            <ProCard tabs={{ type: 'card' }}>
                <ProCard.TabPane key=" tab1" tab="Live Feed">
                    <div class='text-dropdown'>
                        <div class='text'>
                            <p class='Title'>Camera 1</p>
                        </div>
                        <div class='dropdown1'>
                            <Dropdown overlay={menuClass}>
                                <Button>
                                    All Cameras <DownOutlined />
                                </Button>
                            </Dropdown>
                        </div>
                    </div>
                    <div>
                        <img src="http://localhost:5002/video" width="50%" />
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
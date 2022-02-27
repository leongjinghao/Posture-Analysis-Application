import React, { Component, useState, props } from "react";
import ProCard from "@ant-design/pro-card";
import Video from './Video';
import menuClass from "./dropdown";
import { Dropdown, Button, Select } from 'antd';
import { DownOutlined } from '@ant-design/icons';
import './index.css';
import selectCamera from "./Select";

function handleChange(value) {
    console.log(`selected ${value}`);
}

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            showCamera2: false,
        }
    }
    handleOptionChange = (event) => {
        event.preventDefault();
        this.setState({
            showCamera2: true,
      }) 
      console.log('changed')
     }



    render() {
        return (
            <ProCard tabs={{ type: 'card' }}>
                <ProCard.TabPane key=" tab1" tab="Live Feed">
                {this.state.showCamera2 || 
                <div class="camera1">
                    <div class='text-dropdown'>
                        <div class='text'>
                            <p class='Title'>Camera 1</p>
                        </div>
                        <div class='dropdown1'>
                            <selectCamera />
                        </div>
                    </div>
                    <div>
                        <img src="http://localhost:5003/video" />
                    </div>
                </div>
                }
                {this.state.showCamera2 &&
                <div class="camera2">
                    <div class='text-dropdown'>
                        <div class='text'>
                            <p class='Title'>Camera 2</p>
                        </div>
                        <div class='dropdown1'>
                        <Dropdown overlay={menuClass}>
                                <Button>
                                    Camera 2 <DownOutlined />
                                </Button>
                        </Dropdown>
                        </div>
                    </div>
                    <div>
                        <img src="http://localhost:5003/video" />
                    </div>
                </div>
                }
                </ProCard.TabPane>
                <ProCard.TabPane key=" tab2" tab="List of Videos">
                    <Video />
                </ProCard.TabPane>
            </ProCard>
        )
    }

}

export default App
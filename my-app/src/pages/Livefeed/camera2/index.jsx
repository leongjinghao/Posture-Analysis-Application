import React, { Component, useState} from "react";
import ProCard from "@ant-design/pro-card";
import { Dropdown, Button } from 'antd';
import { DownOutlined } from '@ant-design/icons';
import './index.css';
import  WebcamClass  from "./webcam";
import  menuClass  from "./dropdown";


  class App extends Component{
    constructor() {
      super();
  }

    render() {
        return (
            <ProCard>
            <div class = 'text-dropdown'>
              <div class='text'>
                <p class='Title'>Camera 1</p>
              </div>
            <div class = 'dropdown1'>
                <Dropdown overlay={menuClass}>
                  <Button>
                      All Cameras <DownOutlined />
                  </Button>
              </Dropdown>
            </div>
            </div>
            <div class='webcam-container'>
                <WebcamClass />
            </div>
            </ProCard>
        )
    }
}

export default App
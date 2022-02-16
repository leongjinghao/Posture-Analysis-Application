import React, { Component, useState} from "react";
import ProCard from "@ant-design/pro-card";
import Webcam from "react-webcam";
import { Menu, Dropdown, Button, message, Space, Tooltip } from 'antd';
import { DownOutlined, UserOutlined } from '@ant-design/icons';
import { history, useModel } from 'umi';
import '../index.css'

export const WebcamComponent = () => <Webcam videoConstraints={videoConstraints} />;

const videoConstraints = {
    width: 600,
    height: 450,
    facingMode: "user"
};

function handleItem1Click(e) {
  history.push("/Livefeed")
}

function handleItem2Click(e) {
  history.push("/Livefeed/camera2")
}
  
  
  const menu = (
    <Menu>
      <Menu.Item key="1" onClick={handleItem1Click}>
        Camera 1
      </Menu.Item>
      <Menu.Item key="2" onClick={handleItem2Click}>
        Camera 2
      </Menu.Item>
    </Menu>
  );


class App extends Component{
    render() {
        return (
            <ProCard>
            <div class = 'text-dropdown'>
              <div class = 'text'>
                <p class='Title'>Camera 2</p>
              </div>
            <div class = 'dropdown1'>
                <Dropdown overlay={menu}>
                  <Button>
                      All Cameras <DownOutlined />
                  </Button>
              </Dropdown>
            </div>
            </div>
            <div class='webcam-container'>
                <WebcamComponent />
            </div>
            </ProCard>
        )
    }
}

export default App
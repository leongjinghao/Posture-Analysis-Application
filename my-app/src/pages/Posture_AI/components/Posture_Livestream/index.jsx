import React, { Component } from "react";
import "./styles.css";
import { Layout, Menu, Dropdown, Button } from 'antd';
import { DownOutlined } from '@ant-design/icons';
import { FirstCamera, SecondCamera } from './Cameras/Cameras';

class LiveStream extends Component {
    constructor() {
        super();
        this.state = {
            title: 'Location #01 (Camera 01)',
            selectedOption: '0'
        };
    }

    render() {
        const { Content } = Layout;

        const handleChange = ({ key }) => {
            this.setState({ title: key })
        }

        const menu = (
            <Menu onClick={handleChange}>
                <Menu.Item key='Location #01 (Camera 01)'>Location #01 (Camera 01)</Menu.Item>
                <Menu.Item key='Location #02 (Camera 02)'>Location #02 (Camera 02)</Menu.Item>
            </Menu>
        );
        return (
            <>
                <Content>
                    <div className="container">
                        <h1 id="livestream_title"> <u>{this.state.title}</u> </h1>
                        <Dropdown
                            overlay={menu}
                            trigger={['click']}>
                            <Button className="location-dropdown">
                                Location
                                <DownOutlined />
                            </Button>
                        </Dropdown>

                        <div className="camera-container">
                            {this.state.title === "Location #01 (Camera 01)" ? (
                                <FirstCamera />
                            ) : this.state.title === "Location #02 (Camera 02)" ? (
                                <SecondCamera />
                            ) : null}
                        </div>
                    </div>
                </Content>
            </>
        )
    }
}

export default LiveStream
import { Select } from 'antd';
import React, { Component, useState, props } from "react";

const { Option } = Select;

/**
 * Add new camera Url to this array
 */
const cameraUrl = { 'Camera 1': "http://localhost:5003/video", 'Camera 2': "add new link" }

class SelectCamera extends React.Component {
    formRef = React.createRef();
    /**
     * default url and camera
     */
    state = {
        url: 'http://localhost:5003/video',
        camera: 'Camera 1',
    };

    /**
     * Haven't really tested it out!
     */
    handleChange = value => {
        this.setState({
            camera: value,
            url: cameraUrl[value],
        })
    }

    render() {
        const { camera, url } = this.state;
        return (
            <>
                <div class='text-dropdown'>
                    <div class='text'>
                        <p class='Title'>{camera}</p>
                    </div>
                    <div class='dropdown1'>
                        <Select defaultValue="Camera 1" style={{ width: 120 }} onChange={this.handleChange}>
                            <Option value="Camera 1">Camera 1</Option>
                            <Option value="Camera 2">Camera 2</Option>
                            {/* Add <Option /> to add new camera */}
                        </Select>
                    </div>
                </div>
                <div>
                    <img src={url} />
                </div>
            </>
        )
    }
}

export default SelectCamera
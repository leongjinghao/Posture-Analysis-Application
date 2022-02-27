import { Select } from 'antd';
import React, { Component, useState, props } from "react";

const { Option } = Select;

/**
 * Add new camera link to this array. Haven't tested!
 */
const cameraLink = { "Camera 1": "http://localhost:5003/video", "Camera 2": "http://localhost:5003/video" }

// function handleChange(value) {
//     console.log(`selected ${value}`);
// }

class SelectCamera extends React.Component {
    /**
     * default url and camera
     */
    state = {
        url: 'http://localhost:5003/video',
        camera: 'All Cameras',
    };

    /**
     * Haven't really tested it out!
     */
    handleChange(value) {
        console.log(`selected ${value}`);
        this.state.camera = value;
        this.state.url = cameraLink['Camera 1'];
    }

    render() {
        const { url, camera } = this.state;
        return (
            <>
                <div class="camera1">
                    <div class='text-dropdown'>
                        <div class='text'>
                            <p class='Title'>{camera}</p>
                        </div>
                        <div class='dropdown1'>
                            <Select defaultValue="All Cameras" style={{ width: 120 }} onChange={this.handleChange}>
                                <Option value="Camera 1">Camera 1</Option>
                                <Option value="Camera 2">Camera 2</Option>
                                {/* Add <Option /> to add new camera */}
                            </Select>
                        </div>
                    </div>
                    <div>
                        <img src={url} />
                    </div>
                </div>
            </>
        )
    }
}

export default SelectCamera
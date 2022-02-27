import { Select } from 'antd';
import React, { Component, useState, props } from "react";

const { Option } = Select;

// function handleChange(value) {
//     console.log(`selected ${value}`);
// }

class SelectCamera extends React.Component {
    /**
     * video url and which camera type?
     */
    state = {
        url: '',
        camera: '',
    };

    handleChange(value) {
        console.log(`selected ${value}`);
    }

    render() {
        return (
            <>
                <div class="camera1">
                    <div class='text-dropdown'>
                        <div class='text'>
                            <p class='Title'>Camera 1</p>
                        </div>
                        <div class='dropdown1'>
                            <Select defaultValue="All Cameras" style={{ width: 120 }} onChange={handleChange}>
                                <Option value="Camera 1">Camera 1</Option>
                                <Option value="Camera 2">Camera 2</Option>
                            </Select>
                        </div>
                    </div>
                    <div>
                        <img src="http://localhost:5003/video" />
                    </div>
                </div>
            </>
        )
    }
}

export default SelectCamera
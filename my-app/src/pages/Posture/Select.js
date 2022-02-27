import { Select } from 'antd';
import React, { Component, useState, props } from "react";

const { Option } = Select;

function handleChange(value) {
    console.log(`selected ${value}`);
}

class selectCamera extends React.Component  {
    render() {
        return (
            <>
                <Select defaultValue="All Cameras" style={{ width: 120 }} onChange={handleChange}>
                    <Option value="Camera 1">Camera 1</Option>
                    <Option value="Camera 2">Camera 2</Option>
                </Select>
            </>
        )
    }
}

export default selectCamera
import { Select } from 'antd';

const { Option } = Select;

function handleChange(value) {
    console.log(`selected ${value}`);
}

function selectCamera() {
    return (
        <>
            <Select defaultValue="All Cameras" style={{ width: 120 }} onChange={handleChange}>
                <Option value="Camera 1">Camera 1</Option>
                <Option value="Camera 2">Camera 2</Option>
                <Option value="Camera 3">Camera 3</Option>
            </Select>
        </>
    )
}

export default selectCamera
import React, { Component, useState } from "react";
import { Menu } from 'antd';
import { history } from 'umi';
import './index.css';

function handleItem1Click(e) {
  history.push("/Posture")
}

function handleItem2Click(e) {
  history.push("/Posture")
}


const list = (
  <Menu>
    <Menu.Item key="1" onClick={handleItem1Click}>
      Camera 1
    </Menu.Item>
    <Menu.Item key="2" onClick={handleItem2Click}>
      Camera 2
    </Menu.Item>
  </Menu>
);

function menuClass() {
  return (
    <Menu>
      <Menu.Item key="1" onClick={handleItem1Click}>
        Camera 1
      </Menu.Item>
      <Menu.Item key="2" onClick={handleItem2Click}>
        Camera 2
      </Menu.Item>
    </Menu>
  )
}

export default menuClass
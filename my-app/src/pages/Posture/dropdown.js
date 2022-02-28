import React, { Component, useState, props } from "react";
import { Menu } from 'antd';
import { history } from 'umi';
import './index.css';
import App from './index'

function handleItem1Click(e) {
  history.push("/Posture")
}

function handleItem2Click(e) {
  history.push("/Posture")
}

function changecamera(){
  App.handleOptionChange();
}


const list = (
  <Menu>
    <Menu.Item key="1" onClick={handleItem1Click}>
      Camera 1
    </Menu.Item>
    <Menu.Item key="2" onClick={changecamera}>
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
      <Menu.Item key="2" onClick={changecamera}>
        Camera 2
      </Menu.Item>
    </Menu>
  )
}

export default menuClass
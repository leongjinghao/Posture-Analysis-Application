import React, { Component } from "react";
import Webcam from "react-webcam";

const WebcamComponent = () => <Webcam videoConstraints={videoConstraints}/>;

const videoConstraints = {
    width: 600,
    height: 450,
    facingMode: "user"
};

function WebcamClass(){
        return (
            <>
            <WebcamComponent />
            </>
        )
}

export default WebcamClass

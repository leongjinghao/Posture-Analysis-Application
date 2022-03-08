import React, { Component } from "react";

/**
 * Change the src in <img> to change camera.
 */
class AllCameras extends Component {
    render() {
        return (
            <div>
                <img
                    src="http://localhost:5003/video"
                    alt="Video1"
                    width="500"
                    height="400"
                />
                <img
                    src="add new link"
                    alt="Video1.2"
                    width="500"
                    height="400"
                />
                <img
                    src="add new link"
                    alt="Video1.3"
                    width="500"
                    height="400"
                />
                <img
                    src="add new link"
                    alt="Video2"
                    width="500"
                    height="400"
                />
            </div>
        );
    }
}

/**
 * Change the value if need to specify different src, alt.
 * Recreate the class if you need to add more cameras.
 */
class FirstCamera extends Component {
    render() {
        return (
            <div>
                <img
                    src="http://localhost:5003/video"
                    alt="Video1"
                    width="500"
                    height="400"
                />
            </div>
        );
    }
}

class SecondCamera extends Component {
    render() {
        return (
            <div>
                <img
                    src="http://localhost:5003/video"
                    alt="Video2"
                    width="500"
                    height="400"
                />
            </div>
        );
    }
}

export { AllCameras, FirstCamera, SecondCamera };
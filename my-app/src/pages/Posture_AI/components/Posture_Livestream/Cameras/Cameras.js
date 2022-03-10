import React, { Component } from "react";

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

export { FirstCamera, SecondCamera };
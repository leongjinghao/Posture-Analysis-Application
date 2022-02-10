import React from "react";

function Modal() {
    return (
        <div className="modalBackground">
            <div className="modalContainer">
                <button> X </button>
                <div className="title">
                    <h1>Are You Sure you want to continue?</h1>
                </div>
                <div className="body">
                    <p>The next page is awesome! Please work!</p>
                </div>
                <div className="footer">
                    <button>Cancel</button>
                    <button>Continue</button>
                </div>
            </div>
        </div>
    );
}

export default Modal;
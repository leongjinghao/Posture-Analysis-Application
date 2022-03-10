import React, { Component } from "react";
import "./styles.css";
import ProCard from "@ant-design/pro-card";
import PostureVideo from './components/Posture_Video';
import LiveStream from './components/Posture_Livestream';

class Posture_AI extends Component {
    render() {
        return (
            <>
                <ProCard tabs={{ type: 'card' }}>
                    <ProCard.TabPane key=" tab1" tab="LiveStream">
                        <LiveStream />
                    </ProCard.TabPane>

                    <ProCard.TabPane key=" tab2" tab="Posture Videos">
                        <PostureVideo />
                    </ProCard.TabPane>
                </ProCard>
            </>
        )
    }

}

export default Posture_AI;
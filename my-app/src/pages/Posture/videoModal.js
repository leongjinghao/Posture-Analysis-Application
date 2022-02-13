import React, { useEffect, useRef, useState } from 'react';
import { Modal, Button } from 'antd';
import './videoStyle.css';

function VideoModal({ title, url, visible, loading, handleOk, handleCancel }) {

    var videoName = url.replace('posture_video_recording/', '')

    return (
        <>
            <Modal
                destroyOnClose={true}
                width={'fit-content'}
                bodyStyle={{ height: 450, width: 'fit-content' }}
                visible={visible}
                title={title}
                onOk={handleOk}
                onCancel={handleCancel}
                footer={[
                    <Button href={url} download={url} type="primary" loading={loading} onClick={handleOk}>
                        Export
                    </Button>,
                    // Algorithm to download video
                    <Button
                        key="back"
                        type="primary"
                        loading={loading}
                        onClick={() => {
                            fetch('https://localhost:5001/VideoPath/' + videoName, { method: 'DELETE' });
                        }
                        }
                    >
                        Delete
                    </Button>,
                    // Algorithm to delete video

                ]}
            >
                <video className='video-modal' preload='metadata' controls autoPlay>
                    <source src={url} type='video/mp4' />
                </video>
            </Modal>
        </>
    )
}

export default VideoModal
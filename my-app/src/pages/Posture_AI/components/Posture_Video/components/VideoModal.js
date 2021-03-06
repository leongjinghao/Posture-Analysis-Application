import React from 'react';
import { Modal, Button } from 'antd';
import './styles.css';

function VideoModal({ url, visible, loading, handleOk, handleCancel }) {

    var videoName = url.replace('posture_video_recording/', '')

    return (
        <>
            <Modal
                destroyOnClose={true}
                width={'fit-content'}
                bodyStyle={{ height: 450, width: 'fit-content' }}
                visible={visible}
                title={videoName}
                onOk={handleOk}
                onCancel={handleCancel}
                footer={[
                    // Download videos
                    <Button href={url} download={url} type="primary" loading={loading} onClick={handleOk}>
                        Export
                    </Button>,
                    // Delete videos
                    <Button
                        key="back"
                        type="primary"
                        onClick={() => {
                            fetch('https://localhost:5001/PostureVideoPath/' + videoName, { method: 'DELETE' });
                            handleCancel;
                            // Add reloading of page after delete
                            location.reload();
                        }
                        }
                    >
                        Delete
                    </Button>,
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
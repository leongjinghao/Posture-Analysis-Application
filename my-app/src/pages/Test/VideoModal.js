import React from 'react';
import { Modal, Button } from 'antd';
import './VideoModal.css';

function VideoModal({ url, visible, loading, handleOk, handleCancel }) {
    return (
        <>
            <Modal
                maskStyle={{opacity: 0.1}}
                width={900}
                bodyStyle={{ height: 400, textAlign: 'center'}}
                visible={visible}
                title={url}
                onOk={handleOk}
                onCancel={handleCancel}
                footer={[
                    <Button href={url + '.mp4'} download='file' type="primary" loading={loading} onClick={handleOk}>
                        Export
                    </Button>,
                    // Algorithm to download video
                    <Button
                        key="link"
                        href="https://google.com"
                        type="primary"
                        loading={loading}
                        onClick={handleOk}
                    >
                        Delete
                    </Button>,
                    // Algorithm to delete video
                ]}
            >
                <video className='video-modal' preload='metadata' controls autoplay>
                    <source src={url + ".mp4"} />
                </video>
            </Modal>
        </>
    )
}

export default VideoModal
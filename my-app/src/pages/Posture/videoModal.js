import React from 'react';
import { Modal, Button } from 'antd';
import './VideoStyle.css';

function VideoModal({ url, visible, loading, handleOk, handleCancel }) {
    console.log(url)
    return (
        <>
            <Modal
                destroyOnClose={true}
                width={'fit-content'}
                bodyStyle={{ height: 450, width: 'fit-content' }}
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
                <video className='video-modal' preload='metadata' controls autoPlay>
                    <source src={url + ".mp4"} />
                </video>
            </Modal>
        </>
    )
}

export default VideoModal
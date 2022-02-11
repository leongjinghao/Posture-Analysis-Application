import React, { useEffect, useRef, useState } from 'react';
import { Modal, Button } from 'antd';
import './VideoStyle.css';

function VideoModal({ title, url, visible, loading, handleOk, handleCancel }) {

    // async function deleteVideo(item, url) {
    //     fetch(url + '/' + item, { method: 'DELETE' })
    //     handleCancel
    // }

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
                    <Button href={url} download='file' type="primary" loading={loading} onClick={handleOk}>
                        Export
                    </Button>,
                    // Algorithm to download video
                    <Button
                        key="back"
                        type="primary"
                        loading={loading}
                        onClick={
                            // fetch(url + '/' + title, { method: 'DELETE' }), 
                            handleCancel
                        }
                    >
                        Delete
                    </Button>,
                    // Algorithm to delete video

                ]}
            >
                <video className='video-modal' preload='metadata' controls autoPlay>
                    <source src={url} />
                </video>
            </Modal>
        </>
    )
}

export default VideoModal
import React, { useRef } from 'react';
import ProCard from '@ant-design/pro-card';

export default () => {
  return (
    <>
      <ProCard style={{ marginTop: 8 }} gutter={[16, 16]} wrap title="List of Videos" >
        <video width="auto" height="auto" controls>
          <source src='/video_sample/boxing.mp4' type='video/mp4'/>
        </video>
      </ProCard>
    </>
  );
};
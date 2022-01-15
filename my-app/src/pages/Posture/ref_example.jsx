import React, { useRef } from 'react';
import ProCard from '@ant-design/pro-card';

function DisplayVideo(props) {
  return (
    <div className='Video_Container'>
      <video width="326.4" height='326.4' controls>
        <source src='/video_sample/boxing.mp4' type='video/mp4' />
      </video>
    </div>
  )
}

export default () => {
  return (
    <div className='Video_Container'>
      <DisplayVideo/>
      
    </div>
    // <>
    //   <ProCard style={{ marginTop: 8 }} gutter={[16, 16]} wrap title="List of Videos" >
    //     <video width="auto" height='326.4' controls>
    //       <source src='/video_sample/boxing.mp4' type='video/mp4'/>
    //     </video>
    //     <video width="auto" height="326.4" controls>
    //       <source src='/video_sample/boxing2.mp4' type='video/mp4'/>
    //     </video>
    //   </ProCard>
    // </>
  );
};
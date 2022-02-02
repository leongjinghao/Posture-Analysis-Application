const express = require('express')
const app = express()
const videoStream = require('raspberrypi-node-camera-web-streamer');
videoStream.acceptConnections(app, {
    width: 1280,
    height: 720,
    fps: 16,
    encoding: 'JPEG',
    quality: 7 //lower is faster
}, '/stream.mjpg', true);

app.listen(3000, () => console.log(`Listening on port ${port}!`));
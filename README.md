# 2021-TEAM-03

[![PostureRecognitionAPI](https://github.com/leongjinghao/Posture-Analysis-Application/actions/workflows/dotnet.yml/badge.svg)](https://github.com/leongjinghao/Posture-Analysis-Application/actions/workflows/dotnet.yml)
[![ReactWebApplication](https://github.com/leongjinghao/Posture-Analysis-Application/actions/workflows/react.yml/badge.svg)](https://github.com/leongjinghao/Posture-Analysis-Application/actions/workflows/react.yml)

# Posture Detection

## Processes
<p align="center">
  <img width="960" height="540" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Posture_detection_process.png">
</p>
There are two phases in our posture detection feature. The program will first detect all the people on the video stream and crop out their bounding boxes for every frame. Those cropped bounding boxes will then be sent as an input into a pose estimator object for posture detection.

## Detect Person on Video Stream

<p align="center">
  <img width="640" height="360" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Person_Detection.gif">
</p>

YOLO is the open-source library used for person detection. After experimenting with many variants of the models available, the YOLOv4-Tiny model was selected. The rationale behind using this model is mainly because it has the fastest processing speed (by approximately 2-3 times), as compared to all the other variants available. In addition, it has a high detection rate which is on par with the non-Tiny variants. The downside of this model is that the bounding boxes detected are less consistent, as they can expand and contract by a small distance. Other non-Tiny variants have a more consistent bounding box size. Though this is not the main concern in this project as long as it has a high detection rate.

## Detect Posture of Person

<p align="center">
  <img width="640" height="360" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Posture_Detection.gif">
</p>

MediaPipe is the open-source library used for posture detection. For the posture detection process, multiple MediaPipe pose estimator objects will be initialised first. The cropped bounding boxes of persons retrieved from the person detection process will be used as the input for the mediaPipe pose estimator objects. It then outputs a list of landmarks (33 landmarks in total) of the input person's cropped bounding box, each with the x, y, and z coordinates. In this project, we will only be using the x and y coordinates for each of the landmarks.

# Person Detection in Danger Zone

## Ratio of Intersecting Area

<p align="center">
  <img width="1000" height="350" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Intersection_Area_Danger_Zone.png">
</p>

The administrator will first need to define the coordinates of the danger zone on the video stream. The polygon API from Python's Shapely package is then used to create the danger zone, blue quadrilateral above, logically on an XY plane (mapped with the video feed). Polygon of Person's bounding box detected is also created logically on the XY plane, represented by the brown quadrilateral above. To check if the person detected is within the danger zone, the intersection and area APIs are used. The intersection API returns a flag that determines if any two shapes are intersecting, and the area API returns the area of intersection between the two shapes. We can calculate the ratio of the intersecting area to the person's bounding box area, and define a threshold ratio to consider the person to be within the danger zone as shown above.

## Video Demo for Person Detection in Danger Zone

<p align="center">
  <img width="600" height="340" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Person_Detection_Danger_Zone.gif">
</p>

In this video demonstration, the threshold ratio is configured as 0.8. Hence, the person will only be considered to be within the danger zone if his or her intersection ratio is more than 80%. From the video, it can be observed that when more than 80% of the person body is within a danger zone, the person's bounding box is in turquoise (for good posture). Else, the person is considered to be outside of the danger zone and the person's bounding box is in green (represent good posture). The change in colour for the person's bounding box is to signify the different conditions in which the person is in.

# Bad Posture Recognition in Danger Zone

## Processes

<p align="center">
  <img width="1000" height="400" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Posture_Recognition_Danger_Zone_Process.png">
</p>

To integrate the feature for detecting person within danger zone, the process for posture recognition is revised to include the process of checking intersection ratio with danger zone. In addition to the existing model, another model has to be trained for recognising bad posture within danger zone. If the person is detected as outside the danger zone, then the normal model will be used for bad posture detection. Whereas, if the person is detected as within the danger zone, then the danger zone model will be used for bad posture detection.

## Video Demo for Person Detection in Danger Zone

<p align="center">
  <img width="600" height="340" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Posture_Recognition_Danger_Zone.gif">
</p>

In this video demonstration, it illustrates the usage of the different models for detecting bad posture depending if the person is detected to be within or outside of the danger zone. Observe that when the person detected is outside of the danger zone, the person's bounding box is either green (represent good posture) or red (represent bad posture). The red bounding box appears when the person is bending forward, which implies the usage of the normal model for recognising bad posture. In contrast, when the person detected is within the danger zone, the person's bounding box is either turquoise (represent good posture) or purple (represent bad posture). The purple bounding box appears when the person is sitting down and bending forward, which implies the usage of the danger zone model for recognising bad posture. The bending forward motion should not be detected as a bad posture for the danger zone model, we will discuss more on this observation in the following section.

# Storing Good and Bad Posture Recordings

<p align="center">
  <img width="960" height="540" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Saving_good_and_bad_posture_recording_process.png">
</p>

<div align="center">

List             |  Description
:--------------- |:---------------
personPostureState`[n]` | To keep track of person’s posture state
framesArray`[[0_frame0, …, 0_frameX], …, [n_frame0, …, n_frameY]]` | To buffer frames to be merged into a video

</div>

In this feature addition, instances of consecutive good or bad posture detected for each person are saved as a video recording. The person tracking feature developed from the previous iteration is utilised to track each person's posture state. Each person's posture state is captured within the personPostureState list and the consecutive good or bad posture frames of each person are buffered within the framesArray list. The buffered frames are merged into a video using OpenCV's video writer whenever there is a posture state transition.

<p align="center">
  <img width="405" height="450" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/demo_video_saving_full.gif">
</p>

In this video demonstration, the person detected on video stream first performs a series of good posture, then a series of bad posture, and finally another series of good posture. Initially, the personPostureState would store the value "good" as the person's posture state at index 0. As the person's posture state did not change for consecutive frames, the frames of good posture detected would continue to buffer within the 2D framesArray list at the same index(0). Once the person's posture state detected transit to "bad" at the second period, the OpenCV video writer function is used to write out all the frames buffered at framesArray[0] as a video recording. The newly detected bad posture frame will then replace the buffered list and continue to accumulate the consecutive bad posture frames. Similar process will be executed when the person's posture state transit back to "good" at the third period.

<div align="center">

First Period<br>`good_posture_1642659487.39878.avi` | Second Period<br>`bad_posture_1642659496.6107595.avi` | Thrid Period<br>`good_posture_1642659504.7347593.avi`
:-------------------------:|:-------------------------:|:-------------------------:
![](https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/demo_video_saving_part_1.gif)  |  ![](https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/demo_video_saving_part_2.gif) | ![](https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/demo_video_saving_part_3.gif)

</div>

## Execution of Multiple Instances Concurrently

<p align="center">
  <img width="960" height="540" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Execution_of_multiple_instances.gif">
</p>

In this feature addition, multiple instances of the posture recognition python script are made to be executable concurrently. The command-line argument is utilised to indicate the input for video input source and the camera ID for retrieval of danger zone coordinates for defining the danger zone(s). A bash script is then used to specify the number of instances and input configuration to execute multiple instances of the posture recognition python script in parallel. 

## Logging of Posture Data to Database through .Net 5 API

Revision is made on the posture recognition python script to log the posture data upon detection and recognition. Every posture data detected per frame are automatically logged in the database through the use of post request via the implemented .Net 5 API. The above image display the sample logged posture data from the database.

<p align="center">
  <img width="960" height="250" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Posture_log_data_sample.png">
</p>

## Usage of POST Request

<p align="center">
  <img width="740" height="415" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Saving_good_and_bad_posture_recording_process_addition.png">
</p>

The POST request triggered inserts the relative video path of new video recordings generated during the execution of the posture recognition into the VideoPaths table. The diagram above illustrates the sequence of events constituting the storage of consecutive good or bad posture detected. As explained in the previous customer day, the consecutive good or bad posture would be buffered and stored as an mp4 file upon posture state transition. After which the addition of the POST request is introduced to insert the relative path of the newly generated video into the VideoPaths table.

# Establish Video Stream End Points

<p align="center">
  <img width="800" height="400" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Video_stream_endpoint_process_flask.png">
</p>

The diagram above illustrates the flow of the Video Stream Feature. Firstly, frames from the CCTV camera will be taken and streamed to an endpoint using Flask. Flask will stream to an endpoint at localhost, port 5002. Next, our posture recognition script will be run using the stream from the endpoint as input. The output of the posture recognition will be streamed to another endpoint, localhost port 5003, using Flask as well.

## Python Script and HTML
The primary python script that will be used to gather the frames from the CCTV camera uses the following modules:
* OpenCV 
* Flask

OpenCV will be used to retrieve the live stream from the camera in frames. Each frame is taken continuously and streamed to the endpoint This will cause the endpoint to look like a live stream despite taking data from the camera one stream at a time.

Flask will be used to stream the frames taken from the camera to an endpoint. This endpoint will be hosted on the localhost, port 5002. 

# React Web Application

<p align="center">
  <img width="920" height="420" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/React_UI_1.png">
</p>

To facilitate subsequent integration effort, all project teams had reached a consensus on the layout of the web application and agreed to employed Ant Design and followed the template designed and developed.
The layout of the page is finalised with the video name below containing the type of posture (good/bad) and the date and time of the video. There are a few additional things implemented such as the video modal, downloading of the video and deletion of the videos.

# Video Stream Integration

<div align="center">

![image](https://user-images.githubusercontent.com/73938217/160342693-63e879a0-a2be-4e10-bc5e-09c2953130b2.png)

</div>

The above image shows the Posture AI module integrated into the single web application hosted on the cloud server. The Posture AI module consists of the LiveStream and Posture Videos page, with the LiveStream page displaying the Posture AI analytic output on the multiple camera feeds, and the Posture Videos page displaying the stored posture video recordings.

# Notification

## Notification Algorithm (with buffer length only)

<p align="center">
  <img width="1000" height="380" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Notification_algo_bufferlen_only.png">
</p>

The notification feature is the latest feature added in this iteration. The algorithm for the notification feature is implemented by utilising the bad posture frames buffer length. However, just using the buffer length is not sufficient. As illustrated in the above diagram, in the event that there were 2 consecutive blocks of bad posture frames, 2 notifications will be sent out to the administrator. Which can potentially lead to notification spam.

## Notification Algorithm (with buffer length and notify flag)

<p align="center">
  <img width="1000" height="300" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Notification_algo_bufferlen_and_flag.png">
</p>

To address this issue, a notify flag is introduced to indicate if the current block of bad posture frames is transiting from a block of good posture frames. Thus, a notification can be configured to only be triggered if the notify flag is set to true, and the buffer length reaches the threshold. After a notification is sent, the notify flag is set back to false. Therefore, the subsequent consecutive block of bad posture frames will not trigger another notification even if the buffer length reaches the threshold.

## Notification Implementation for React Web Application

<p align="center">
  <img width="1000" height="400" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Notification_implementation_react.png">
</p>

The diagram above illustrates the actual implementation of the notification feature for the react web application. On the posture AI python script, if the notification feature is triggered, the notification API implemented by C1 gets called. Which will retrieve all the admin IDs and insert new notification records with all the admin IDs and the configured message in the notification table. The react web application will then pick up the updated notifications from the newly inserted records and display them on the notification tab accordingly.

## Notification Implementation for Email

<div align="center">

Attributes | Description
------------- | -------------
sender_email | The system email address used for sending out email notification
password | The system email's application password, to be generated
recipients | The list of administrator email address(es)
message | The email notification's message content

</div>

The email notification feature is implemented in the email notifier class. It contains the above-listed attributes primarily for configuration, consisting of the sender email, the application password for authentication, the recipients of the email, and the message body. 

<p align="center">
  <img width="1000" height="350" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Notification_implementation_email.png">
</p>

The diagram above illustrates the actual implementation of the email notification feature. On the posture AI python script, if the notification feature is triggered, it will call the send email function defined in the email notifier class, which then sends the email notification to the administrators' email as specified in the email notifier object.

Further documentation and demonstrations can be found in the wiki sections:
- Person & posture detection, model training framework: https://github.com/leongjinghao/Posture-Analysis-Application/wiki/2.-Customer-Day-1#232-features-developed
- Detection of person in danger zone/ vice versa: https://github.com/leongjinghao/Posture-Analysis-Application/wiki/3.-Customer-Day-2#232-features-developed
- Backend implementation (DB & WebAPIs), Storage of videos captured: https://github.com/leongjinghao/Posture-Analysis-Application/wiki/4.-Customer-Day-3#232-features-developed
- Frontend implementation, multi-instance execution: https://github.com/leongjinghao/Posture-Analysis-Application/wiki/5.-Customer-Day-4#232-features-developed
- Notification feature, integration: https://github.com/leongjinghao/Posture-Analysis-Application/wiki/6.-Final-Demonstration#132-features-developed

Proceed to the wiki section for full documentation:
https://github.com/leongjinghao/Posture-Analysis-Application/wiki

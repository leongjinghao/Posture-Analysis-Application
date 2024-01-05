# 2021-TEAM-03

[![PostureRecognitionAPI](https://github.com/leongjinghao/Posture-Analysis-Application/actions/workflows/dotnet.yml/badge.svg)](https://github.com/leongjinghao/Posture-Analysis-Application/actions/workflows/dotnet.yml)
[![ReactWebApplication](https://github.com/leongjinghao/Posture-Analysis-Application/actions/workflows/react.yml/badge.svg)](https://github.com/leongjinghao/Posture-Analysis-Application/actions/workflows/react.yml)

### Posture Detection

#### Processes
<p align="center">
  <img width="960" height="540" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Posture_detection_process.png">
</p>
There are two phases in our posture detection feature. The program will first detect all the people on the video stream and crop out their bounding boxes for every frame. Those cropped bounding boxes will then be sent as an input into a pose estimator object for posture detection.

#### Detect Person on Video Stream

<p align="center">
  <img width="640" height="360" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Person_Detection.gif">
</p>

YOLO is the open-source library used for person detection. After experimenting with many variants of the models available, the YOLOv4-Tiny model was selected. The rationale behind using this model is mainly because it has the fastest processing speed (by approximately 2-3 times), as compared to all the other variants available. In addition, it has a high detection rate which is on par with the non-Tiny variants. The downside of this model is that the bounding boxes detected are less consistent, as they can expand and contract by a small distance. Other non-Tiny variants have a more consistent bounding box size. Though this is not the main concern in this project as long as it has a high detection rate.

#### Detect Posture of Person

<p align="center">
  <img width="640" height="360" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Posture_Detection.gif">
</p>

MediaPipe is the open-source library used for posture detection. For the posture detection process, multiple MediaPipe pose estimator objects will be initialised first. The cropped bounding boxes of persons retrieved from the person detection process will be used as the input for the mediaPipe pose estimator objects. It then outputs a list of landmarks (33 landmarks in total) of the input person's cropped bounding box, each with the x, y, and z coordinates. In this project, we will only be using the x and y coordinates for each of the landmarks.

### Person Detection in Danger Zone

#### Ratio of Intersecting Area

<p align="center">
  <img width="1000" height="350" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Intersection_Area_Danger_Zone.png">
</p>

The administrator will first need to define the coordinates of the danger zone on the video stream. The polygon API from Python's Shapely package is then used to create the danger zone, blue quadrilateral above, logically on an XY plane (mapped with the video feed). Polygon of Person's bounding box detected is also created logically on the XY plane, represented by the brown quadrilateral above. To check if the person detected is within the danger zone, the intersection and area APIs are used. The intersection API returns a flag that determines if any two shapes are intersecting, and the area API returns the area of intersection between the two shapes. We can calculate the ratio of the intersecting area to the person's bounding box area, and define a threshold ratio to consider the person to be within the danger zone as shown above.

#### Video Demo for Person Detection in Danger Zone

<p align="center">
  <img width="600" height="340" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Person_Detection_Danger_Zone.gif">
</p>

### Bad Posture Recognition in Danger Zone

#### Processes

<p align="center">
  <img width="1000" height="400" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Posture_Recognition_Danger_Zone_Process.png">
</p>

To integrate the feature for detecting person within danger zone, the process for posture recognition is revised to include the process of checking intersection ratio with danger zone. In addition to the existing model, another model has to be trained for recognising bad posture within danger zone. If the person is detected as outside the danger zone, then the normal model will be used for bad posture detection. Whereas, if the person is detected as within the danger zone, then the danger zone model will be used for bad posture detection.

#### Video Demo for Person Detection in Danger Zone

<p align="center">
  <img width="600" height="340" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Posture_Recognition_Danger_Zone.gif">
</p>

In this video demonstration, it illustrates the usage of the different models for detecting bad posture depending if the person is detected to be within or outside of the danger zone. Observe that when the person detected is outside of the danger zone, the person's bounding box is either green (represent good posture) or red (represent bad posture). The red bounding box appears when the person is bending forward, which implies the usage of the normal model for recognising bad posture. In contrast, when the person detected is within the danger zone, the person's bounding box is either turquoise (represent good posture) or purple (represent bad posture). The purple bounding box appears when the person is sitting down and bending forward, which implies the usage of the danger zone model for recognising bad posture. The bending forward motion should not be detected as a bad posture for the danger zone model, we will discuss more on this observation in the following section.

### React Web Application

<div align="center">

![image](https://user-images.githubusercontent.com/73938217/160342693-63e879a0-a2be-4e10-bc5e-09c2953130b2.png)

</div>

The above image shows the Posture AI module integrated into the single web application hosted on the cloud server. The Posture AI module consists of the LiveStream and Posture Videos page, with the LiveStream page displaying the Posture AI analytic output on the multiple camera feeds, and the Posture Videos page displaying the stored posture video recordings.

Further documentations and demonstrations can be found in the wiki sections:
- Person & posture detection, model training framework: https://github.com/leongjinghao/Posture-Analysis-Application/wiki/2.-Customer-Day-1#232-features-developed
- Detection of person in danger zone/ vice versa: https://github.com/leongjinghao/Posture-Analysis-Application/wiki/3.-Customer-Day-2#232-features-developed
- Backend implementation (DB & WebAPIs), Storage of videos captured: https://github.com/leongjinghao/Posture-Analysis-Application/wiki/4.-Customer-Day-3#232-features-developed
- Frontend implementation, multi-instance execution: https://github.com/leongjinghao/Posture-Analysis-Application/wiki/5.-Customer-Day-4#232-features-developed
- Notification feature, integration: https://github.com/leongjinghao/Posture-Analysis-Application/wiki/6.-Final-Demonstration#132-features-developed

Proceed to the wiki section for full documentation:
https://github.com/leongjinghao/Posture-Analysis-Application/wiki

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

#### Detect Posture of Person

<p align="center">
  <img width="640" height="360" src="https://github.com/leongjinghao/Posture-Analysis-Application/blob/main/wiki_media/Posture_Detection.gif">
</p>

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

### 1.5.3. React Web Application

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

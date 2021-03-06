import ast
import datetime
import math
import sys
import cv2
import numpy as np
import mediapipe as mp
import time
import torch
import requests
from model_training.train_model import predict, MLP
from shapely.geometry import Polygon
from urllib3.exceptions import InsecureRequestWarning
from flask import Flask, render_template, Response
from email_notification import EmailNotifier

# Used for establishing flask endpoint
app = Flask(__name__)

# CLI argument(s)
args = sys.argv[1:]

# video stream source
cap = cv2.VideoCapture(args[0])

# confidence threshold for person detection
confThreshold = 0.5
# score threshold for bounding box suppression
nmsThreshold = 0.3
# relative start time for fps calculation
pTime = 0

# coco class name
classNames = []
with open('posture_recognition_python_scripts/YOLO_config/coco.names', 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# YOLO model configurations
modelConfiguration = 'posture_recognition_python_scripts/YOLO_config/yolov4-tiny.cfg'
modelWeights = 'posture_recognition_python_scripts/YOLO_config/yolov4-tiny.weights'

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# mediapipe posture estimator object instantiation
personCount = 10
mpPose = [mp.solutions.pose for i in range(personCount)]
pose = [mpPose[i].Pose(min_detection_confidence=0.8) for i in range(personCount)]
mpDraw = mp.solutions.drawing_utils

# arrays to keep track on the coordinates of ctr point bbox used in previous frames by each of the posture estimator obj
poseEstimatorDim = [[0.0] * 2] * personCount
poseEstimatorInUse = []
boxDistDiff = [0.0] * personCount

# load model
normalZoneModel = torch.load('posture_recognition_python_scripts/model_training/models/normal_zone_model.pth')
dangerZoneModel = torch.load('posture_recognition_python_scripts/model_training/models/danger_zone_model.pth')

# suppress wanning from SSL verification
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# retieve entries of danger zone coordinates according to the cameraId specified in CLI argument
response = requests.get("https://localhost:5001/DangerZoneCoordinates/" + str(args[1]), verify=False)
# interprete using json format
data = response.json()
# list to store all the danger zone coordinates for the cameraId specified
dangerZone = []
# append entries of danger zone coordinates retrieved into the list
for row in data:
    dangerZone.append(ast.literal_eval("[" + row["coordinates"] + "]"))

# create a polygon for each danger zone
dangerZonePolygon = [Polygon(dangerZone[i]) for i in range(len(dangerZone))]
# threshold of intersection ratio
intersectionThreshold = 0.8

# list to store the posture state (good or bad) of each person
personPostureState = [None] * personCount
# list of frames buffer for each person
framesArray = [[]] * personCount

# minimum threshold of buffered bad posture frames to notify supervisor, based on 15 fps
bufferFrameThreshold = 75
# flag to track to if notification is required, false by default
toNotifyFlag = False

def multiPersonPostureRecognition(outputs, frame):
    # STEP 1: Detect each person on frame (frame) #
    hT, wT, cT = frame.shape
    bbox = []
    classIds = []
    confs = []

    for output in outputs:
        for det in output:
            # first 5 elements are the x, y values, width, height of bounding box, and detection flag
            # remaining 80 elements are the confidence level for detection of each coco.name items
            scores = det[5:]
            # out of the 80 elements, get index of the highest scored classname identified
            classId = np.argmax(scores)
            # if object detected is not not a person, skip this object
            if not classId == 0:
                continue
            confidence = scores[classId]
            # if confidence level for person detected is higher than threshold, store the bounding box param
            if confidence > confThreshold:
                w, h = int(det[2] * wT), int(det[3] * hT)
                x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))

    # suppress duplicated bounding boxes
    indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold, top_k=personCount)

    # STEP 2: Posture Detection for each person detected #
    # for each person detected
    for i in indices:
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]

        # calculate center point of current person's bounding box
        ctr_pt = [float(x + w / 2), float(y + h / 2)]
        for j in range(personCount):
            # if posture estimator j is in used already, prevent it from being use by current person
            # by setting distance difference to inf
            if j in poseEstimatorInUse:
                boxDistDiff[j] = float("inf")
            # else calculate the difference in distance for the center point for each posture estimator object
            else:
                boxDistDiff[j] = math.sqrt(pow(poseEstimatorDim[j][0] - ctr_pt[0], 2) + pow(poseEstimatorDim[j][1] - ctr_pt[1], 2))

        # retrieve the index of posture estimator that was used for the person detected previously
        # by selecting the least distance difference
        poseObjIdx = np.argmin(boxDistDiff)
        poseEstimatorDim[poseObjIdx] = ctr_pt
        poseEstimatorInUse.append(poseObjIdx)

        # crop the frame (crop_frame) for each person detected using the bounding box para
        crop_frame = frame[y: y + h, x: x + w]
        crop_frame_h, crop_frame_w, _ = crop_frame.shape

        # skip if frame cropped is empty
        try:
            frameRGB = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2RGB)
        except:
            continue

        # To improve performance, optionally mark the frame as not writeable to pass by reference.
        frameRGB.flags.writeable = False

        # get posture landmarks
        results = pose[poseObjIdx].process(frameRGB)

        # if no posture landmark detected, continue on next frame
        if results.pose_landmarks is None:
            continue

        # draw landmarks on the cropped frame
        mpDraw.draw_landmarks(crop_frame, results.pose_landmarks, mpPose[poseObjIdx].POSE_CONNECTIONS)

        # bundle landmarks data of person together to be used for model feedforward for posture recognition
        postureLm = []
        for _, lm in enumerate(results.pose_landmarks.landmark):
            postureLm.append(lm.x)
            postureLm.append(lm.y)

        # STEP 3: Check if person is in danger zone, use the respective models for posture recognition #
        # create polygon of person using bounding box coordinates
        personPolygon = Polygon([[x, y], [x + w, y], [x + w, y + h], [x, y + h]])

        # danger zone intersection flag to capture if person detected is in danger zone, false by default
        intersectFlag = False

        # calculate the intersection of polygons for person detected and each danger zone
        for j in range(len(dangerZonePolygon)):
            intersection = personPolygon.intersects(dangerZonePolygon[j])

            # calculate the ratio of intersection area to the person's bounding box
            intersectAreaRatio = personPolygon.intersection(dangerZonePolygon[j]).area / personPolygon.area

            # if person is in the danger zone, and ratio of intersecting area is over threshold,
            # set intersection flag = true
            if (intersection is True) and (intersectAreaRatio > intersectionThreshold):
                intersectFlag = True

                # break out of loop once person is detected in any danger zone, for optimisation
                break

        # if person detected is in one of the danger zone
        if intersectFlag is True:

            # retrieve toNotifyFlag from global scope
            global toNotifyFlag

            # if bad posture detected
            if predict(postureLm, dangerZoneModel).round() == float(1):
                
                # bounding box colour is purple
                bboxColour = (255, 0, 255)
                
                # log bad posture detected in database through post request
                requests.post(
                    url = "https://localhost:5001/PostureLog", 
                    json = {'cameraId': int(args[1]),
                            'zone': 'danger',
                            'postureLandmarks': ",".join([str(lm) for lm in postureLm]),
                            'classification': 'bad'},
                    verify = False)

                # if the person was performing good posture previously or buffer length is more than 105 (7sec for 15fps video),
                # consolidate and save the good posture frames of the person into a video
                # note: poseObjIdx can be mapped to a person
                if personPostureState[poseObjIdx] != "bad" or len(framesArray[poseObjIdx]) == 105:
                    
                    # set video name according to context
                    if personPostureState[poseObjIdx] != "bad":
                        # past buffered frames are good posture frames
                        videoOutputName = 'good_posture_%s.mp4'%datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
                        
                        # set flag to track to if notification is required, 
                        # i.e. next block of buffered frame is bad posture, would require notifying supervisor
                        # as posture transit from good posture to bad posture, with 105 buffered bad posture frames (7 seconds)
                        toNotifyFlag = True

                    else:
                        # past buffered frames are bad posture frames (buffered length == 105)
                        videoOutputName = 'bad_posture_%s.mp4'%datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
                        
                        # unset flag to track if notification is required,
                        # as past buffered frames are already blocks of bad posture frames
                        toNotifyFlag = False

                    # drop unstable frames of detection with total buffer frame <= 5
                    if len(framesArray[poseObjIdx]) > 5:
                        
                        # store buffered frames of the detected person's good posture as video output in react public folder
                        out = cv2.VideoWriter('my-app\public\\posture_video_recording\%s'%videoOutputName, cv2.VideoWriter_fourcc(*'avc1'), 15, (wT, hT))

                        for k in range(len(framesArray[poseObjIdx])):
                            out.write(framesArray[poseObjIdx][k])
                        
                        out.release()

                        # log video output path in database through post request
                        requests.post(
                            url = "https://localhost:5001/PostureVideoPath", 
                            json = {'postureVideoPath': "posture_video_recording/%s"%videoOutputName},
                            verify = False)
                    
                    # set person's posture state
                    personPostureState[poseObjIdx] = "bad"
                    
                    # replace buffer with the person's newly detected bad posture frame
                    framesArray[poseObjIdx] = [frame]

                # else the person was performing bad posture previously,
                # append bad posture frame to the framesArray
                else:
                    framesArray[poseObjIdx].append(frame)
                
                # Check only once if the notify flag is set to true and buffered length is == bufferFrameThreshold
                if toNotifyFlag == True and len(framesArray[poseObjIdx]) == bufferFrameThreshold:
                    
                    # send email notification
                    message = """\
                    Subject: Bad Posture Detection

                    This message is sent from Python."""

                    emailNotifier = EmailNotifier(["leongjinghao@gmail.com"])
                    emailNotifier.setMessage(message)
                    # emailNotifier.sendEmail()

                    print("NOTIFIED HERE!!!")
                        
            # else, it is a good posture
            else:
                # bounding box colour is cyan
                bboxColour = (255, 255, 0)
                
                # log good posture detected in database through post request
                requests.post(
                    url = "https://localhost:5001/PostureLog", 
                    json = {'cameraId': int(args[1]),
                            'zone': 'danger',
                            'postureLandmarks': ",".join([str(lm) for lm in postureLm]),
                            'classification': 'good'},
                    verify = False)
                
                # if the person was performing bad posture previously or buffer length is more than 105 (7sec for 15fps video),
                # consolidate and save the bad posture frames of the person into a video
                # note: poseObjIdx can be mapped to a person
                if personPostureState[poseObjIdx] != "good" or len(framesArray[poseObjIdx]) == 105:
                    
                    # set video name according to context
                    if personPostureState[poseObjIdx] != "good":
                        # past buffered frames are bad posture frames (buffered length == 105)
                        videoOutputName = 'bad_posture_%s.mp4'%datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
                    else:
                        # past buffered frames are good posture frames
                        videoOutputName = 'good_posture_%s.mp4'%datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")

                    # drop unstable frames of detection with total buffer frame <= 5
                    if len(framesArray[poseObjIdx]) > 5:
                        
                        # store buffered frames of the detected person's bad posture as video output in react public folder
                        out = cv2.VideoWriter('my-app\public\\posture_video_recording\%s'%videoOutputName, cv2.VideoWriter_fourcc(*'avc1'), 15, (wT, hT))
                        
                        for k in range(len(framesArray[poseObjIdx])):
                            out.write(framesArray[poseObjIdx][k])
                        
                        out.release()

                        # log video output path in database through post request
                        requests.post(
                            url = "https://localhost:5001/PostureVideoPath", 
                            json = {'postureVideoPath': "posture_video_recording/%s"%videoOutputName},
                            verify = False)
                    
                    # set person's posture state
                    personPostureState[poseObjIdx] = "good"

                    # replace buffer with the person's newly detected good posture frame
                    framesArray[poseObjIdx] = [frame]

                # else the person was performing good posture previously,
                # append good posture frame to the framesArray
                else:
                    framesArray[poseObjIdx].append(frame)

        # else person is not in any danger zone
        else:
            # if bad posture detected
            if predict(postureLm, normalZoneModel).round() == float(1):
                # bounding box colour is red
                bboxColour = (0, 0, 255)
                
                # log bad posture detected in database through post request
                requests.post(
                    url = "https://localhost:5001/PostureLog", 
                    json = {'cameraId': int(args[1]),
                            'zone': 'normal',
                            'postureLandmarks': ",".join([str(lm) for lm in postureLm]),
                            'classification': 'bad'},
                    verify = False)
                
                # if the person was performing good posture previously or buffer length is more than 105 (7sec for 15fps video), 
                # consolidate and save the good posture frames of the person into a video
                # note: poseObjIdx can be mapped to a person
                if personPostureState[poseObjIdx] != "bad" or len(framesArray[poseObjIdx]) == 105:
                    
                    # set video name according to context
                    if personPostureState[poseObjIdx] != "bad":
                        # past buffered frames are good posture frames
                        videoOutputName = 'good_posture_%s.mp4'%datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
                        
                        # set flag to track to if notification is required, 
                        # i.e. next block of buffered frame is bad posture, would require notifying supervisor
                        # as posture transit from good posture to bad posture, with 105 buffered bad posture frames (7 seconds)
                        toNotifyFlag = True

                    else:
                        # past buffered frames are bad posture frames (buffered length == 105)
                        videoOutputName = 'bad_posture_%s.mp4'%datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
                        
                        # unset flag to track if notification is required,
                        # as past buffered frames are already blocks of bad posture frames
                        toNotifyFlag = False
                        
                    # drop unstable frames of detection with total buffer frame <= 5
                    if len(framesArray[poseObjIdx]) > 5:
                        
                        # store buffered frames of the detected person's good posture as video output in react public folder
                        out = cv2.VideoWriter('my-app\public\\posture_video_recording\%s'%videoOutputName, cv2.VideoWriter_fourcc(*'avc1'), 15, (wT, hT))
                        
                        for k in range(len(framesArray[poseObjIdx])):
                            out.write(framesArray[poseObjIdx][k])

                        out.release()

                        # log video output path in database through post request
                        requests.post(
                            url = "https://localhost:5001/PostureVideoPath", 
                            json = {'postureVideoPath': "posture_video_recording/%s"%videoOutputName},
                            verify = False)
                    
                    # set person's posture state
                    personPostureState[poseObjIdx] = "bad"
                    
                    framesArray[poseObjIdx] = [frame]

                # else the person was performing bad posture previously,
                # append bad posture frame to the framesArray
                else:
                    framesArray[poseObjIdx].append(frame)
                
                # Check only once if the notify flag is set to true and buffered length is == bufferFrameThreshold
                if toNotifyFlag == True and len(framesArray[poseObjIdx]) == bufferFrameThreshold:
                    
                    # send email notification
                    message = """\
                    Subject: Bad Posture Detection

                    This message is sent from Python."""

                    emailNotifier = EmailNotifier(["leongjinghao@gmail.com"])
                    emailNotifier.setMessage(message)
                    # emailNotifier.sendEmail()

                    print("NOTIFIED HERE!!!")
            
            # else, it is a good posture
            else:
                # bounding box colour is green
                bboxColour = (0, 255, 0)
                
                # log good posture detected in database through post request
                requests.post(
                    url = "https://localhost:5001/PostureLog", 
                    json = {'cameraId': int(args[1]),
                            'zone': 'normal',
                            'postureLandmarks': ",".join([str(lm) for lm in postureLm]),
                            'classification': 'good'},
                    verify = False)

                # if the person was performing bad posture previously or buffer length is more than 105 (7sec for 15fps video), 
                # consolidate and save the bad posture frames of the person into a video
                # note: poseObjIdx can be mapped to a person
                if personPostureState[poseObjIdx] != "good" or len(framesArray[poseObjIdx]) == 105:
                    
                    # set video name according to context
                    if personPostureState[poseObjIdx] != "good":
                        # past buffered frames are bad posture frames (buffered length == 105)
                        videoOutputName = 'bad_posture_%s.mp4'%datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
                    else:
                        # past buffered frames are good posture frames
                        videoOutputName = 'good_posture_%s.mp4'%datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")

                    # drop unstable frames of detection with total buffer frame <= 5
                    if len(framesArray[poseObjIdx]) > 5:
                        
                        # store buffered frames of the detected person's good posture as video output in react public folder
                        out = cv2.VideoWriter('my-app\public\\posture_video_recording\%s'%videoOutputName, cv2.VideoWriter_fourcc(*'avc1'), 15, (wT, hT))
                        
                        for k in range(len(framesArray[poseObjIdx])):
                            out.write(framesArray[poseObjIdx][k])
                        
                        out.release()

                        # log video output path in database through post request
                        requests.post(
                            url = "https://localhost:5001/PostureVideoPath", 
                            json = {'postureVideoPath': "posture_video_recording/%s"%videoOutputName},
                            verify = False)
                    
                    # set person's posture state
                    personPostureState[poseObjIdx] = "good"

                    framesArray[poseObjIdx] = [frame]

                # else the person was performing good posture previously,
                # append good posture frame to the framesArray
                else:
                    framesArray[poseObjIdx].append(frame)

        # display bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), bboxColour, 2)

        # label for object and confidence
        cv2.putText(frame,
                    f'{classNames[classIds[i]].upper()} {int(confs[i] * 100)}% {str("estimator ID ") + str(poseObjIdx)}',
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

def instance(source): 
    while True:
        global pTime
        global poseEstimatorInUse
        
        success, frame = cap.read()

        # if video stream ended
        if not success:
            print('End of video stream from camera %s...'%args[1])
            sys.exit()

        # convert coordinates (pts) of all danger zone to int32 format
        pts = [np.array(dangerZone[i], np.int32) for i in range(len(dangerZone))]
        # plot polygons of all danger zones on video steam
        for i in range(len(dangerZone)):
            cv2.polylines(frame, [pts[i]], True, (255, 0, 0), 2)

        # inputs from frame are stored in a blob, which will be used for the model input
        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (320, 320), [0, 0, 0], 1, crop=False)

        # set the blob as input for model
        net.setInput(blob)

        # YOLO's 3 output layers
        layerNames = net.getLayerNames()
        outputNames = [layerNames[i - 1] for i in net.getUnconnectedOutLayers()]

        # retrieve object detection data
        outputs = net.forward(outputNames)

        # reset posture estimator in use for every new frame
        poseEstimatorInUse = []

        # Detect person on frame, then perform posture recognition based on cropped frame of person
        multiPersonPostureRecognition(outputs, frame)

        # show FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, "{:.1f} FPS".format(float(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # display video stream with posture landmarks plotted
        # frame = cv2.resize(frame, (1270, 720))
        # cv2.imshow('Video Stream', frame)
        # cv2.waitKey(1)
        
        # Function to output video stream on flask endpoint
        ret, buffer = cv2.imencode('.jpg', frame)
        frameBuffer = buffer.tobytes()
        yield (b'--frameBuffer\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frameBuffer + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(instance(cap), mimetype='multipart/x-mixed-replace; boundary=frameBuffer')


if __name__ == "__main__":
    app.run(port=int(args[2]), debug=True)

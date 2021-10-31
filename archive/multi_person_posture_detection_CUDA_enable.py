import cv2
import numpy as np
import mediapipe as mp
import time
import torch
from neural_network.model_training import predict, MLP


# video stream source
cap = cv2.VideoCapture('../video_sample/dancing2.mp4')
# confidence threshold for object detection
confThreshold = 0.5
# score threshold for bounding box suppression
nmsThreshold = 0.3
# relative start time for fps calculation
pTime = 0

# coco class name
classNames = []
with open('../YOLO_config/coco.names', 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# YOLO model configurations
modelConfiguration = '../YOLO_config/yolov4-tiny.cfg'
modelWeights = '../YOLO_config/yolov4-tiny.weights'

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

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
model = torch.load('../model_training/model.pth')

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
                break
            confidence = scores[classId]
            # if confidence level for person detected is higher than threshold, store the bounding box param
            if confidence > confThreshold:
                w, h = int(det[2] * wT), int(det[3] * hT)
                x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))

    # suppress duplicated bounding boxes
    indicies = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold, top_k=personCount)

    # STEP 2: Posture Recognition for each person detected #
    # for each person detected
    for i in indicies:
        #i = i[0]
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]

        # calculate center point of current person's bounding box
        ctr_pt = [float(x + w / 2), float(y + h / 2)]
        for j in range(personCount):
            # if posture estimator j is in used already, prevent it from being use by current person by setting distance difference to inf
            if j in poseEstimatorInUse:
                boxDistDiff[j] = float("inf")
            # else calculate the difference in distance for the center point for each posture estimator object
            else:
                boxDistDiff[j] = abs(poseEstimatorDim[j][0] - ctr_pt[0]) + abs(poseEstimatorDim[j][1] - ctr_pt[1])

        # retrieve the index of posture estimator that was used for the person detected previously
        # by selecting the least distance difference
        poseObjIdx = np.argmin(boxDistDiff)
        poseEstimatorDim[poseObjIdx] = ctr_pt
        poseEstimatorInUse.append(poseObjIdx)

        # crop the frame (crop_frame) for each person detected using the bounding box para
        crop_frame = frame[y: y + h, x: x + w]
        #cv2.imshow('test', crop_frame)
        #breakpoint()
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

        postureLm = []
        for id, lm in enumerate(results.pose_landmarks.landmark):
            postureLm.append(lm.x)
            postureLm.append(lm.y)

        # if bad posture detected
        if predict(postureLm, model).round() == float(1):
            # bounding box colour is red
            bboxColour = (0, 0, 255)
        # else, it is a good posture
        else:
            # bounding box colour is green
            bboxColour = (0, 255, 0)

        # display bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), bboxColour, 2)

        # label for object and confidence
        cv2.putText(frame,
                    f'{classNames[classIds[i]].upper()} {int(confs[i] * 100)}% {str("estimator ID ") + str(poseObjIdx)}',
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)


while True:
    success, frame = cap.read()

    # if video stream ended
    if not success:
        print('End of video stream...')
        break

    # inputs from frame are stored in a blob, which will be used for the model input
    blob = cv2.dnn.blobFromImage(frame, 1 / 255, (320, 320), [0, 0, 0], 1, crop=False)

    # set the blob as input for model
    net.setInput(blob)

    # YOLO's 3 output layers
    layerNames = net.getLayerNames()
    # print(net.getUnconnectedOutLayers())
    # breakpoint()
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
    frame = cv2.resize(frame, (1270, 720))
    cv2.imshow('Video Stream', frame)
    cv2.waitKey(1)

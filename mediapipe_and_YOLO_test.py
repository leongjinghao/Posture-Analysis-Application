import cv2
import numpy as np
import mediapipe as mp
import time

cap = cv2.VideoCapture('video_sample/exercise.mp4')
whT = 320
confThreshold = 0.5
nmsThreshold = 0.3
pTime = 0

classNames = []
with open('YOLO_config/coco.names', 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

modelConfiguration = 'YOLO_config/yolov3-320.cfg'
modelWeights = 'YOLO_config/yolov3-320.weights'

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

mpPose = mp.solutions.pose
pose = mpPose.Pose(min_detection_confidence=0.5)
mpDraw = mp.solutions.drawing_utils
mpDrawingStyle = mp.solutions.drawing_styles

def multiPersonPostureRecognition(outputs, img):
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []

    for output in outputs:
        for det in output:
            scores = det[5:]
            # get highest scored classname identified
            classId = np.argmax(scores)
            # if object detected is not not a person, skip this object
            if not classId == 0:
                break
            confidence = scores[classId]
            # if confidence level for person detected is higher than threshold
            if confidence > confThreshold:
                w, h = int(det[2] * wT), int(det[3] * hT)
                x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))

    indicies = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)

    # for each person detected
    for i in indicies:
        i = i[0]
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        # bounding box
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
        # label for object and confidence
        cv2.putText(img, f'{classNames[classIds[i]].upper()} {int(confs[i] * 100)}%',
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

        # for each person
        crop_img = img[y: y + h, x: x + w]
        #cv2.imshow('test', crop_img)
        #breakpoint()
        crop_img_h, crop_img_w, _ = crop_img.shape

        # skip if image cropped is empty
        try:
            frameRGB = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
        except:
            continue

        # To improve performance, optionally mark the frame as not writeable to pass by reference.
        frameRGB.flags.writeable = False
        results = pose.process(frameRGB)

        '''
        if not results.pose_landmarks:
            continue
        print(
            f'Nose coordinates: ('
            f'{results.pose_landmarks.landmark[mpPose.PoseLandmark.NOSE].x * crop_img_w}, '
            f'{results.pose_landmarks.landmark[mpPose.PoseLandmark.NOSE].y * crop_img_h})'
        )'''

        # draw landmarks on the cropped image
        mpDraw.draw_landmarks(crop_img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)


while True:
    success, img = cap.read()

    # check if there are still frames left on video stream
    try:
        blob = cv2.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
    except:
        print('End of video stream...')
        break
    net.setInput(blob)

    layerNames = net.getLayerNames()
    outputNames = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    outputs = net.forward(outputNames)

    multiPersonPostureRecognition(outputs, img)

    # show FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow('Video Stream', img)
    cv2.waitKey(1)

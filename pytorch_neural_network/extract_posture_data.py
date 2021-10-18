import cv2
import numpy as np
import mediapipe as mp
import time

cap = cv2.VideoCapture('../video_sample/goodposture.mp4')
# 1 = bad posture data, 0 = good posture data
posClass = 0
whT = 320
confThreshold = 0.5
nmsThreshold = 0.3
pTime = 0

classNames = []
with open('../YOLO_config/coco.names', 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

modelConfiguration = '../YOLO_config/yolov4-tiny.cfg'
modelWeights = '../YOLO_config/yolov4-tiny.weights'

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

mpPose = mp.solutions.pose
pose = mpPose.Pose(min_detection_confidence=0.5)
mpDraw = mp.solutions.drawing_utils


def findObjects(outputs, img):
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []

    for output in outputs:
        for det in output:
            scores = det[5:]
            # get highest scored classname identified
            classId = np.argmax(scores)
            # if person is detected
            if not classId == 0:
                break
            confidence = scores[classId]
            if confidence > confThreshold:
                w, h = int(det[2] * wT), int(det[3] * hT)
                x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))

    indicies = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold, top_k=1)

    for i in indicies:
        i = i[0]
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        # bounding box
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
        # label for object and confidence
        cv2.putText(img, f'{classNames[classIds[i]].upper()} {int(confs[i] * 100)}%',
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

        # crop frame for the person
        crop_img = img[y: y + h, x: x + w]
        crop_img_h, crop_img_w, _ = crop_img.shape

        results = pose.process(cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB))

        # plot if landmark is detected
        if results.pose_landmarks:

            # draw landmarks on the image
            mpDraw.draw_landmarks(
                crop_img,
                results.pose_landmarks,
                mpPose.POSE_CONNECTIONS)

            # log landmarks data
            for id, lm in enumerate(results.pose_landmarks.landmark):
                if id < 32:
                    delimiter = ', '
                else:
                    delimiter = ', {0}\n'.format(posClass)
                with open('posture_log_file/landmark_data.txt', 'a') as f:
                    f.write("{0}, {1}{2}".format(lm.x, lm.y, delimiter))


while True:
    success, img = cap.read()

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
    net.setInput(blob)

    layerNames = net.getLayerNames()
    outputNames = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    # print(outputNames)

    outputs = net.forward(outputNames)

    findObjects(outputs, img)

    # show FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, "{:.1f} FPS".format(float(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    img = cv2.resize(img, (1270, 720))
    cv2.imshow('Image', img)
    cv2.waitKey(1)

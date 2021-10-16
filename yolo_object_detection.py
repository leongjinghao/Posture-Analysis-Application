import cv2
import numpy as np
import time

cap = cv2.VideoCapture('video_sample/exercise.mp4')
whT = 320
confThreshold = 0.5
nmsThreshold = 0.3
pTime = 0

classNames = []
with open('YOLO_config/coco.names', 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

modelConfiguration = 'YOLO_config/yolov4-tiny.cfg'
modelWeights = 'YOLO_config/yolov4-tiny.weights'

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

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
            # filter for person
            if not classId == 0:
                break
            confidence = scores[classId]
            if confidence > confThreshold:
                w, h = int(det[2] * wT), int(det[3] * hT)
                x, y = int((det[0] * wT) - w/2), int((det[1] * hT) - h/2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))

    indicies = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)

    for i in indicies:
        i = i[0]
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        # bounding box
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 2)
        # label for object and confidence
        cv2.putText(img, f'{classNames[classIds[i]].upper()} {int(confs[i] * 100)}%',
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

while True:
    success, img = cap.read()

    blob = cv2.dnn.blobFromImage(img, 1/255, (whT, whT), [0, 0, 0], 1, crop=False)
    net.setInput(blob)

    layerNames = net.getLayerNames()
    outputNames = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    #print(outputNames)

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

import cv2
import mediapipe as mp

import time

mpPose = mp.solutions.pose
pose = mpPose.Pose(min_detection_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture('video_sample/goodposture.mp4')
pTime = 0
writeLM = False
# 1 = bad posture data, 0 = good posture data
posClass = 0

if writeLM:
    # overwrite previous landmark data
    open('neural_network/posture_log_file/landmark_data.txt', 'w')

while True:
    success, frame = cap.read()
    if not success:
        break
    # cv2 frames are in BGR while mediapipe uses RGB, hence conversion required
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to pass by reference.
    frameRGB.flags.writeable = False
    results = pose.process(frameRGB)

    # plot if landmark is detected
    if results.pose_landmarks:
        # Draw the pose annotation on the image.
        # plot all landmark detected in results
        mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

        # plotting without the above API call, mpDraw.draw_landmarks()
        # calculating the actual pixel value using the ratio of x and y in lm
        for id, lm in enumerate(results.pose_landmarks.landmark):
            # get the dimensions (in pixel) of the video
            h, w, c = frame.shape
            # calculate pixel value
            xPixelValue, yPixelValue = int(lm.x * w), int(lm.y * h)
            # plot the landmarks individually
            cv2.circle(frame, (xPixelValue, yPixelValue), 3, (255, 0, 255), cv2.FILLED)
            # True, write landmark data into a txt file
            if writeLM:
                if id < 32:
                    delimiter = ', '
                else:
                    delimiter = ', {0}\n'.format(posClass)
                with open('neural_network/posture_log_file/landmark_data.txt', 'a') as f:
                    f.write("{0}, {1}{2}".format(lm.x, lm.y, delimiter))

    # show FPS
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(frame, "{:.1f} FPS".format(float(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    #frame = cv2.resize(frame, (1270, 720))
    # video output with landmark plotted
    cv2.imshow("Video", frame)
    # delay
    cv2.waitKey(1)

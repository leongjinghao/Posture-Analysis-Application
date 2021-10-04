import cv2
import mediapipe as mp

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture('video_sample\\exercise.mp4')
pTime = 0

# overwrite previous landmark data
open('landmark_data.txt', 'w')

while True:
    success, frame = cap.read()
    # cv2 frames are in BGR while mediapipe uses RGB, hence conversion required
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frameRGB)

    # override previous data stored in landmark_data.txt

    # plot if landmark is detected
    if results.pose_landmarks:
        # plot all landmark detected in results
        mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

        # plotting without the above API call, mpDraw.draw_landmarks()
        # calculating the actual pixel value using the ratio of x and y in lm
        for id, lm in enumerate(results.pose_landmarks.landmark):
            # get the dimentions (in pixel) of the video
            h, w, c = frame.shape
            # calculate pixel value
            xPixelValue, yPixelValue = int (lm.x * w), int(lm.y * h)
            # plot the landmarks individually
            cv2.circle(frame, (xPixelValue, yPixelValue), 3, (255, 0, 255), cv2.FILLED)
            # write landmark data into a txt file
            with open('landmark_data.txt', 'a') as f:
                f.write("{0}, {1}, {2}, {3}\n".format(id, lm.x, lm.y, lm.z))

    # video output with landmark plotted
    cv2.imshow("Video", frame)
    # delay
    cv2.waitKey(1)
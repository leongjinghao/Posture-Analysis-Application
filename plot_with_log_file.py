import cv2
import time

cap = cv2.VideoCapture('video_sample/exercise.mp4')
pTime = 0
count = 0

while True:
    success, frame = cap.read()

    # plotting without the above API call, mpDraw.draw_landmarks()
    # calculating the actual pixel value using the ratio of x and y in lm
    with open('landmark_data.txt', 'r') as f:
        lm_data = f.readlines()

    for i in range(33):
        line = lm_data[count + i]
        coordinates = line.replace('\n', '').split(', ')
        # get the dimensions (in pixel) of the video
        h, w, c = frame.shape
        # calculate pixel value
        xPixelValue, yPixelValue = int(float(coordinates[1]) * w), int(float(coordinates[2]) * h)
        # plot the landmarks individually
        cv2.circle(frame, (xPixelValue, yPixelValue), 3, (255, 0, 255), cv2.FILLED)
        # write landmark data into a txt file

    # shift to next set of landmark (each posture (per frame) consist a set of 33 lm)
    count += 33

    # show FPS
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(frame, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # video output with landmark plotted
    cv2.imshow("Video", frame)
    # delay
    cv2.waitKey(1)

import cv2
import time

cap = cv2.VideoCapture('video_sample/exercise.mp4')
pTime = 0
count = 0

# read landmark log file
with open('neural_network/posture_log_file/landmark_data.txt', 'r') as f:
    lm_data = f.readlines()

# line index of landmark log file
lineIndex = 0

while True:
    success, frame = cap.read()

    if not success:
        break

    line = lm_data[lineIndex]
    coordinates = line.replace('\n', '').split(', ')
    # get the dimensions (in pixel) of the video
    h, w, c = frame.shape
    # plot x, y coordinates (in pair) for each landmark (33 in total)
    for i in range(0, 66, 2):
        # calculate pixel value
        xPixelValue, yPixelValue = int(float(coordinates[i]) * w), int(float(coordinates[i + 1]) * h)
        # plot the landmarks individually
        cv2.circle(frame, (xPixelValue, yPixelValue), 3, (255, 0, 255), cv2.FILLED)

    # increment to next line in landmark log file
    lineIndex += 1

    # show FPS
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(frame, "{:.1f} FPS".format(float(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    frame = cv2.resize(frame, (1270, 720))
    # video output with landmark plotted
    cv2.imshow("Video", frame)
    # delay
    cv2.waitKey(1)

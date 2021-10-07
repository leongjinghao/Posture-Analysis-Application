import os
import cv2
import time
import argparse
import posenet
import tensorflow as tf
import matplotlib.pyplot as plt

input_file = 'video_sample\\exercise.mp4'
output_file = 'testOutput.mp4'
# Load input video files and
cap = cv2.VideoCapture(input_file)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
# create a video writer to write the output file
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
video = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

model = 101
scale_factor = 0.4

with tf.Session() as sess:
    # Load PoseNet model
    model_cfg, model_outputs = posenet.load_model(model, sess)
    output_stride = model_cfg['output_stride']
    start = time.time()

    incnt = 0
    # Process the whole video frame by frame
    while True:
        # Increase frame count by one
        incnt = incnt + 1
        try:
            # read_cap is utility function to read and process from video
            input_image, draw_image, output_scale = posenet.read_cap(
                cap, scale_factor=scale_factor, output_stride=output_stride)
        except:
            break
        # run the model on the image and generate output results
        heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess.run(
            model_outputs,
            feed_dict={'image:0': input_image}
        )
        # here we filter poses generated by above model
        # and output pose score, keypoint scores and their keypoint coordinates
        # this function will return maximum 10 pose, it can be changed by maximum_pose
        # variable.
        pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multiple_poses(
            heatmaps_result.squeeze(axis=0),
            offsets_result.squeeze(axis=0),
            displacement_fwd_result.squeeze(axis=0),
            displacement_bwd_result.squeeze(axis=0),
            output_stride=output_stride,
            min_pose_score=0.25)
        # scale keypoint co-ordinate to output scale
        keypoint_coords *= output_scale
        # draw pose on input frame to obtain output frame
        draw_image = posenet.draw_skel_and_kp(
            draw_image, pose_scores, keypoint_scores, keypoint_coords,
            min_pose_score=0.25, min_part_score=0.25)
        video.write(draw_image)
# release the videoreader and writer
video.release()
cap.release()
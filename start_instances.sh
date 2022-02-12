#!/bin/bash

python python_scripts/posture_analyser_main.py "python_scripts/video_sample/dancing2.mp4" 2 &
python python_scripts/posture_analyser_main.py "python_scripts/video_sample/cycling.mp4" 1 &
# python python_scripts/posture_analyser_main.py "http://localhost:5002/video" 2 &